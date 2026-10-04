
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score, f1_score, accuracy_score, classification_report, ConfusionMatrixDisplay
from gensim.models import Word2Vec, Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import gensim.downloader as api
from sentence_transformers import SentenceTransformer

SEED = 42
SAMPLE_N = 60000  # stratified subsample for speed; None = full data
PATH = "Data_Set__Question_Identification_-_Data_Set___1748351159-5ea65d4bfbba7875acb26a15__1__csv.csv"

# load
df = pd.read_csv(PATH).dropna(subset=["sentence"]).drop_duplicates(subset=["sentence", "label"])
df["y"] = (df.label == "question").astype(int)
if SAMPLE_N:
    df = df.groupby("y").sample(frac=min(1, SAMPLE_N / len(df)), random_state=SEED)

# punctuation is stripped (99.4% of questions end in '?'); stopwords kept (wh-words are the signal)
def clean(t):
    t = t.lower()
    t = re.sub(r"https?://\S+|www\.\S+", " ", t)
    t = re.sub(r"\d+", " ", t)
    t = re.sub(r"[^a-z\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

df["clean"] = df.sentence.map(clean)
df = df[df.clean.str.len() > 0].reset_index(drop=True)
df["tokens"] = df.clean.str.split()

tr, te = train_test_split(df, test_size=0.2, stratify=df.y, random_state=SEED)
ytr, yte = tr.y.values, te.y.values

# vectorizers: each returns (Xtr, Xte, is_sparse)
def sparse_vec(v):
    return lambda: (v.fit_transform(tr.clean), v.transform(te.clean), True)

def avg_embed(tokens, kv, dim):
    vs = [kv[w] for w in tokens if w in kv]
    return np.mean(vs, axis=0) if vs else np.zeros(dim)

def w2v():
    m = Word2Vec(tr.tokens.tolist(), vector_size=100, window=5, min_count=2, workers=4, epochs=10, seed=SEED)
    f = lambda d: np.vstack([avg_embed(t, m.wv, 100) for t in d.tokens])
    return f(tr), f(te), False

def glove():
    kv = api.load("glove-wiki-gigaword-100")
    f = lambda d: np.vstack([avg_embed(t, kv, 100) for t in d.tokens])
    return f(tr), f(te), False

def d2v():
    docs = [TaggedDocument(t, [i]) for i, t in enumerate(tr.tokens)]
    m = Doc2Vec(docs, vector_size=100, window=5, min_count=2, workers=4, epochs=10, seed=SEED)
    inf = lambda d: np.vstack([m.infer_vector(t) for t in d.tokens])
    return np.vstack([m.dv[i] for i in range(len(docs))]), inf(te), False

def sbert():
    m = SentenceTransformer("all-MiniLM-L6-v2")
    f = lambda d: m.encode(d.clean.tolist(), batch_size=256, show_progress_bar=False)
    return f(tr), f(te), False

VECTORIZERS = {
    "BoW": sparse_vec(CountVectorizer(max_features=20000)),
    "TF-IDF": sparse_vec(TfidfVectorizer(max_features=20000)),
    "TF-IDF (1-3gram)": sparse_vec(TfidfVectorizer(ngram_range=(1, 3), min_df=3, max_features=50000)),
    "Word2Vec": w2v,
    "GloVe": glove,
    "Doc2Vec": d2v,
    "SBERT": sbert,
}

def models(sparse):
    m = {
        "LogReg": LogisticRegression(max_iter=1000),
        "LinearSVM": LinearSVC(C=0.5),
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=40 if sparse else None, n_jobs=-1, random_state=SEED),
    }
    if sparse:
        m["NaiveBayes"] = MultinomialNB()  # needs non-negative features
    return m

def score(model, X):
    return model.predict_proba(X)[:, 1] if hasattr(model, "predict_proba") else model.decision_function(X)

# train + evaluate
results, curves, fitted, feats = [], {}, {}, {}
for vname, make in VECTORIZERS.items():
    Xtr, Xte, sp = make()
    feats[vname] = Xte
    for mname, model in models(sp).items():
        model.fit(Xtr, ytr)
        s = score(model, Xte)
        curves[(vname, mname)] = roc_curve(yte, s)[:2]
        fitted[(vname, mname)] = model
        pred = model.predict(Xte)
        results.append(dict(vectorizer=vname, model=mname, auc=roc_auc_score(yte, s),
                            f1=f1_score(yte, pred), acc=accuracy_score(yte, pred)))
res = pd.DataFrame(results).sort_values("auc", ascending=False).reset_index(drop=True)
print(res.to_string())
print(res.pivot(index="vectorizer", columns="model", values="auc").round(4).to_string())

# ROC: one panel per vectorizer
fig, axes = plt.subplots(2, 4, figsize=(20, 9))
for ax, v in zip(axes.ravel(), VECTORIZERS):
    for (vn, mn), (fpr, tpr) in curves.items():
        if vn == v:
            auc = res[(res.vectorizer == v) & (res.model == mn)].auc.iloc[0]
            ax.plot(fpr, tpr, label=f"{mn} ({auc:.4f})")
    ax.plot([0, 1], [0, 1], "k--", lw=0.8)
    ax.set(title=v, xlabel="FPR", ylabel="TPR")
    ax.legend(loc="lower right")
axes.ravel()[-1].axis("off")
plt.tight_layout()
plt.savefig("roc_per_vectorizer.png", dpi=150)

# ROC: all combinations
plt.figure(figsize=(8, 6))
for (v, m), (fpr, tpr) in curves.items():
    plt.plot(fpr, tpr, lw=1, label=f"{v} + {m}")
plt.plot([0, 1], [0, 1], "k--")
plt.xlabel("FPR"); plt.ylabel("TPR"); plt.title("ROC: all combinations")
plt.legend(fontsize=6, ncol=2)
plt.savefig("roc_all.png", dpi=150)

# best model
best = res.iloc[0]
pred = fitted[(best.vectorizer, best.model)].predict(feats[best.vectorizer])
print(f"Best: {best.vectorizer} + {best.model}")
print(classification_report(yte, pred, target_names=["sentence", "question"], digits=4))
ConfusionMatrixDisplay.from_predictions(yte, pred, display_labels=["sentence", "question"])
plt.title(f"{best.vectorizer} + {best.model}")
plt.savefig("confusion_matrix.png", dpi=150)
plt.show()