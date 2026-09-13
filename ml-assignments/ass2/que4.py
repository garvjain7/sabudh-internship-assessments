import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, k=1000, tau=1e-9, lam=0.01, reg_type=None, reg_strength=0.0):
    """
    Learn logistic regression coefficients using gradient descent.

    Parameters
    ----------
    X : np.ndarray, shape (n, m)
        Independent variables.
    y : np.ndarray, shape (n, 1)
        Binary output values.
    k : int
        Maximum number of gradient descent iterations.
    tau : float
        Stop early if the change in cost between iterations is below this.
    lam : float
        Learning rate.
    reg_type : str or None
        Type of regularization: None, "l1", or "l2".
    reg_strength : float
        Regularization constant.

    Returns
    -------
    beta : np.ndarray
        Learned coefficient vector.
    cost : float
        Final regularized cost.
    """
    n, m = X.shape
    X_b = np.column_stack((np.ones(n), X))
    beta = np.random.randn(m + 1, 1)

    def compute_cost(beta):
        p = np.clip(sigmoid(X_b @ beta), 1e-15, 1 - 1e-15)
        c = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
        beta_without_intercept = beta[1:]
        if reg_type == "l1":
            c += (reg_strength / n) * np.sum(np.abs(beta_without_intercept))
        elif reg_type == "l2":
            c += (reg_strength / (2 * n)) * np.sum(beta_without_intercept ** 2)
        return c

    cost_prev = compute_cost(beta)

    for _ in range(k):
        p = sigmoid(X_b @ beta)
        gradient = (X_b.T @ (p - y)) / n

        beta_without_intercept = beta.copy()
        beta_without_intercept[0] = 0

        if reg_type == "l1":
            gradient += (reg_strength / n) * np.sign(beta_without_intercept)
        elif reg_type == "l2":
            gradient += (reg_strength / n) * beta_without_intercept

        beta -= lam * gradient

        cost = compute_cost(beta)
        if abs(cost_prev - cost) < tau:
            cost_prev = cost
            break
        cost_prev = cost

    return beta, cost_prev


if __name__ == "__main__":
    np.random.seed(42)

    X = np.random.randn(200, 3)
    true_beta = np.array([[1.0], [-2.0], [1.5]])
    probabilities = sigmoid(X @ true_beta)
    y = (probabilities > 0.5).astype(int)

    beta_none, cost_none = logistic_regression(X, y, k=3000, tau=1e-9, lam=0.1, reg_type=None)
    beta_l1, cost_l1 = logistic_regression(X, y, k=3000, tau=1e-9, lam=0.1, reg_type="l1", reg_strength=0.1)
    beta_l2, cost_l2 = logistic_regression(X, y, k=3000, tau=1e-9, lam=0.1, reg_type="l2", reg_strength=0.1)

    print("Without regularization:")
    print("Beta:", beta_none.ravel())
    print("Cost:", cost_none)

    print("\nL1 regularization:")
    print("Beta:", beta_l1.ravel())
    print("Cost:", cost_l1)

    print("\nL2 regularization:")
    print("Beta:", beta_l2.ravel())
    print("Cost:", cost_l2)


# How does L1 and L2 regularization impact the models learned?
#
# L1 regularization adds a penalty based on the absolute values of the
# coefficients. It encourages some coefficients in the learned beta vector
# to become exactly zero. As a result, the model may effectively ignore some
# independent variables, making L1 useful for feature selection and producing
# a simpler model.
#
# L2 regularization adds a penalty based on the squared values of the
# coefficients. It reduces the magnitude of the learned coefficients and
# discourages very large beta values. Unlike L1 regularization, L2 generally
# does not make coefficients exactly zero, so all variables usually remain
# part of the model with reduced influence.
#
# Both L1 and L2 regularization can reduce overfitting by limiting the
# complexity of the learned model. L1 tends to produce sparse models, while
# L2 tends to produce models with smaller and more evenly distributed
# coefficient values.


# How does the choice of the regularization constant impact the beta vector learned?
#
# The regularization constant controls how strongly large coefficient values
# are penalized. When the regularization constant is close to zero, the model
# behaves similarly to ordinary logistic regression and the learned beta
# values are mainly determined by the training data.
#
# As the regularization constant increases, the penalty becomes stronger and
# the magnitude of the learned beta values generally decreases.
#
# For L1 regularization, increasing the regularization constant can cause more
# coefficients to become exactly zero. Therefore, a larger value can result in
# a beta vector with fewer non-zero coefficients.
#
# For L2 regularization, increasing the regularization constant shrinks the
# coefficients closer to zero, but they usually remain non-zero.
#
# If the regularization constant is too large, the coefficients may be shrunk
# too much and the model can underfit the data. Therefore, the value of the
# regularization constant must balance reducing overfitting with retaining
# enough information from the independent variables.