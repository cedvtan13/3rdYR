import numpy as np

def gaussian_elimination(A, b):
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Make the diagonal contain all 1's
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
    X_transpose = np.transpose(X)
    beta = np.linalg.inv(X_transpose @ X) @ X_transpose @ y
    return beta

def gradient_descent(X, y, learning_rate=0.01, iterations=1000):
    m, n = X.shape
    beta = np.zeros(n)
    for _ in range(iterations):
        predictions = X @ beta
        errors = predictions - y
        gradient = (1/m) * (X.T @ errors)
        beta -= learning_rate * gradient
    return beta

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
    while True:
        print("\n--- Machine Learning Library Comparison ---")
        print("1. Gaussian Elimination")
        print("2. Regression Algorithms")
        print("3. Numerical Differentiation")
        print("4. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            print("Gaussian Elimination")
            A = []
            b = []
            for i in range(5):
                row = list(map(float, input(f"Enter coefficients for equation {i + 1} (space-separated): ").split()))
                A.append(row)
                b.append(float(input(f"Enter constant for equation {i + 1}: ")))
            A = np.array(A)
            b = np.array(b)
            solution = gaussian_elimination(A, b)
            print("Solution:", solution)

        elif choice == '2':
            print("Regression Algorithms")
            X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])  # Example data
            y = np.array([1, 2, 2, 3])  # Example target
            print("1. Ordinary Least Squares")
            print("2. Gradient Descent")
            reg_choice = input("Select an option: ")
            if reg_choice == '1':
                beta = ordinary_least_squares(X, y)
                print("OLS Coefficients:", beta)
            elif reg_choice == '2':
                beta = gradient_descent(X, y)
                print("Gradient Descent Coefficients:", beta)
            else:
                print("Invalid choice.")

        elif choice == '3':
            print("Numerical Differentiation")
            func = lambda x: x**2  # Example function
            x = float(input("Enter the point to differentiate at: "))
            print("1. Forward Difference")
            print("2. Backward Difference")
            print("3. Central Difference")
            diff_choice = input("Select an option: ")
            if diff_choice == '1':
                derivative = numerical_differentiation(func, x, method='forward')
            elif diff_choice == '2':
                derivative = numerical_differentiation(func, x, method='backward')
            elif diff_choice == '3':
                derivative = numerical_differentiation(func, x, method='central')
            else:
                print("Invalid choice.")
                continue
            print("Derivative at x =", x, "is approximately:", derivative)

        elif choice == '4':
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()