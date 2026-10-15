import json
import os
import pickle
import re
import sys
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import spacy
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel, LdaModel, Word2Vec
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score, roc_curve,
                             silhouette_score)
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from wordcloud import WordCloud

SEED = 42
DATA_PATH = "beauty_reviews.csv"
OUT_DIR = "outputs"
ENTITY_LABELS = {"ORG", "PRODUCT", "GPE", "LOC"}
LDA_KS = [5, 7, 10]
# Human-readable LDA labels keyed by topic id for the selected k
TOPIC_LABELS = {0: "Value for money & product failure", 1: "Hair, wigs & accessories",
                2: "Nail polish & brushes", 3: "Eye/lash, makeup & general value",
                4: "Skincare, scent & lip care"}
# Non-entity tokens that spaCy mislabels as ORG/GPE in review text
ENTITY_STOPLIST = {"nice", "great", "excelente", "videoid", "argan", "cons"}


def load_data(path):
    # Load reviews and drop empty rows
    df = pd.read_csv(path).dropna(subset=["review_text", "sentiment"]).reset_index(drop=True)
    df["sentiment"] = df["sentiment"].astype(int)
    return df


def preprocess(texts, cache_path):
    # One spaCy pass: POS stream, light stream and raw-text entities
    if os.path.exists(cache_path):
        with open(cache_path, "rb") as f:
            return pickle.load(f)
    nlp = spacy.load("en_core_web_lg", disable=["parser"])
    pos_tokens, light_tokens, entities = [], [], []
    for doc in nlp.pipe(texts, batch_size=64, n_process=2):
        pos_tokens.append([t.lemma_.lower() for t in doc
                           if t.pos_ in {"NOUN", "ADJ"} and t.is_alpha and not t.is_stop and len(t.lemma_) > 2])
        light_tokens.append([t.lower_ for t in doc
                             if t.pos_ in {"NOUN", "PROPN", "VERB", "ADJ", "ADV"}
                             and t.is_alpha and not t.is_stop and len(t) > 2])
        entities.append([(e.text, e.label_) for e in doc.ents if e.label_ in ENTITY_LABELS])
    with open(cache_path, "wb") as f:
        pickle.dump((pos_tokens, light_tokens, entities), f)
    return pos_tokens, light_tokens, entities


def normalise_entity(text):
    # Lowercase, strip possessives, leading "the" and non-letters
    t = re.sub(r"[’']s\b", "", text.lower())
    t = re.sub(r"^the\s+", "", t)
    t = re.sub(r"[^a-z0-9&\.\- ]", "", t).strip()
    return t


def run_ner(entities, sentiments, out_dir, top_n=20):
    # Count entity mentions and mean sentiment of reviews mentioning each
    counts, labels, reviews = Counter(), defaultdict(Counter), defaultdict(set)
    for i, ents in enumerate(entities):
        for text, label in ents:
            e = normalise_entity(text)
            if len(e) < 3 or not re.search(r"[a-z]", e) or e in ENTITY_STOPLIST:
                continue
            counts[e] += 1
            labels[e][label] += 1
            reviews[e].add(i)
    rows = []
    for e, c in counts.most_common(top_n):
        idx = list(reviews[e])
        rows.append({"entity": e, "label": labels[e].most_common(1)[0][0], "mentions": c,
                     "reviews": len(idx), "mean_sentiment": float(np.mean(sentiments[idx]))})
    table = pd.DataFrame(rows)
    table.to_csv(os.path.join(out_dir, "top_entities.csv"), index=False)

    fig, ax = plt.subplots(figsize=(9, 7))
    colors = sns.color_palette("RdYlGn", as_cmap=True)(table["mean_sentiment"].values)
    ax.barh(table["entity"][::-1], table["mentions"][::-1], color=colors[::-1])
    ax.set_xlabel("Mentions")
    ax.set_title("Top 20 named entities (bar colour = mean sentiment, red=neg, green=pos)")
    for y, (m, s) in enumerate(zip(table["mentions"][::-1], table["mean_sentiment"][::-1])):
        ax.text(m, y, f" {s:.2f}", va="center", fontsize=8)
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "ner_top20.png"), dpi=150)
    plt.close(fig)
    return table


def build_tfidf_heatmap(pos_tokens, sentiments, out_dir, per_class=25):
    # Cosine similarity heatmap on a label-balanced random sample
    docs = [" ".join(t) for t in pos_tokens]
    X = TfidfVectorizer(min_df=2).fit_transform(docs)
    rng = np.random.RandomState(SEED)
    idx = np.concatenate([rng.choice(np.where(sentiments == c)[0], per_class, replace=False) for c in (0, 1)])
    S = cosine_similarity(X[idx])
    lab = sentiments[idx]
    same = lab[:, None] == lab[None, :]
    off = ~np.eye(len(idx), dtype=bool)
    stats = {"within_label_mean": float(S[same & off].mean()), "cross_label_mean": float(S[~same].mean()),
             "within_neg": float(S[(lab[:, None] == 0) & (lab[None, :] == 0) & off].mean()),
             "within_pos": float(S[(lab[:, None] == 1) & (lab[None, :] == 1) & off].mean())}
    ticks = ["neg" if l == 0 else "pos" for l in lab]
    fig, ax = plt.subplots(figsize=(9, 8))
    vmax = np.percentile(S[off], 99)
    sns.heatmap(S, ax=ax, cmap="viridis", vmax=vmax, xticklabels=ticks, yticklabels=ticks,
                cbar_kws={"label": "cosine similarity (clipped at 99th pct)"})
    ax.axhline(per_class, color="white", lw=2)
    ax.axvline(per_class, color="white", lw=2)
    ax.set_title("TF-IDF cosine similarity (50 reviews, sorted by sentiment)")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "tfidf_cosine_heatmap.png"), dpi=150)
    plt.close(fig)
    return stats


