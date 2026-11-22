import json
import joblib
import numpy as np
import pandas as pd
from scipy.stats import ttest_rel
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RepeatedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

DATA = "epldata_final.csv"
NUM = ["age", "page_views", "fpl_value", "fpl_sel", "fpl_points", "age_cat"]
CAT = ["position_cat", "region"]
BIN = ["new_foreign", "big_club", "new_signing"]
FEATURES = NUM + CAT + BIN
TARGET = "market_value"

df = pd.read_csv(DATA)
df["region"] = df["region"].fillna(4)  # one missing region (Benin -> Rest of World)
df["fpl_sel"] = df["fpl_sel"].astype(str).str.rstrip("%").astype(float)
X, y = df[FEATURES], df[TARGET]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

prep = ColumnTransformer(
    [("num", StandardScaler(), NUM), ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)],
    remainder="passthrough",
)
base = {
    "Linear": LinearRegression(), "Lasso": Lasso(max_iter=20000), "Ridge": Ridge(),
    "KNN": KNeighborsRegressor(), "SVR": SVR(), "Tree": DecisionTreeRegressor(random_state=42),
    "RandomForest": RandomForestRegressor(random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
}
try:
    with open("best_params.json") as f:  # produced by task3_tuning.py
        tuned = json.load(f)
except FileNotFoundError:
    tuned = {}


def build(name):
    return Pipeline([("prep", prep), ("model", base[name].set_params(**tuned.get(name, {})))])


# repeated 5-fold CV on the training set, identical folds for every model
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
scores = {n: -cross_val_score(build(n), X_train, y_train, cv=cv, scoring="neg_root_mean_squared_error", n_jobs=-1)
          for n in base}
table = pd.DataFrame({
    "cv_RMSE_mean": {n: s.mean() for n, s in scores.items()},
    "cv_RMSE_std": {n: s.std() for n, s in scores.items()},
}).sort_values("cv_RMSE_mean")
print(table.round(3).to_string())

# paired t-test on matched folds: best vs runner-up
best, second = table.index[0], table.index[1]
t, p = ttest_rel(scores[best], scores[second])
print(f"\npaired t-test {best} vs {second}: t={t:.2f}, p={p:.4f}")

chosen = best  # lowest mean CV RMSE

# held-out test check of the chosen model, then refit on all data for deployment
final = build(chosen).fit(X_train, y_train)
pred = final.predict(X_test)
print(f"\nchosen = {chosen}: test R2={r2_score(y_test, pred):.3f}, "
      f"RMSE={np.sqrt(mean_squared_error(y_test, pred)):.3f}, MAE={mean_absolute_error(y_test, pred):.3f}")

joblib.dump({"model": build(chosen).fit(X, y), "features": FEATURES, "name": chosen}, "best_model.joblib")