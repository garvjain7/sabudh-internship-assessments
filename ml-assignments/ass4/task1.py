import pandas as pd

URL = "https://raw.githubusercontent.com/123deepak/Kaggle-problems/refs/heads/master/USvideos.csv"
df = pd.read_csv(URL)
# one row per video: a video trends on several days and would leak across train/test
df = df.loc[df.groupby("video_id")["views"].idxmax()].reset_index(drop=True)
df["title_length"] = df["title"].str.len()
trend = pd.to_datetime(df["trending_date"], format="%y.%d.%m")
publish = pd.to_datetime(df["publish_time"]).dt.tz_localize(None).dt.normalize()
df["days_since_publish"] = (trend - publish).dt.days
# regression target: views | classification target: viral = views above the 75th percentile
df["viral"] = (df["views"] > df["views"].quantile(0.75)).astype(int)

if __name__ == "__main__":
    print(df.shape)
    print(df.head())
    df.info()
    print(df.describe())
    print(df["viral"].value_counts())