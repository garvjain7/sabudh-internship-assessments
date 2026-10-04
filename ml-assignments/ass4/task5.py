import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from task4 import X_test_p, X_train_p, pre, yr_test, yr_train

model = LinearRegression().fit(X_train_p, yr_train)
pred = model.predict(X_test_p)

mse = mean_squared_error(yr_test, pred)
print(f"MSE: {mse:.3e}")
print(f"RMSE: {np.sqrt(mse):.3e}")
print(f"MAE: {mean_absolute_error(yr_test, pred):.3e}")
print(f"R2: {r2_score(yr_test, pred):.4f}")

coef = pd.Series(model.coef_, index=pre.get_feature_names_out()).sort_values(key=abs).tail(15)
coef.plot.barh()
plt.xlabel("coefficient")
plt.tight_layout()
plt.show()

# R2=0.77: the model explains most of the variance; RMSE (3.2e6) is large vs median views (5.2e5) due to extreme outliers
# likes has the largest coefficient (+7.5e6 per std), then dislikes (+3.1e6)
# comment_count is negative (-3.7e6) because it is collinear with likes (r=0.77)
# next are channel dummies (Universal Pictures, AsapSCIENCE, Marvel); title_length and days_since_publish are negligible