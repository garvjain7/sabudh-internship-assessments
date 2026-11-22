import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
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
grids = {
    "Linear": (LinearRegression(), {}),
    "Lasso": (Lasso(max_iter=20000), {"model__alpha": [0.001, 0.01, 0.1, 0.5, 1, 5]}),
    "Ridge": (Ridge(), {"model__alpha": [0.01, 0.1, 1, 5, 10, 50]}),
    "KNN": (KNeighborsRegressor(), {
        "model__n_neighbors": [3, 5, 7, 9, 11],
        "model__weights": ["uniform", "distance"],
        "model__p": [1, 2],
    }),
    "SVR": (SVR(), {
        "model__kernel": ["rbf", "linear"],
        "model__C": [1, 10, 100, 1000],
        "model__epsilon": [0.1, 0.5, 1],
        "model__gamma": ["scale", 0.01, 0.1],
    }),
    "Tree": (DecisionTreeRegressor(random_state=42), {
        "model__max_depth": [3, 4, 5, 6, 8, None],
        "model__min_samples_leaf": [1, 2, 4, 8],
    }),
    "RandomForest": (RandomForestRegressor(random_state=42), {
        "model__n_estimators": [100, 300],
        "model__max_depth": [None, 6, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", 0.6, 1.0],
    }),
    "GradientBoosting": (GradientBoostingRegressor(random_state=42), {
        "model__n_estimators": [100, 300],
        "model__learning_rate": [0.03, 0.1],
        "model__max_depth": [2, 3, 4],
        "model__subsample": [0.7, 1.0],
    }),
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)
rows, best_params = [], {}
for name, (est, grid) in grids.items():
    pipe = Pipeline([("prep", prep), ("model", est)])
    gs = GridSearchCV(pipe, grid or {"model": [est]}, cv=cv, scoring="neg_root_mean_squared_error", n_jobs=-1)
    gs.fit(X_train, y_train)
    pred = gs.predict(X_test)
    best_params[name] = {k.replace("model__", ""): v for k, v in gs.best_params_.items() if k != "model"}
    rows.append({
        "model": name,
        "cv_RMSE": -gs.best_score_,
        "test_R2": r2_score(y_test, pred),
        "test_RMSE": np.sqrt(mean_squared_error(y_test, pred)),
        "test_MAE": mean_absolute_error(y_test, pred),
        "best_params": best_params[name],
    })

res = pd.DataFrame(rows).sort_values("cv_RMSE")
pd.set_option("display.max_colwidth", None, "display.width", 250)
print(res.round(3).to_string(index=False))
print(f"\nmost accurate (lowest CV RMSE): {res.iloc[0]['model']}")

with open("best_params.json", "w") as f:
    json.dump(best_params, f, indent=2)