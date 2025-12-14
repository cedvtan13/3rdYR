import numpy as np

def gaussian_elimination(A, b):
    """Solve the system of equations Ax = b using Gaussian elimination."""
    A = np.array(A, float)
    b = np.array(b, float)
    n = len(b)

    # Forward elimination
    for i in range(n):
        # Make the diagonal contain all 1s
        A[i] = A[i] / A[i][i]
        b[i] = b[i] / A[i][i]
        
        for j in range(i + 1, n):
            factor = A[j][i]
            A[j] = A[j] - factor * A[i]
            b[j] = b[j] - factor * b[i]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = b[i] - np.dot(A[i][i + 1:], x[i + 1:])
    
    return x

def ordinary_least_squares(X, y):
    """Perform Ordinary Least Squares regression."""
    X = np.array(X)
    y = np.array(y)
    beta = np.linalg.inv(X.T @ X) @ X.T @ y
    return beta

def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    """Perform Gradient Descent regression."""
    X = np.array(X)
    y = np.array(y)
    m, n = X.shape
    beta = np.zeros(n)
    
    for _ in range(iterations):
        predictions = X @ beta
        errors = predictions - y
        gradient = (1/m) * (X.T @ errors)
        beta -= learning_rate * gradient
    
    return beta

def numerical_differentiation(func, x, method='central', h=1e-5):
    """Calculate the derivative of a function at a point x using numerical differentiation."""
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
    A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b = [8, -11, -3]
    solution = gaussian_elimination(A, b)
    print("Solution of Ax = b:", solution)

    # Regression Algorithms
    print("\nRegression Algorithms:")
    X = [[1, 1], [1, 2], [2, 2], [2, 3]]
    y = [1, 2, 2, 3]
    
    ols_beta = ordinary_least_squares(X, y)
    print("Ordinary Least Squares coefficients:", ols_beta)

    gd_beta = gradient_descent(np.array(X), np.array(y))
    print("Gradient Descent coefficients:", gd_beta)

    # Numerical Differentiation
    print("\nNumerical Differentiation:")
    func = lambda x: x**2
    x = 2.0
    print("Forward Difference:", numerical_differentiation(func, x, method='forward'))
    print("Backward Difference:", numerical_differentiation(func, x, method='backward'))
    print("Central Difference:", numerical_differentiation(func, x, method='central'))

if __name__ == "__main__":
    main()