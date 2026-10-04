import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score, f1_score,
                             precision_score, recall_score, roc_auc_score)

from task4 import X_test_p, X_train_p, pre, yc_test, yc_train

model = LogisticRegression(max_iter=1000).fit(X_train_p, yc_train)
pred = model.predict(X_test_p)
proba = model.predict_proba(X_test_p)[:, 1]

print(f"Accuracy: {accuracy_score(yc_test, pred):.4f}")
print(f"Precision: {precision_score(yc_test, pred):.4f}")
print(f"Recall: {recall_score(yc_test, pred):.4f}")
print(f"F1: {f1_score(yc_test, pred):.4f}")
print(f"ROC-AUC: {roc_auc_score(yc_test, proba):.4f}")

ConfusionMatrixDisplay.from_predictions(yc_test, pred)
plt.show()
RocCurveDisplay.from_predictions(yc_test, proba)
plt.show()

coef = pd.Series(model.coef_[0], index=pre.get_feature_names_out()).sort_values(key=abs, ascending=False)
print(coef.head(5).round(3))

# likes (+9.43) and dislikes (+3.73) dominate virality; channel effects follow (Warner Bros. +2.11, IISuperwomanII -2.17)
# comment_count, title_length and days_since_publish are small (|coef| < 0.5)
# recall (0.72) is lower than precision (0.91): ~28% of viral videos are missed at the 0.5 threshold