def train_word2vec(light_tokens):
    # Train Word2Vec and average word vectors into document embeddings
    model = Word2Vec(light_tokens, vector_size=100, window=5, min_count=2, workers=2, epochs=15, seed=SEED)
    emb = np.zeros((len(light_tokens), model.vector_size), dtype=np.float32)
    for i, toks in enumerate(light_tokens):
        vecs = [model.wv[t] for t in toks if t in model.wv]
        if vecs:
            emb[i] = np.mean(vecs, axis=0)
    return model, emb


def plot_pca_comparison(pos_tokens, w2v_emb, sentiments, out_dir):
    # 2-D PCA for TF-IDF (after SVD-50) and Word2Vec embeddings
    X = TfidfVectorizer(min_df=2).fit_transform([" ".join(t) for t in pos_tokens])
    svd50 = TruncatedSVD(n_components=50, random_state=SEED).fit_transform(X)
    reps = {"TF-IDF (SVD-50 → PCA)": svd50, "Word2Vec (mean) → PCA": w2v_emb}
    stats = {}
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, (name, M) in zip(axes, reps.items()):
        pca = PCA(n_components=2, random_state=SEED)
        P = pca.fit_transform(M)
        for c, col, lab in ((0, "#d62728", "negative"), (1, "#2ca02c", "positive")):
            ax.scatter(P[sentiments == c, 0], P[sentiments == c, 1], s=5, alpha=0.3, c=col, label=lab)
        ax.set_title(f"{name}\nexplained var (2 PCs): {pca.explained_variance_ratio_.sum():.1%}")
        ax.set_xlabel("PC1")
        ax.set_ylabel("PC2")
        ax.legend(markerscale=3)
        sil = silhouette_score(M, sentiments, sample_size=3000, random_state=SEED)
        stats[name] = {"explained_var_2pc": float(pca.explained_variance_ratio_.sum()),
                       "silhouette_by_sentiment_full_dim": float(sil)}
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "pca_tfidf_vs_word2vec.png"), dpi=150)
    plt.close(fig)
    return stats


def run_lda(pos_tokens, sentiments, out_dir):
    # BoW LDA for k in LDA_KS, pick best by c_v, word clouds, dominant-topic sentiment table
    dictionary = Dictionary(pos_tokens)
    dictionary.filter_extremes(no_below=5, no_above=0.5)
    corpus = [dictionary.doc2bow(t) for t in pos_tokens]
    models, scores = {}, {}
    for k in LDA_KS:
        m = LdaModel(corpus, num_topics=k, id2word=dictionary, passes=10, iterations=100,
                     random_state=SEED, chunksize=2000, alpha="auto", eta="auto")
        models[k] = m
        scores[k] = CoherenceModel(model=m, texts=pos_tokens, dictionary=dictionary,
                                   coherence="c_v", processes=1).get_coherence()
    best_k = max(scores, key=scores.get)
    best = models[best_k]

    topic_words = {i: [w for w, _ in best.show_topic(i, 10)] for i in range(best_k)}
    labels = {i: TOPIC_LABELS.get(i, "/".join(topic_words[i][:3])) for i in range(best_k)}

    cols = 4
    rows = int(np.ceil(best_k / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
    for i, ax in enumerate(np.atleast_1d(axes).ravel()):
        ax.axis("off")
        if i < best_k:
            wc = WordCloud(width=400, height=300, background_color="white", random_state=SEED)
            ax.imshow(wc.generate_from_frequencies(dict(best.show_topic(i, 30))), interpolation="bilinear")
            ax.set_title(f"T{i}: {labels[i]}", fontsize=10)
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, "lda_wordclouds.png"), dpi=150)
    plt.close(fig)

    dominant = []
    for bow in corpus:
        if not bow:
            dominant.append(-1)
            continue
        dist = best.get_document_topics(bow, minimum_probability=0)
        dominant.append(max(dist, key=lambda x: x[1])[0])
    dominant = np.array(dominant)
    rows_out = []
    for i in range(best_k):
        mask = dominant == i
        rows_out.append({"topic": i, "label": labels[i], "top_words": ", ".join(topic_words[i][:8]),
                         "reviews": int(mask.sum()),
                         "pct_positive": float(sentiments[mask].mean() * 100) if mask.any() else np.nan,
                         "pct_negative": float((1 - sentiments[mask].mean()) * 100) if mask.any() else np.nan})
    table = pd.DataFrame(rows_out).sort_values("reviews", ascending=False)
    table.to_csv(os.path.join(out_dir, "lda_topic_sentiment.csv"), index=False)
    return {"coherence": {int(k): float(v) for k, v in scores.items()}, "best_k": int(best_k),
            "empty_docs": int((dominant == -1).sum())}, table


