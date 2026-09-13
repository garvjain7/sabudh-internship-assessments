import numpy as np


def generate_dataset(theta, n, m, seed=None):
    """
    p(y=1|x) = 1 / (1 + exp(-x @ beta))
    y = 1 if p > 0.5 else 0, then flipped w.p. theta
    """
    rng = np.random.default_rng(seed)
    X = np.column_stack((np.ones(n), rng.standard_normal((n, m))))
    beta = rng.standard_normal((m + 1, 1))
    z = X @ beta
    p = 1.0 / (1.0 + np.exp(-z))
    y_clean = (p > 0.5).astype(int)
    flip = rng.binomial(1, theta, size=(n, 1)).astype(bool)
    y = np.where(flip, 1 - y_clean, y_clean)
    return X, y, beta


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def gradient_descent(X, y, k, tau, lam):
    """
    Batch gradient descent minimizing the logistic regression cross-entropy
    cost. X here already includes the intercept column.
    """
    n = X.shape[0]
    beta = np.random.randn(X.shape[1], 1)
    eps = 1e-12
    p = np.clip(sigmoid(X @ beta), eps, 1 - eps)
    cost_prev = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

    for _ in range(k):
        error = sigmoid(X @ beta) - y
        grad = (X.T @ error) / n
        beta = beta - lam * grad

        p = np.clip(sigmoid(X @ beta), eps, 1 - eps)
        cost = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        if abs(cost_prev - cost) < tau:
            cost_prev = cost
            break
        cost_prev = cost

    return beta, cost_prev


# --- experiment ---
m = 3
TRIALS = 10
K = 5000
TAU = 1e-10
LAM = 0.3

n_values = [20, 50, 200, 1000, 5000]
theta_values = [0.0, 0.1, 0.25, 0.4, 0.5]

results = {}
seed_counter = 0
for n in n_values:
    for theta in theta_values:
        errors = []
        for trial in range(TRIALS):
            seed_counter += 1
            X, y, beta_true = generate_dataset(theta, n, m, seed=seed_counter)
            np.random.seed(seed_counter)
            beta_hat, cost = gradient_descent(X, y, k=K, tau=TAU, lam=LAM)
            errors.append(np.linalg.norm(beta_hat - beta_true))
        results[(n, theta)] = float(np.mean(errors))

print(f"{'n':>6} |" + "".join(f" theta={t:<6}" for t in theta_values))
for n in n_values:
    row = " ".join(f"{results[(n, t)]:11.4f}" for t in theta_values)
    print(f"{n:>6} | {row}")


# How do n and theta affect the recovery of beta?
#
# For each (n, theta) pair I ran 10 trials with different random seeds
# and averaged the error, since a single run is just one noisy draw,
# especially when n is small. m was kept fixed at 3 so only n and theta
# are changing.
#
# theta=0 looks broken but isn't -- with no noise the classes are
# perfectly separable, so logistic regression has no finite solution
# and beta just keeps growing. Checked directly at n=200: gradient
# descent used all 5000 iterations, never hit tau, and beta's norm
# ended up ~15 vs the true ~2. Diverging, not a bug.
#
# For theta > 0, more data helps a lot at first then levels off. At
# theta=0.1, error drops from 5.31 (n=20) to 0.55 (n=5000), but most of
# that gain happens by n=200-1000.
#
# theta matters too, and more noise hurts more as it goes up. At
# n=1000, error goes from 0.59 (theta=0.1) to 1.83 (theta=0.5) -- makes
# sense, more flipped labels means less real signal. At theta=0.5 a
# label is basically a coin toss, so more data barely helps there
# (2.63 -> 2.06 from n=20 to n=5000, vs 5.31 -> 0.55 at theta=0.1).
#
# The two interact: small + noisy (n=20, theta=0.4) is one of the worst
# cases tested, and even n=5000 can't fully beat heavy noise (error
# 2.06 at theta=0.5 vs 0.55 at theta=0.1). More data reduces randomness
# in the estimate but can't undo information the noise destroyed.
#
# So: more n helps and then plateaus, more noise hurts and more data
# can't fully fix it, and no noise at all breaks convergence entirely.
#
#
# ===========================================================
# DERIVATION OF THE PARTIAL DERIVATIVE
# ===========================================================
#
# The logistic regression cost function is:
#
# J(beta) = -(1/n) * sum_i [ y_i log(p_i) + (1-y_i) log(1-p_i) ]
#
# where p_i = sigmoid(z_i), z_i = x_i . beta
#
# Work with a single observation first, then average.
#
# Step 1: differentiate the per-example loss w.r.t. p_i.
#
# J_i = -[y_i log(p_i) + (1-y_i) log(1-p_i)]
#
# dJ_i/dp_i = -y_i/p_i + (1-y_i)/(1-p_i)
#           = (p_i - y_i) / [p_i(1-p_i)]
#
# Step 2: differentiate the sigmoid w.r.t. its input.
#
# p_i = 1 / (1 + exp(-z_i))
#
# dp_i/dz_i = p_i(1-p_i)      (standard result of the quotient rule)
#
# Step 3: chain rule to get dJ_i/dz_i.
#
# dJ_i/dz_i = (dJ_i/dp_i) * (dp_i/dz_i)
#           = [(p_i-y_i)/(p_i(1-p_i))] * [p_i(1-p_i)]
#           = p_i - y_i
#
# The p_i(1-p_i) terms cancel exactly -- this is why logistic
# regression's gradient ends up as simple as linear regression's,
# despite the sigmoid in between.
#
# Step 4: differentiate z_i w.r.t. beta_j.
#
# z_i = x_i . beta = sum_k x_ik * beta_k
# dz_i/d(beta_j) = x_ij
#
# Step 5: chain rule, then average over n examples.
#
# dJ_i/d(beta_j) = (p_i - y_i) * x_ij
#
# dJ/d(beta_j) = (1/n) * sum_i (p_i - y_i) * x_ij
#
# In matrix form:
#
# Gradient = (1/n) * X.T @ (p - y)
#
# which gives the gradient descent update used throughout:
#
# beta = beta - lam * Gradient