import matplotlib.pyplot as plt
import seaborn as sns

from task1 import df

sns.histplot(df["views"], bins=50, log_scale=True)
plt.show()

plt.scatter(df["likes"], df["views"], s=5, alpha=0.4)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("likes")
plt.ylabel("views")
plt.show()

# duration is not in USvideos.csv, so it is excluded
cols = ["views", "likes", "dislikes", "comment_count", "title_length", "days_since_publish"]
corr = df[cols].corr()
print(corr.round(2))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.show()

# views are heavily right-skewed (median 5.2e5, max 2.3e8), hence the log axes
# likes vs views: strong positive correlation (r=0.83); comment_count moderate (0.57), dislikes weaker (0.44)
# likes, comment_count and dislikes are strongly correlated with each other (0.73-0.77)
# title_length and days_since_publish are almost uncorrelated with views (r=-0.04, -0.02)