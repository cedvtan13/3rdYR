import numpy as np

def gaussian_elimination(A, b):
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

def linear_regression(X, y):
    # Analytical solution using Normal Equation
    X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Add bias term
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    return theta_best

def gradient_descent(X, y, learning_rate=0.01, n_iterations=1000):
    m = len(y)
    X_b = np.c_[np.ones((m, 1)), X]  # Add bias term
    theta = np.random.randn(X_b.shape[1])  # Random initialization
    
    for iteration in range(n_iterations):
        gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
        theta -= learning_rate * gradients
        
    return theta

def numerical_differentiation(func, x, method='central', h=1e-5):
    if method == 'forward':
        return (func(x + h) - func(x)) / h
    elif method == 'backward':
        return (func(x) - func(x - h)) / h
    elif method == 'central':
        return (func(x + h) - func(x - h)) / (2 * h)
    else:
        raise ValueError("Unknown method: choose 'forward', 'backward', or 'central'.")

def main():
    print("Welcome to the Machine Learning Library Comparison Tool!")
    
    while True:
        print("\nChoose an option:")
        print("1. Gaussian Elimination")
        print("2. Linear Regression (Analytical)")
        print("3. Linear Regression (Gradient Descent)")
        print("4. Numerical Differentiation")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("Enter the coefficients of the equations (up to 5 unknowns):")
            A = []
            for i in range(5):
                row = list(map(float, input(f"Row {i + 1}: ").split()))
                A.append(row)
            b = list(map(float, input("Enter the constants: ").split()))
            solution = gaussian_elimination(np.array(A), np.array(b))
            print("Solution:", solution)
        
        elif choice == '2':
            X = np.array([[1], [2], [3]])  # Example data
            y = np.array([1, 2, 3])  # Example target
            theta = linear_regression(X, y)
            print("Theta (Analytical):", theta)
        
        elif choice == '3':
            X = np.array([[1], [2], [3]])  # Example data
            y = np.array([1, 2, 3])  # Example target
            theta = gradient_descent(X, y)
            print("Theta (Gradient Descent):", theta)
        
        elif choice == '4':
            func = lambda x: x**2  # Example function
            x = float(input("Enter the point to differentiate at: "))
            method = input("Choose differentiation method (forward/backward/central): ")
            derivative = numerical_differentiation(func, x, method)
            print(f"Derivative at x={x} using {method} method:", derivative)
        
        elif choice == '5':
            print("Exiting the application.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()