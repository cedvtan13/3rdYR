import numpy as np

def gaussian_elimination(A, b):
    """Solve the system of equations Ax = b using Gaussian elimination."""
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Make the diagonal contain all 1s
        factor = A[i][i]
        for j in range(i, n):
            A[i][j] /= factor
        b[i] /= factor
        
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    
    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = b[i] - np.dot(A[i][i + 1:], x[i + 1:])
    
    return x

def ordinary_least_squares(X, y):
    """Perform Ordinary Least Squares regression."""
    X_transpose = np.transpose(X)
    beta = np.linalg.inv(X_transpose @ X) @ X_transpose @ y
    return beta

def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    """Perform Gradient Descent regression."""
    m, n = X.shape
    beta = np.zeros(n)
    for _ in range(iterations):
        predictions = X @ beta
        errors = predictions - y
        gradient = (1/m) * (X.T @ errors)
        beta -= learning_rate * gradient
    return beta

def numerical_differentiation(func, x, method='central', h=1e-5):
    """Calculate the derivative of a function at a point x using the specified method."""
    if method == 'forward':
        return (func(x + h) - func(x)) / h
    elif method == 'backward':
        return (func(x) - func(x - h)) / h
    elif method == 'central':
        return (func(x + h) - func(x - h)) / (2 * h)
    else:
        raise ValueError("Invalid method. Choose 'forward', 'backward', or 'central'.")

def main():
    print("Welcome to the Machine Learning Library Comparison Tool!")
    
    # Gaussian Elimination
    print("\nGaussian Elimination:")
    A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
    b = np.array([8, -11, -3], dtype=float)
    solution = gaussian_elimination(A, b)
    print("Solution to Ax = b:", solution)

    # Regression Algorithms
    print("\nRegression Algorithms:")
    X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]], dtype=float)
    y = np.array([1, 2, 2, 3], dtype=float)

    ols_beta = ordinary_least_squares(X, y)
    print("Ordinary Least Squares coefficients:", ols_beta)

    gd_beta = gradient_descent(X, y)
    print("Gradient Descent coefficients:", gd_beta)

    # Numerical Differentiation
    print("\nNumerical Differentiation:")
    func = lambda x: x**2  # Example function
    x_point = 2
    method = input("Choose differentiation method (forward/backward/central): ")
    derivative = numerical_differentiation(func, x_point, method)
    print(f"The derivative of f(x) at x={x_point} using {method} method is:", derivative)

if __name__ == "__main__":
    main()