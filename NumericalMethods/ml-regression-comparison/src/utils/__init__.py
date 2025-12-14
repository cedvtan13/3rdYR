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
    
    while True:
        print("\nChoose an option:")
        print("1. Solve a system of equations using Gaussian Elimination")
        print("2. Compare regression algorithms")
        print("3. Numerical Differentiation")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            # Example for Gaussian Elimination
            A = np.array([[3, 2, -4], [2, 3, 3], [5, -3, 1]], dtype=float)
            b = np.array([3, 15, 14], dtype=float)
            solution = gaussian_elimination(A, b)
            print("Solution:", solution)
        
        elif choice == '2':
            # Example for regression algorithms
            X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]], dtype=float)
            y = np.array([1, 2, 2, 3], dtype=float)
            
            print("1. Ordinary Least Squares")
            print("2. Gradient Descent")
            reg_choice = input("Choose regression method (1-2): ")
            
            if reg_choice == '1':
                beta = ordinary_least_squares(X, y)
                print("OLS Coefficients:", beta)
            elif reg_choice == '2':
                beta = gradient_descent(X, y)
                print("Gradient Descent Coefficients:", beta)
            else:
                print("Invalid choice.")
        
        elif choice == '3':
            # Example for Numerical Differentiation
            func = lambda x: x**2  # Example function
            x = float(input("Enter the point to differentiate at: "))
            print("1. Forward")
            print("2. Backward")
            print("3. Central")
            diff_choice = input("Choose differentiation method (1-3): ")
            
            if diff_choice == '1':
                derivative = numerical_differentiation(func, x, method='forward')
            elif diff_choice == '2':
                derivative = numerical_differentiation(func, x, method='backward')
            elif diff_choice == '3':
                derivative = numerical_differentiation(func, x, method='central')
            else:
                print("Invalid choice.")
                continue
            
            print(f"Derivative at x={x}: {derivative}")
        
        elif choice == '4':
            print("Exiting the application.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()