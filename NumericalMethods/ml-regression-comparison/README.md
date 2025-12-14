### Application Structure

1. **Gaussian Elimination**: Implement a function to solve systems of linear equations using Gaussian elimination.
2. **Regression Algorithms**: Implement both analytical (e.g., Ordinary Least Squares) and iterative (e.g., Gradient Descent) regression algorithms.
3. **Numerical Differentiation**: Provide options for users to select methods for numerical differentiation (e.g., Forward Difference, Backward Difference, Central Difference).
4. **User Interface**: A simple CLI to interact with the user.

### Implementation

Here's a basic implementation of the application:

```python
import numpy as np

def gaussian_elimination(A, b):
    n = len(b)
    # Forward elimination
    for i in range(n):
        # Make the diagonal contain all non-zero elements
        if A[i][i] == 0.0:
            raise ValueError("Matrix is singular!")
        for j in range(i + 1, n):
            ratio = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= ratio * A[i][k]
            b[j] -= ratio * b[i]

    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = b[i] / A[i][i]
        for j in range(i + 1, n):
            x[i] -= (A[i][j] / A[i][i]) * x[j]
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
        raise ValueError("Invalid method selected!")

def main():
    print("Welcome to the Machine Learning Library Comparison Tool!")
    
    while True:
        print("\nSelect an option:")
        print("1. Gaussian Elimination")
        print("2. Regression Algorithms")
        print("3. Numerical Differentiation")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Gaussian Elimination
            A = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], dtype=float)
            b = np.array([8, -11, -3], dtype=float)
            solution = gaussian_elimination(A, b)
            print("Solution:", solution)
        
        elif choice == '2':
            # Regression Algorithms
            X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]], dtype=float)
            y = np.array([1, 2, 2, 3], dtype=float)
            print("1. Ordinary Least Squares")
            print("2. Gradient Descent")
            reg_choice = input("Select regression method: ")
            if reg_choice == '1':
                beta = ordinary_least_squares(X, y)
                print("OLS Coefficients:", beta)
            elif reg_choice == '2':
                beta = gradient_descent(X, y)
                print("Gradient Descent Coefficients:", beta)
            else:
                print("Invalid choice.")
        
        elif choice == '3':
            # Numerical Differentiation
            func = lambda x: x**2  # Example function
            x = float(input("Enter the point to differentiate at: "))
            print("1. Forward Difference")
            print("2. Backward Difference")
            print("3. Central Difference")
            diff_choice = input("Select differentiation method: ")
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
```

### Explanation

1. **Gaussian Elimination**: The `gaussian_elimination` function solves a system of linear equations represented by matrix `A` and vector `b`.
2. **Regression Algorithms**: The `ordinary_least_squares` function computes the coefficients using the OLS method, while `gradient_descent` implements a simple gradient descent algorithm.
3. **Numerical Differentiation**: The `numerical_differentiation` function allows the user to choose between forward, backward, and central difference methods.
4. **User Interface**: The `main` function provides a simple CLI for users to interact with the application.

### Running the Application

To run the application, save the code in a file named `ml_tool.py` and execute it using Python:

```bash
python ml_tool.py
```

This application can be expanded with more features, better error handling, and a more sophisticated user interface (e.g., using a GUI framework like Tkinter or a web framework like Flask).