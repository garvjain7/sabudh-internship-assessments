import numpy as np


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def gradient_descent(X, y, k, tau, lam):
    """
    Learn logistic regression coefficients via batch gradient descent.

    Minimizes J(beta) = -(1/n) * sum(y*log(p) + (1-y)*log(1-p)), p = sigmoid(X_b @ beta)
    using the update rule: beta <- beta - lam * grad,
    where grad = (1/n) * X_b.T @ (p - y).

    Parameters
    ----------
    X : np.ndarray, shape (n, m)
    y : np.ndarray, shape (n, 1)
    k : int      -- max number of iterations
    tau : float  -- stop early if |cost_prev - cost| < tau
    lam : float  -- learning rate

    Returns
    -------
    beta : np.ndarray, shape (m+1, 1)
    cost : float -- final value of J(beta)
    """
    n, m = X.shape
    X_b = np.hstack((np.ones((n, 1)), X))  # add intercept column -> (n, m+1)

    beta = np.random.randn(m + 1, 1)

    eps = 1e-12  # avoid log(0)
    p = sigmoid(X_b @ beta)
    p = np.clip(p, eps, 1 - eps)
    cost_prev = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

    for _ in range(k):
        error = sigmoid(X_b @ beta) - y
        grad = (X_b.T @ error) / n
        beta = beta - lam * grad

        p = sigmoid(X_b @ beta)
        p = np.clip(p, eps, 1 - eps)
        cost = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

        if abs(cost_prev - cost) < tau:
            cost_prev = cost
            break
        cost_prev = cost

    return beta, cost_prev


if __name__ == "__main__":
    X = np.random.randn(200, 3)
    y = (np.random.rand(200, 1) > 0.5).astype(float)

    beta, cost = gradient_descent(X, y, k=2000, tau=1e-8, lam=0.1)

    print("beta:", beta.ravel())
    print("cost:", cost)