from scipy import stats

from task1 import df

# H0: mean views of high-feature videos <= low-feature videos; H1: high > low (split at median)
for c in ["likes", "dislikes", "comment_count"]:
    m = df[c].median()
    t, p = stats.ttest_ind(df.loc[df[c] > m, "views"], df.loc[df[c] <= m, "views"],
                           equal_var=False, alternative="greater")
    print(f"{c}: p-value = {p:.3g} -> {'reject H0' if p < 0.05 else 'fail to reject H0'}")

# all three p-values are far below 0.05: reject H0, hypothesis supported for likes, dislikes and comment_count
# the test shows association with views, not causation