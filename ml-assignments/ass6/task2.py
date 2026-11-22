import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
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
models = {
    "Linear": LinearRegression(),
    "Lasso": Lasso(),
    "Ridge": Ridge(),
    "KNN": KNeighborsRegressor(),
    "SVR": SVR(),
    "Tree": DecisionTreeRegressor(random_state=42),
    "RandomForest": RandomForestRegressor(random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
}

rows = []
for name, est in models.items():
    pipe = Pipeline([("prep", prep), ("model", est)]).fit(X_train, y_train)
    pred = pipe.predict(X_test)
    rows.append({
        "model": name,
        "R2": r2_score(y_test, pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, pred)),
        "MAE": mean_absolute_error(y_test, pred),
    })

print(pd.DataFrame(rows).sort_values("RMSE").round(3).to_string(index=False))