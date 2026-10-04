import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

from task1 import df
from task4 import CAT, NUM, X


def pre(scaler):
    return ColumnTransformer([
        ("num", scaler, NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=10), CAT)], sparse_threshold=0)


kf = KFold(5, shuffle=True, random_state=42)
skf = StratifiedKFold(5, shuffle=True, random_state=42)

for name, scaler in [("StandardScaler", StandardScaler()), ("MinMaxScaler", MinMaxScaler())]:
    lin = cross_val_score(make_pipeline(pre(scaler), LinearRegression()), X, df["views"], cv=kf, scoring="r2")
    log = cross_val_score(make_pipeline(pre(scaler), LogisticRegression(max_iter=1000)), X, df["viral"],
                          cv=skf, scoring="roc_auc")
    print(f"{name}: LinReg R2 mean={lin.mean():.4f} var={lin.var():.4g} | "
          f"LogReg ROC-AUC mean={log.mean():.4f} var={log.var():.4g}")

pipe = make_pipeline(pre(StandardScaler()), LogisticRegression(max_iter=1000)).fit(X, df["viral"])
coef = pd.Series(pipe[-1].coef_[0], index=pipe[0].get_feature_names_out()).sort_values(key=abs).tail(15)
coef.plot.barh()
plt.xlabel("logistic coefficient")
plt.tight_layout()
plt.show()

# LinReg R2 is identical for both scalers (OLS is invariant to linear scaling); fold variance comes from outlier videos
# LogReg ROC-AUC: StandardScaler 0.948 vs MinMaxScaler 0.807
# MinMax squeezes outlier-heavy features (likes, dislikes) into a tiny range and L2 regularization shrinks them: use StandardScaler
# likes and dislikes are the strongest viral predictors, same as Task 6