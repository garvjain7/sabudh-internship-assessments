from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from task1 import df

NUM = ["likes", "dislikes", "comment_count", "title_length", "days_since_publish"]
CAT = ["channel_title", "category_id"]

X = df[NUM + CAT]
X_train, X_test, yr_train, yr_test, yc_train, yc_test = train_test_split(
    X, df["views"], df["viral"], test_size=0.2, random_state=42, stratify=df["viral"])

# rare channels are grouped to avoid ~2000 one-hot columns; fit on train only
pre = ColumnTransformer([
    ("num", StandardScaler(), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=10), CAT)], sparse_threshold=0)
X_train_p = pre.fit_transform(X_train)
X_test_p = pre.transform(X_test)

if __name__ == "__main__":
    print(X_train_p.shape, X_test_p.shape)
    print(X_train_p[:, :len(NUM)].mean(axis=0).round(2), X_train_p[:, :len(NUM)].std(axis=0).round(2))