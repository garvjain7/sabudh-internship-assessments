import numpy as np

def generate_dataset(sigma, n, m, seed=None):
    """
    Generate a synthetic linear-regression dataset:
        y = X @ beta + e,   e ~ N(0, sigma^2)

    Parameters
    ----------
    sigma : float
        Standard deviation of the Gaussian noise.
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
        Output values.
    beta : np.ndarray, shape (m+1, 1)
        True coefficients used to generate y.
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    rng = np.random.default_rng(seed)

    X = np.column_stack((np.ones(n), rng.standard_normal((n, m))))
    beta = rng.standard_normal((m + 1, 1))
    e = rng.normal(0, sigma, size=(n, 1))
    y = X @ beta + e

    return X, y, beta

if __name__ == "__main__":
    X, y, beta = generate_dataset(sigma=1.0, n=10, m=3)

    print(beta.ravel())
    print()
    print(f"{'x0':>6} {'x1':>8} {'x2':>8} {'x3':>8} | {'y':>8}")
    for row_x, row_y in zip(X, y):
        print(" ".join(f"{v:8.3f}" for v in row_x), "|", f"{row_y[0]:8.3f}")
