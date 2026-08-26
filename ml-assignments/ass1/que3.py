"""
Investigation: how do n (sample size) and sigma (noise level) affect
gradient descent's ability to recover the true beta used to generate
a synthetic dataset?

Self-contained: data generation and gradient descent are both defined
here directly, not imported from elsewhere.

Method
------
For each (n, sigma) combination:
  1. Generate a synthetic dataset with a known true beta.
  2. Run gradient descent on it to get beta_hat.
  3. Measure recovery error = ||beta_hat - beta_true||.
  4. Repeat across several random seeds and average, since a single
     run is one noisy draw -- especially at small n.
m is held fixed throughout so n and sigma are the only variables
being studied.
"""
import numpy as np


def make_dataset(sigma, n, m, seed):
    """Generate y = X @ beta + e, with an intercept column in X."""
    rng = np.random.default_rng(seed)
    X = np.column_stack((np.ones(n), rng.standard_normal((n, m))))
    beta = rng.standard_normal((m + 1, 1))
    e = rng.normal(0, sigma, size=(n, 1))
    y = X @ beta + e
    return X, y, beta


def gradient_descent(X, y, k, tau, lam):
    """Batch gradient descent minimizing J(beta) = (1/2n)||X@beta - y||^2.
    X here already includes the intercept column."""
    n = X.shape[0]
    beta = np.random.randn(X.shape[1], 1)
    cost_prev = np.mean((X @ beta - y) ** 2) / 2

    for _ in range(k):
        error = X @ beta - y
        grad = (X.T @ error) / n
        beta = beta - lam * grad

        cost = np.mean((X @ beta - y) ** 2) / 2
        if abs(cost_prev - cost) < tau:
            cost_prev = cost
            break
        cost_prev = cost

    return beta, cost_prev


# --- experiment ---
m = 3
TRIALS = 8
K = 5000
TAU = 1e-12
LAM = 0.1

n_values = [10, 50, 200, 1000, 5000, 20000]
sigma_values = [0.1, 1, 5, 15, 40]

results = {}
seed_counter = 0
for n in n_values:
    for sigma in sigma_values:
        errors = []
        for trial in range(TRIALS):
            seed_counter += 1
            X, y, beta_true = make_dataset(sigma, n, m, seed=seed_counter)
            beta_hat, cost = gradient_descent(X, y, k=K, tau=TAU, lam=LAM)
            errors.append(np.linalg.norm(beta_hat - beta_true))
        results[(n, sigma)] = float(np.mean(errors))

# --- print results table ---
print(f"{'n':>7} |" + "".join(f" sigma={s:<6}" for s in sigma_values))
for n in n_values:
    row = " ".join(f"{results[(n, s)]:10.4f}" for s in sigma_values)
    print(f"{n:>7} | {row}")

# --- verification: check against theory (error ~ sigma * sqrt((m+1)/n)) ---
print("\nVerification: empirical error / theoretical prediction (should hover near 1)")
for n in n_values:
    row = " ".join(
        f"{results[(n, s)] / (s * np.sqrt((m + 1) / n)):10.3f}" for s in sigma_values
    )
    print(f"{n:>7} | {row}")


# Report
'''
Effect of Sample Size (\(n\)) and Noise Level (\(\sigma\)) on Learning \(\beta\)
Objective

This experiment investigates how the number of observations (\(n\)) and the level of Gaussian noise (\(\sigma\)) affect the ability of Gradient Descent-based linear regression to recover the true coefficient vector, \(\beta\), used to generate the dataset.

For each combination of \(n\) and \(\sigma\), a synthetic dataset with known coefficients was generated. Gradient Descent was then used to estimate the coefficients, and the recovery error was measured as:

$$ \|\hat{\beta}-\beta\| $$

Each experiment was repeated multiple times, and the average error was used to reduce the effect of random variation.

Results and Analysis

The results showed a clear relationship between both variables and coefficient recovery. Increasing the sample size generally reduced the error between the learned and true coefficients. With more observations, the model has more information about the underlying linear relationship, reducing the influence of random variations in individual samples.

Increasing the noise level had the opposite effect. Higher values of \(\sigma\) produced larger coefficient recovery errors because the output variable contained more unexplained random variation. The effect was particularly significant when the sample size was small.

The results also demonstrated an interaction between the two factors. Large datasets were able to achieve relatively accurate coefficient estimates even under high noise levels, whereas a combination of small sample size and high noise resulted in poor recovery of the true coefficients.

Conclusion

Both \(n\) and \(\sigma\) significantly affect the ability of linear regression to learn the true coefficients. Increasing the sample size improves coefficient recovery, while increasing the noise level makes it more difficult. A larger dataset can help reduce the impact of noise, but accurate learning ultimately depends on having sufficient data relative to the amount of variation present in the output.
'''