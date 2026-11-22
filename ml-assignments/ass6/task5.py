import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler

DATA = "epldata_final.csv"
FEATURES = ["age", "position_cat", "page_views", "fpl_value", "fpl_sel", "fpl_points",
            "region", "new_foreign", "age_cat", "big_club", "new_signing"]
K = 5
POP, GENS, ELITE = 40, 40, 2
TOURN, CX_RATE, MUT_RATE, MUT_STD = 3, 0.9, 0.15, 0.15
SIGMA_SHARE = 0.6  # niche radius for fitness sharing
rng = np.random.default_rng(42)

df = pd.read_csv(DATA)
df["region"] = df["region"].fillna(4)  # one missing region (Benin -> Rest of World)
df["fpl_sel"] = df["fpl_sel"].astype(str).str.rstrip("%").astype(float)
X_tr, X_te, y_tr, y_te = train_test_split(df[FEATURES], df["market_value"], test_size=0.2, random_state=42)
scaler = MinMaxScaler().fit(X_tr)
X_tr, X_te = scaler.transform(X_tr), scaler.transform(X_te)
y_tr, y_te = y_tr.to_numpy(), y_te.to_numpy()
folds = list(KFold(n_splits=5, shuffle=True, random_state=42).split(X_tr))
D = len(FEATURES)


def rmse_knn(w, Xa, ya, Xb, yb):
    m = KNeighborsRegressor(n_neighbors=K, weights="distance").fit(Xa * w, ya)
    return np.sqrt(mean_squared_error(yb, m.predict(Xb * w)))


def cv_rmse(w):  # fitness base: CV error on the training set only
    return np.mean([rmse_knn(w, X_tr[a], y_tr[a], X_tr[b], y_tr[b]) for a, b in folds])


def shared_fitness(pop, raw):
    # fitness sharing: divide by niche count so crowded regions are penalised
    d = np.linalg.norm(pop[:, None] - pop[None], axis=2)
    sh = np.where(d < SIGMA_SHARE, 1 - d / SIGMA_SHARE, 0.0)
    return raw / sh.sum(axis=1)


def tournament(pop, fit):
    idx = rng.integers(0, len(pop), TOURN)
    return pop[idx[np.argmax(fit[idx])]].copy()


def crossover(a, b):
    if rng.random() > CX_RATE:
        return a.copy(), b.copy()
    alpha = rng.random(D)  # blend crossover
    return alpha * a + (1 - alpha) * b, alpha * b + (1 - alpha) * a


def mutate(c):
    mask = rng.random(D) < MUT_RATE
    c[mask] += rng.normal(0, MUT_STD, mask.sum())
    return np.clip(c, 0, 1)


def diversity(pop):
    d = np.linalg.norm(pop[:, None] - pop[None], axis=2)
    return d.sum() / (len(pop) * (len(pop) - 1))


pop = rng.random((POP, D))
pop[0] = np.ones(D)  # seed with the unweighted baseline
best_w, best_err = pop[0].copy(), np.inf
for g in range(GENS):
    err = np.array([cv_rmse(w) for w in pop])
    raw = 1.0 / err
    fit = shared_fitness(pop, raw)
    if err.min() < best_err:
        best_err, best_w = err.min(), pop[err.argmin()].copy()
    if g % 5 == 0 or g == GENS - 1:
        print(f"gen {g:2d} | best CV RMSE {best_err:.3f} | mean CV RMSE {err.mean():.3f} | diversity {diversity(pop):.3f}")
    order = np.argsort(-raw)
    nxt = [pop[i].copy() for i in order[:ELITE]]
    while len(nxt) < POP:
        c1, c2 = crossover(tournament(pop, fit), tournament(pop, fit))
        nxt += [mutate(c1), mutate(c2)]
    pop = np.array(nxt[:POP])

ones = np.ones(D)
print("\nlearned attribute weights:")
for f, w in sorted(zip(FEATURES, best_w), key=lambda t: -t[1]):
    print(f"  {f:13s} {w:.3f}")
print(f"\ntest RMSE | unweighted kNN: {rmse_knn(ones, X_tr, y_tr, X_te, y_te):.3f} | "
      f"GA-weighted kNN: {rmse_knn(best_w, X_tr, y_tr, X_te, y_te):.3f}")