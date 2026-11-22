import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

DATA = "epldata_final.csv"
OUT = "plots"
os.makedirs(OUT, exist_ok=True)
sns.set_theme(style="whitegrid")

df = pd.read_csv(DATA)
df["region"] = df["region"].fillna(4)  # one missing region (Benin -> Rest of World)
df["fpl_sel"] = df["fpl_sel"].astype(str).str.rstrip("%").astype(float)
df["position_name"] = df["position_cat"].map({1: "Attacker", 2: "Midfielder", 3: "Defender", 4: "Goalkeeper"})
df["region_name"] = df["region"].map({1: "England", 2: "EU", 3: "Americas", 4: "Rest of World"})
num = df.select_dtypes("number").drop(columns=["club_id"])


def save(name):
    plt.tight_layout()
    plt.savefig(f"{OUT}/{name}.png", dpi=120)
    plt.close()


# 1. target distribution
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(df["market_value"], kde=True, ax=ax[0])
sns.histplot(np.log1p(df["market_value"]), kde=True, ax=ax[1])
ax[1].set_xlabel("log(market_value + 1)")
save("01_target_distribution")

# 2. market value by category
fig, ax = plt.subplots(2, 2, figsize=(12, 9))
sns.boxplot(data=df, x="position_name", y="market_value", ax=ax[0, 0])
sns.boxplot(data=df, x="big_club", y="market_value", ax=ax[0, 1])
sns.boxplot(data=df, x="region_name", y="market_value", ax=ax[1, 0])
sns.boxplot(data=df, x="age_cat", y="market_value", ax=ax[1, 1])
save("02_value_by_category")

# 3. numeric drivers of value
fig, ax = plt.subplots(2, 2, figsize=(12, 9))
sns.scatterplot(data=df, x="page_views", y="market_value", hue="big_club", ax=ax[0, 0])
sns.scatterplot(data=df, x="fpl_value", y="market_value", hue="position_name", ax=ax[0, 1])
sns.scatterplot(data=df, x="fpl_points", y="market_value", hue="big_club", ax=ax[1, 0])
sns.scatterplot(data=df, x="age", y="market_value", hue="position_name", ax=ax[1, 1])
save("03_numeric_drivers")

# 4. correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
save("04_correlation_heatmap")

# 5. club level view
order = df.groupby("club")["market_value"].mean().sort_values(ascending=False).index
plt.figure(figsize=(10, 5))
sns.barplot(data=df, x="club", y="market_value", order=order, errorbar=None)
plt.xticks(rotation=60, ha="right")
save("05_club_mean_value")

# 6. pairplot of key variables
sns.pairplot(df[["market_value", "page_views", "fpl_value", "fpl_points", "age", "big_club"]], hue="big_club", corner=True)
plt.savefig(f"{OUT}/06_pairplot.png", dpi=100)
plt.close()

# findings computed from the data
corr = num.corr()["market_value"].drop("market_value").sort_values(key=abs, ascending=False)
print(f"rows={len(df)}, clubs={df['club'].nunique()}, missing={int(df.isna().sum().sum())}")
print(f"market_value: mean={df.market_value.mean():.2f}, median={df.market_value.median():.2f}, "
      f"max={df.market_value.max():.1f}, skew={df.market_value.skew():.2f}")
print("\nTop correlations with market_value:")
print(corr.head(6).round(3).to_string())
print("\nMean value by position:")
print(df.groupby("position_name")["market_value"].mean().round(2).to_string())
print("\nMean value big club vs rest:")
print(df.groupby("big_club")["market_value"].mean().round(2).to_string())
print("\nMean value by region:")
print(df.groupby("region_name")["market_value"].mean().round(2).to_string())
print("\nMean value by age group:")
print(df.groupby("age_cat")["market_value"].mean().round(2).to_string())
print("\nTop 5 players by value:")
print(df.nlargest(5, "market_value")[["name", "club", "market_value", "page_views"]].to_string(index=False))
print(f"\nplots saved in ./{OUT}/")