def train_classifiers(pos_tokens, sentiments, out_dir):
    # Split first, fit TF-IDF on train only, evaluate three classifiers
    docs = np.array([" ".join(t) for t in pos_tokens])
    tr, te = train_test_split(np.arange(len(docs)), test_size=0.2, random_state=SEED, stratify=sentiments)
    vec = TfidfVectorizer(min_df=2, ngram_range=(1, 2))
    Xtr, Xte = vec.fit_transform(docs[tr]), vec.transform(docs[te])
    models = {"MultinomialNB": MultinomialNB(), "BernoulliNB": BernoulliNB(),
              "Logistic Regression": LogisticRegression(max_iter=1000, random_state=SEED)}
    rows, curves = [], {}
    for name, m in models.items():
        m.fit(Xtr, sentiments[tr])
        prob = m.predict_proba(Xte)[:, 1]
        rows.append(score_row(name, sentiments[te], prob))
        curves[name] = roc_curve(sentiments[te], prob)
    plot_roc(curves, rows, out_dir, "roc_curves.png")
    return pd.DataFrame(rows), (tr, te)


def score_row(name, y_true, prob):
    # Metrics at the 0.5 threshold plus AUC
    pred = (prob >= 0.5).astype(int)
    return {"model": name, "accuracy": accuracy_score(y_true, pred),
            "precision": precision_score(y_true, pred), "recall": recall_score(y_true, pred),
            "f1": f1_score(y_true, pred), "auc": roc_auc_score(y_true, prob)}


def plot_roc(curves, rows, out_dir, fname):
    # ROC curves for all models on the same axes
    fig, ax = plt.subplots(figsize=(7, 6))
    aucs = {r["model"]: r["auc"] for r in rows}
    for name, (fpr, tpr, _) in curves.items():
        ax.plot(fpr, tpr, label=f"{name} (AUC={aucs[name]:.3f})")
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("ROC curves")
    ax.legend(loc="lower right")
    plt.tight_layout()
    fig.savefig(os.path.join(out_dir, fname), dpi=150)
    plt.close(fig)


def distilbert_classifier(texts, sentiments, split, cache_path, batch_size=32, max_length=128):
    # CLS embeddings from pre-trained DistilBERT + Logistic Regression; returns None if unavailable
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
        if os.path.exists(cache_path):
            emb = np.load(cache_path)
        else:
            tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            model = AutoModel.from_pretrained("distilbert-base-uncased").eval()
            chunks = []
            with torch.no_grad():
                for i in range(0, len(texts), batch_size):
                    enc = tok(list(texts[i:i + batch_size]), padding=True, truncation=True,
                              max_length=max_length, return_tensors="pt")
                    chunks.append(model(**enc).last_hidden_state[:, 0, :].numpy())
            emb = np.vstack(chunks)
            np.save(cache_path, emb)
    except Exception as exc:
        print(f"DistilBERT skipped: {type(exc).__name__}", file=sys.stderr)
        return None
    tr, te = split
    clf = LogisticRegression(max_iter=2000, random_state=SEED).fit(emb[tr], sentiments[tr])
    prob = clf.predict_proba(emb[te])[:, 1]
    return score_row("DistilBERT CLS + LR", sentiments[te], prob), roc_curve(sentiments[te], prob)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = load_data(DATA_PATH)
    y = df["sentiment"].values
    pos_tokens, light_tokens, entities = preprocess(df["review_text"].tolist(), os.path.join(OUT_DIR, "tokens.pkl"))

    results = {"n_reviews": len(df), "pct_positive": float(y.mean() * 100)}
    ner_table = run_ner(entities, y, OUT_DIR)
    results["tfidf_similarity"] = build_tfidf_heatmap(pos_tokens, y, OUT_DIR)
    _, w2v_emb = train_word2vec(light_tokens)
    results["pca"] = plot_pca_comparison(pos_tokens, w2v_emb, y, OUT_DIR)
    lda_info, lda_table = run_lda(pos_tokens, y, OUT_DIR)
    results["lda"] = lda_info
    clf_table, split = train_classifiers(pos_tokens, y, OUT_DIR)

    bert = distilbert_classifier(df["review_text"].values, y, split, os.path.join(OUT_DIR, "distilbert_cls.npy"))
    if bert is not None:
        clf_table = pd.concat([clf_table, pd.DataFrame([bert[0]])], ignore_index=True)
    clf_table.to_csv(os.path.join(OUT_DIR, "classifier_comparison.csv"), index=False)

    with open(os.path.join(OUT_DIR, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(ner_table.to_string(index=False))
    print(lda_table.to_string(index=False))
    print(clf_table.round(4).to_string(index=False))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()