import numpy as np

def generate_dataset(theta, n, m, seed=None):
    """
    Generate a synthetic logistic-regression dataset with label noise:
        p(y=1|x) = 1 / (1 + exp(-x @ beta))
        y = 1{p > 0.5}, then each label flipped independently w.p. theta

    Parameters
    ----------
    theta : float
        Probability of flipping a generated label (0 <= theta <= 1).
    n : int
        Number of observations (n >= 1).
    m : int
        Number of independent variables (m >= 0).
    seed : int, optional
        Random seed, for reproducible output.

    Returns
    -------
    X : np.ndarray, shape (n, m+1)
        Design matrix; first column is all ones (x_i0 = 1).
    y : np.ndarray, shape (n, 1)
        Binary output values (0/1), possibly noisy.
    beta : np.ndarray, shape (m+1, 1)
        True coefficients used to generate y.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if not (0 <= theta <= 1):
        raise ValueError("theta must be in [0, 1]")

    rng = np.random.default_rng(seed)

    X = np.column_stack((np.ones(n), rng.standard_normal((n, m))))
    beta = rng.standard_normal((m + 1, 1))

    z = X @ beta
    p = 1.0 / (1.0 + np.exp(-z))
    y_clean = (p > 0.5).astype(int)

    flip = rng.binomial(1, theta, size=(n, 1)).astype(bool)
    y = np.where(flip, 1 - y_clean, y_clean)

    return X, y, beta


if __name__ == "__main__":
    X, y, beta = generate_dataset(theta=0.1, n=10, m=3)

    print(beta.ravel())
    print()
    print(f"{'x0':>6} {'x1':>8} {'x2':>8} {'x3':>8} | {'y':>3}")
    for row_x, row_y in zip(X, y):
        print(" ".join(f"{v:8.3f}" for v in row_x), "|", f"{row_y[0]:3d}")