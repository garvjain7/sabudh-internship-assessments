import numpy as np


def gradient_descent(X, y, k, tau, lam):
    """
    Learn linear regression coefficients via batch gradient descent.

    Minimizes J(beta) = (1/2n) * ||X_b @ beta - y||^2
    using the update rule: beta <- beta - lam * grad,
    where grad = (1/n) * X_b.T @ (X_b @ beta - y).

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
    cost_prev = np.mean((X_b @ beta - y) ** 2) / 2

    for _ in range(k):
        error = X_b @ beta - y
        grad = (X_b.T @ error) / n
        beta = beta - lam * grad

        cost = np.mean((X_b @ beta - y) ** 2) / 2
        if abs(cost_prev - cost) < tau:
            cost_prev = cost
            break
        cost_prev = cost

    return beta, cost_prev

if __name__ == "__main__":
    X = np.random.randn(200, 3)
    y = np.random.randn(200, 1)

    beta, cost = gradient_descent(X, y, k=2000, tau=1e-8, lam=0.1)

    print("beta:", beta.ravel())
    print("cost:", cost)
