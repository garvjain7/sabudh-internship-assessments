import numpy as np


class GradientDescentBase:
    """
    Shared batch gradient descent loop for linear/logistic regression.
    Subclasses only need to define _activation and _cost.
    """

    def __init__(self, k, tau, lam):
        self.k = k
        self.tau = tau
        self.lam = lam
        self.beta = None
        self.cost_ = None

    def _activation(self, z):
        raise NotImplementedError

    def _cost(self, p, y):
        raise NotImplementedError

    def fit(self, X, y):
        n, m = X.shape
        X_b = np.hstack((np.ones((n, 1)), X))  # add intercept column -> (n, m+1)

        beta = np.random.randn(m + 1, 1)
        cost_prev = self._cost(self._activation(X_b @ beta), y)

        for _ in range(self.k):
            error = self._activation(X_b @ beta) - y
            grad = (X_b.T @ error) / n
            beta = beta - self.lam * grad

            cost = self._cost(self._activation(X_b @ beta), y)
            if abs(cost_prev - cost) < self.tau:
                cost_prev = cost
                break
            cost_prev = cost

        self.beta = beta
        self.cost_ = cost_prev
        return beta, cost_prev

    def predict(self, X):
        n = X.shape[0]
        X_b = np.hstack((np.ones((n, 1)), X))
        return self._activation(X_b @ self.beta)


class LinearRegressionGD(GradientDescentBase):

    def _activation(self, z):
        return z

    def _cost(self, p, y):
        return np.mean((p - y) ** 2) / 2


class LogisticRegressionGD(GradientDescentBase):

    def _activation(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def _cost(self, p, y):
        eps = 1e-12
        p = np.clip(p, eps, 1 - eps)
        return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))


if __name__ == "__main__":
    X = np.random.randn(200, 3)
    y_lin = np.random.randn(200, 1)
    y_log = (np.random.rand(200, 1) > 0.5).astype(float)

    lin_model = LinearRegressionGD(k=2000, tau=1e-8, lam=0.1)
    beta, cost = lin_model.fit(X, y_lin)
    print("Linear regression")
    print("beta:", beta.ravel())
    print("cost:", cost)

    print()

    log_model = LogisticRegressionGD(k=2000, tau=1e-8, lam=0.1)
    beta, cost = log_model.fit(X, y_log)
    print("Logistic regression")
    print("beta:", beta.ravel())
    print("cost:", cost)    