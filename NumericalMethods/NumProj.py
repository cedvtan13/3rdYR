# Simple Numerical Methods Program
# This program helps you understand basic numerical methods

# IMPORTS - These are like importing tools from a toolbox
import numpy as np  # numpy = math calculator for lists/arrays
import math         # math = basic math functions like sqrt, exp, etc.
import matplotlib.pyplot as plt  # matplotlib = makes graphs!

# ========================================
# PART 1: GAUSSIAN ELIMINATION
# This solves equations like: 2x + 3y = 8, x - y = 1
# Can handle 2 to 5 variables!
# ========================================

def get_user_equations():
    """
    This function asks the user to type in their equations
    Returns: equations matrix and answers list
    """
    print("\n" + "="*50)
    print("GAUSSIAN ELIMINATION - Solve System of Equations")
    print("="*50)
    
    # Ask how many equations (2 to 5)
    while True:
        num_vars = int(input("How many variables? (2-5): "))
        if 2 <= num_vars <= 5:
            break
        print("Please enter a number between 2 and 5!")
    
    # Create empty lists to store equations
    equations = []  # This will be like [[2,3], [1,-1]]
    answers = []    # This will be like [8, 1]
    
    print(f"\nEnter {num_vars} equations:")
    print("Example: For 2x + 3y = 8, enter coefficients: 2 3 8")
    
    # Loop through each equation
    for i in range(num_vars):
        print(f"\nEquation {i+1}:")
        
        # Get coefficients (the numbers before variables)
        coeffs = []
        for j in range(num_vars):
            var_name = chr(120 + j)  # 120 is 'x' in ASCII, so x, y, z, etc.
            coeff = float(input(f"  Coefficient of {var_name}: "))
            coeffs.append(coeff)
        
        # Get the answer (right side of =)
        answer = float(input(f"  Answer (right side): "))
        
        equations.append(coeffs)
        answers.append(answer)
    
    return equations, answers


def solve_gaussian(equations, answers):
    """
    Solve using Gaussian Elimination
    This uses numpy's built-in solver (it does Gaussian Elimination internally)
    """
    print("\n--- Solving with NUMPY (fast method) ---")
    
    # Convert to numpy arrays (numpy needs this format)
    A = np.array(equations)  # Coefficient matrix
    b = np.array(answers)    # Answer vector
    
    try:
        # np.linalg.solve() does Gaussian Elimination
        solution = np.linalg.solve(A, b)
        
        # Print the solution nicely
        print("\nSOLUTION:")
        for i, value in enumerate(solution):
            var_name = chr(120 + i)  # x, y, z, etc.
            print(f"  {var_name} = {value:.4f}")
        
        return solution
    
    except np.linalg.LinAlgError:
        print("ERROR: Cannot solve! Equations might be inconsistent.")
        return None


# NEW FUNCTION - ADD THIS AFTER solve_gaussian
def solve_gaussian_manual(equations, answers):
    """
    MANUAL Gaussian Elimination - Shows every step!
    This is how you solve equations by hand in math class
    
    Steps:
    1. Forward Elimination - Make lower triangle zeros
    2. Back Substitution - Solve from bottom to top
    """
    print("\n--- Solving MANUALLY (step-by-step) ---")
    
    # Get the size (how many equations)
    n = len(equations)
    
    # Make a copy so we don't change the original
    # We combine equations and answers into one matrix [A|b]
    matrix = []
    for i in range(n):
        row = equations[i].copy()  # Copy the equation
        row.append(answers[i])      # Add the answer at the end
        matrix.append(row)
    
    print("\nStarting matrix [Equations | Answers]:")
    print_matrix(matrix)
    
    # STEP 1: FORWARD ELIMINATION
    # Goal: Make all numbers below the diagonal = 0
    print("\n=== STEP 1: FORWARD ELIMINATION ===")
    
    for col in range(n):  # For each column (variable)
        print(f"\nWorking on column {col} (variable {chr(120 + col)}):")
        
        # Find the biggest number in this column (pivot)
        # This makes the calculation more accurate
        max_row = col
        for row in range(col + 1, n):
            if abs(matrix[row][col]) > abs(matrix[max_row][col]):
                max_row = row
        
        # Swap rows if needed
        if max_row != col:
            print(f"  Swapping row {col} with row {max_row}")
            matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
            print_matrix(matrix)
        
        # Check if pivot is zero (can't divide by zero!)
        if abs(matrix[col][col]) < 0.0001:
            print("ERROR: Cannot solve! (Division by zero)")
            return None
        
        # Eliminate all rows below this one
        for row in range(col + 1, n):
            # Calculate the factor to multiply
            factor = matrix[row][col] / matrix[col][col]
            print(f"  Row {row}: Subtract {factor:.4f} × Row {col}")
            
            # Subtract: row = row - factor * col_row
            for j in range(n + 1):  # +1 because we include the answer
                matrix[row][j] -= factor * matrix[col][j]
            
            print_matrix(matrix)
    
    print("\n=== After Forward Elimination ===")
    print_matrix(matrix)
    
    # STEP 2: BACK SUBSTITUTION
    # Goal: Solve from bottom to top
    print("\n=== STEP 2: BACK SUBSTITUTION ===")
    
    # Create list to store solutions
    solution = [0.0] * n
    
    # Start from the last equation and work backwards
    for i in range(n - 1, -1, -1):  # n-1, n-2, ..., 1, 0
        var_name = chr(120 + i)
        
        # Start with the answer (right side)
        solution[i] = matrix[i][n]  # n is the answer column
        
        # Subtract all known variables
        for j in range(i + 1, n):
            solution[i] -= matrix[i][j] * solution[j]
        
        # Divide by the coefficient
        solution[i] /= matrix[i][i]
        
        print(f"  {var_name} = {solution[i]:.4f}")
    
    print("\n=== FINAL SOLUTION ===")
    for i, value in enumerate(solution):
        var_name = chr(120 + i)
        print(f"  {var_name} = {value:.4f}")
    
    return solution


def print_matrix(matrix):
    """
    Helper function to print a matrix nicely
    Makes it easier to see what's happening
    """
    for row in matrix:
        # Format each number to 4 decimal places
        formatted = [f"{num:8.4f}" for num in row]
        print("  [ " + "  ".join(formatted) + " ]")


# UPDATE get_user_equations to ask which method
def gaussian_menu():
    """
    Menu for Gaussian Elimination - choose manual or numpy
    """
    # Get equations from user
    equations, answers = get_user_equations()
    
    # Ask which method to use
    print("\n" + "="*50)
    print("Choose solving method:")
    print("1. NumPy (Fast, no steps shown)")
    print("2. Manual (Slow, shows every step)")
    print("="*50)
    
    method = input("Choice (1-2): ")
    
    if method == "1":
        solve_gaussian(equations, answers)
    elif method == "2":
        solve_gaussian_manual(equations, answers)
    else:
        print("Invalid choice! Using NumPy...")
        solve_gaussian(equations, answers)

# ========================================
# PART 2: NUMERICAL DIFFERENTIATION
# This finds the slope/derivative at a point
# Three methods: Forward, Backward, Central
# ========================================

def simple_function(x):
    """
    This is the function we'll differentiate
    You can change this to test different functions!
    Current: f(x) = x² + 2x + 1
    """
    return x**2 + 2*x + 1


def forward_difference(x, h):
    """
    Forward Difference: Look ahead
    Formula: f'(x) ≈ [f(x+h) - f(x)] / h
    """
    # Calculate function at x and x+h
    f_x = simple_function(x)
    f_x_plus_h = simple_function(x + h)
    
    # Apply formula
    derivative = (f_x_plus_h - f_x) / h
    
    print(f"Forward Difference: f'({x}) ≈ {derivative:.6f}")
    return derivative


def backward_difference(x, h):
    """
    Backward Difference: Look behind
    Formula: f'(x) ≈ [f(x) - f(x-h)] / h
    """
    # Calculate function at x and x-h
    f_x = simple_function(x)
    f_x_minus_h = simple_function(x - h)
    
    # Apply formula
    derivative = (f_x - f_x_minus_h) / h
    
    print(f"Backward Difference: f'({x}) ≈ {derivative:.6f}")
    return derivative


def central_difference(x, h):
    """
    Central Difference: Look both ways (most accurate!)
    Formula: f'(x) ≈ [f(x+h) - f(x-h)] / 2h
    """
    # Calculate function at x+h and x-h
    f_x_plus_h = simple_function(x + h)
    f_x_minus_h = simple_function(x - h)
    
    # Apply formula
    derivative = (f_x_plus_h - f_x_minus_h) / (2 * h)
    
    print(f"Central Difference: f'({x}) ≈ {derivative:.6f}")
    return derivative


def differentiation_menu():
    """
    Let user choose differentiation method
    """
    print("\n" + "="*50)
    print("NUMERICAL DIFFERENTIATION")
    print("="*50)
    print("Function: f(x) = x² + 2x + 1")
    print("Exact derivative: f'(x) = 2x + 2")
    
    # Get x value from user
    x = float(input("\nEnter x value: "))
    h = float(input("Enter step size h (try 0.01): "))
    
    # Calculate exact answer for comparison
    exact = 2*x + 2
    print(f"\nExact answer: f'({x}) = {exact}")
    print("\nNumerical methods:")
    
    # Choose method
    print("\nWhich method?")
    print("1. Forward Difference")
    print("2. Backward Difference")
    print("3. Central Difference")
    print("4. Compare all three!")
    
    choice = input("Choice (1-4): ")
    
    if choice == "1":
        forward_difference(x, h)
    elif choice == "2":
        backward_difference(x, h)
    elif choice == "3":
        central_difference(x, h)
    elif choice == "4":
        print("\nComparing all methods:")
        forward_difference(x, h)
        backward_difference(x, h)
        central_difference(x, h)


# ========================================
# PART 3: REGRESSION - ANALYTICAL vs ITERATIVE
# Compare two ways to find the best-fit line
# ========================================

def analytical_regression(x_points, y_points):
    """
    ANALYTICAL METHOD (Direct calculation using formulas)
    This calculates the answer directly using math formulas
    Formula for line: y = mx + b
    """
    print("\n--- ANALYTICAL METHOD ---")
    print("This solves using direct formulas (fast!)")
    
    n = len(x_points)
    
    # Calculate sums needed for formulas
    sum_x = sum(x_points)
    sum_y = sum(y_points)
    sum_xy = sum(x_points[i] * y_points[i] for i in range(n))
    sum_x2 = sum(x * x for x in x_points)
    
    # Formula for slope (m)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    
    # Formula for intercept (b)
    b = (sum_y - m * sum_x) / n
    
    print(f"Result: y = {m:.4f}x + {b:.4f}")
    return m, b


def iterative_regression(x_points, y_points, learning_rate=0.01, iterations=1000):
    """
    ITERATIVE METHOD (Gradient Descent)
    This guesses the answer and improves it step by step
    Like climbing down a hill to find the lowest point
    """
    print("\n--- ITERATIVE METHOD (Gradient Descent) ---")
    print("This starts with a guess and improves it step by step")
    
    # Start with random guess
    m = 0.0  # slope
    b = 0.0  # intercept
    n = len(x_points)
    
    print(f"Starting guess: y = {m}x + {b}")
    print(f"Learning rate: {learning_rate}, Iterations: {iterations}")
    
    # Improve guess many times
    for i in range(iterations):
        # Predict y values with current m and b
        y_predicted = [m * x + b for x in x_points]
        
        # Calculate error
        error = [(y_predicted[j] - y_points[j]) for j in range(n)]
        
        # Update m and b to reduce error
        # These formulas come from calculus (derivatives)
        m_gradient = (2/n) * sum(error[j] * x_points[j] for j in range(n))
        b_gradient = (2/n) * sum(error)
        
        # Take a small step in the right direction
        m = m - learning_rate * m_gradient
        b = b - learning_rate * b_gradient
        
        # Show progress every 200 steps
        if (i+1) % 200 == 0:
            avg_error = sum(abs(e) for e in error) / n
            print(f"  Step {i+1}: y = {m:.4f}x + {b:.4f}, Error: {avg_error:.4f}")
    
    print(f"Final result: y = {m:.4f}x + {b:.4f}")
    return m, b

# ========================================
# PART 4: POLYNOMIAL REGRESSION
# Fit curves (not just lines) through data
# ========================================

def polynomial_regression(x_points, y_points, degree=2):
    """
    POLYNOMIAL REGRESSION
    Instead of y = mx + b (straight line)
    We find y = ax² + bx + c (curve)
    
    degree = 1: line (y = mx + b)
    degree = 2: parabola (y = ax² + bx + c)
    degree = 3: cubic (y = ax³ + bx² + cx + d)
    """
    print(f"\n--- POLYNOMIAL REGRESSION (Degree {degree}) ---")
    print("This fits a CURVE through your data points")
    
    # numpy has a function that does polynomial regression
    # It returns coefficients from highest degree to lowest
    # Example: [2, 3, 1] means 2x² + 3x + 1
    coefficients = np.polyfit(x_points, y_points, degree)
    
    # Create a polynomial function from coefficients
    poly_function = np.poly1d(coefficients)
    
    # Print the equation nicely
    print(f"Equation: {poly_function}")
    
    return coefficients, poly_function


def plot_polynomial_regression(x_points, y_points, degree_list=[1, 2, 3]):
    """
    Plot data with different polynomial curves
    Shows how curves fit better than lines for curved data
    """
    print("\n📊 Creating polynomial comparison graph...")
    
    plt.figure(figsize=(12, 6))
    
    # Plot the actual data points
    plt.scatter(x_points, y_points, color='black', s=100, label='Data Points', zorder=3)
    
    # Create smooth x values for plotting curves
    x_smooth = np.linspace(min(x_points) - 0.5, max(x_points) + 0.5, 200)
    
    # Colors for different degree polynomials
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    line_styles = ['-', '--', '-.', ':']
    
    # Fit and plot each polynomial degree
    for i, degree in enumerate(degree_list):
        coeffs, poly_func = polynomial_regression(x_points, y_points, degree)
        
        # Calculate y values for the smooth curve
        y_smooth = poly_func(x_smooth)
        
        # Plot the curve
        plt.plot(x_smooth, y_smooth, 
                color=colors[i % len(colors)], 
                linewidth=2,
                linestyle=line_styles[i % len(line_styles)],
                label=f'Degree {degree}')
    
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Polynomial Regression Comparison', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()
    
    print("✅ Graph displayed!")


def polynomial_menu():
    """
    Menu for polynomial regression
    """
    print("\n" + "="*50)
    print("POLYNOMIAL REGRESSION")
    print("="*50)
    
    # Get data - use curved example or custom
    print("\nUse example curved data? (1,1), (2,4), (3,9), (4,16), (5,23)")
    print("(This data follows a curve, not a line!)")
    use_example = input("(y/n): ").lower()
    
    if use_example == 'y':
        # Example: roughly follows y = x²
        x_points = [1, 2, 3, 4, 5]
        y_points = [1, 4, 9, 16, 23]
    else:
        num_points = int(input("How many data points? "))
        x_points = []
        y_points = []
        for i in range(num_points):
            x = float(input(f"x{i+1}: "))
            y = float(input(f"y{i+1}: "))
            x_points.append(x)
            y_points.append(y)
    
    print(f"\nData points: {list(zip(x_points, y_points))}")
    
    # Ask what degree polynomial
    print("\nWhat degree polynomial?")
    print("1 = Line (y = mx + b)")
    print("2 = Parabola (y = ax² + bx + c)")
    print("3 = Cubic curve")
    print("0 = Compare multiple degrees")
    
    choice = input("Choice: ")
    
    if choice == "0":
        # Compare multiple degrees
        print("\n=== Comparing Different Polynomial Degrees ===")
        for deg in [1, 2, 3]:
            polynomial_regression(x_points, y_points, deg)
        
        # Show graph
        show_graph = input("\nShow comparison graph? (y/n): ").lower()
        if show_graph == 'y':
            plot_polynomial_regression(x_points, y_points, [1, 2, 3])
    else:
        # Single degree
        degree = int(choice)
        coeffs, poly_func = polynomial_regression(x_points, y_points, degree)
        
        # Show graph
        show_graph = input("\nShow graph? (y/n): ").lower()
        if show_graph == 'y':
            plot_polynomial_regression(x_points, y_points, [degree])


# ========================================
# PART 5: NEWTON'S METHOD FOR ROOT FINDING
# Find where a function crosses zero (f(x) = 0)
# ========================================

def test_function(x):
    """
    The function we want to find roots for
    Current: f(x) = x² - 4
    This has roots at x = 2 and x = -2
    (because 2² - 4 = 0 and (-2)² - 4 = 0)
    """
    return x**2 - 4


def test_function_derivative(x):
    """
    The derivative of our test function
    For f(x) = x² - 4, derivative is f'(x) = 2x
    
    Newton's method needs the derivative!
    """
    return 2 * x


def newtons_method(x0, tolerance=0.0001, max_iterations=50):
    """
    NEWTON'S METHOD
    Find where f(x) = 0 by making better and better guesses
    
    Formula: x_new = x_old - f(x_old) / f'(x_old)
    
    x0 = starting guess
    tolerance = how close to zero is "good enough"
    max_iterations = give up after this many tries
    """
    print("\n--- NEWTON'S METHOD ---")
    print("Finding where f(x) = x² - 4 equals zero")
    print(f"Starting guess: x = {x0}")
    print(f"Tolerance: {tolerance}")
    
    x = x0  # Current guess
    
    print("\nIteration | x value | f(x) value | Change")
    print("-" * 50)
    
    for i in range(max_iterations):
        # Calculate function value and derivative at current x
        fx = test_function(x)
        fpx = test_function_derivative(x)
        
        # Check if derivative is zero (can't divide by zero!)
        if abs(fpx) < 0.000001:
            print("ERROR: Derivative is zero! Can't continue.")
            return None
        
        # Newton's formula: new guess = old guess - f(x)/f'(x)
        x_new = x - fx / fpx
        
        # How much did we change?
        change = abs(x_new - x)
        
        # Print progress
        print(f"{i+1:9d} | {x:7.4f} | {fx:10.6f} | {change:.6f}")
        
        # Check if we're close enough
        if abs(fx) < tolerance:
            print(f"\n✅ Found root: x = {x:.6f}")
            print(f"Check: f({x:.6f}) = {fx:.6f} ≈ 0")
            return x
        
        # Update x for next iteration
        x = x_new
    
    print(f"\n⚠️ Did not converge after {max_iterations} iterations")
    print(f"Last value: x = {x:.6f}, f(x) = {test_function(x):.6f}")
    return x


def bisection_method(a, b, tolerance=0.0001, max_iterations=50):
    """
    BISECTION METHOD (Alternative to Newton's)
    Repeatedly cut the interval in half
    Slower but more reliable than Newton's method
    
    a, b = interval endpoints (must have opposite signs)
    """
    print("\n--- BISECTION METHOD ---")
    print("Finding where f(x) = x² - 4 equals zero")
    print(f"Starting interval: [{a}, {b}]")
    
    # Check if there's a root in this interval
    fa = test_function(a)
    fb = test_function(b)
    
    if fa * fb > 0:
        print("ERROR: Function has same sign at both ends!")
        print("No root guaranteed in this interval.")
        return None
    
    print("\nIteration | Left | Right | Middle | f(middle)")
    print("-" * 60)
    
    for i in range(max_iterations):
        # Find the middle point
        c = (a + b) / 2
        fc = test_function(c)
        
        print(f"{i+1:9d} | {a:5.4f} | {b:5.4f} | {c:6.4f} | {fc:9.6f}")
        
        # Check if we found the root
        if abs(fc) < tolerance:
            print(f"\n✅ Found root: x = {c:.6f}")
            return c
        
        # Decide which half to keep
        if fa * fc < 0:
            # Root is in left half
            b = c
            fb = fc
        else:
            # Root is in right half
            a = c
            fa = fc
    
    print(f"\n⚠️ Did not converge after {max_iterations} iterations")
    return (a + b) / 2


def root_finding_menu():
    """
    Menu for root finding methods
    """
    print("\n" + "="*50)
    print("ROOT FINDING METHODS")
    print("="*50)
    print("Function: f(x) = x² - 4")
    print("This has roots at x = 2 and x = -2")
    
    print("\nWhich method?")
    print("1. Newton's Method (fast, needs good starting guess)")
    print("2. Bisection Method (slower, more reliable)")
    print("3. Compare both methods")
    
    choice = input("Choice (1-3): ")
    
    if choice == "1":
        x0 = float(input("\nEnter starting guess: "))
        newtons_method(x0)
        
    elif choice == "2":
        print("\nEnter interval [a, b] where root exists")
        a = float(input("  Left endpoint (a): "))
        b = float(input("  Right endpoint (b): "))
        bisection_method(a, b)
        
    elif choice == "3":
        print("\n=== NEWTON'S METHOD ===")
        x0 = float(input("Starting guess for Newton's: "))
        root_newton = newtons_method(x0)
        
        print("\n" + "="*50)
        print("\n=== BISECTION METHOD ===")
        print("Enter interval [a, b] where root exists")
        a = float(input("  Left endpoint (a): "))
        b = float(input("  Right endpoint (b): "))
        root_bisection = bisection_method(a, b)
        
        if root_newton and root_bisection:
            print("\n" + "="*50)
            print("COMPARISON:")
            print(f"Newton's Method:    x = {root_newton:.6f}")
            print(f"Bisection Method:   x = {root_bisection:.6f}")
            print(f"Difference:         {abs(root_newton - root_bisection):.6f}")

def plot_regression_results(x_points, y_points, m_analytical, b_analytical, m_iterative, b_iterative):
    """
    Create a visual graph showing:
    - The data points (dots)
    - The analytical line (blue)
    - The iterative line (red)
    """
    print("\n📊 Creating graph...")
    
    # Create a figure (the graph window)
    plt.figure(figsize=(10, 6))
    
    # Plot the actual data points as black dots
    plt.scatter(x_points, y_points, color='black', s=100, label='Data Points', zorder=3)
    
    # Create x values for drawing the lines
    x_line = np.linspace(min(x_points) - 1, max(x_points) + 1, 100)
    
    # Calculate y values for both lines
    y_analytical = m_analytical * x_line + b_analytical
    y_iterative = m_iterative * x_line + b_iterative
    
    # Draw the analytical line (blue, solid)
    plt.plot(x_line, y_analytical, color='blue', linewidth=2, 
             label=f'Analytical: y = {m_analytical:.2f}x + {b_analytical:.2f}')
    
    # Draw the iterative line (red, dashed)
    plt.plot(x_line, y_iterative, color='red', linewidth=2, linestyle='--',
             label=f'Iterative: y = {m_iterative:.2f}x + {b_iterative:.2f}')
    
    # Add labels and title
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Linear Regression: Analytical vs Iterative', fontsize=14, fontweight='bold')
    
    # Add grid for easier reading
    plt.grid(True, alpha=0.3)
    
    # Add legend
    plt.legend(fontsize=10)
    
    # Make it look nice
    plt.tight_layout()
    
    # Show the graph!
    plt.show()
    
    print("✅ Graph displayed!")

def regression_menu():
    """
    Compare analytical vs iterative regression
    """
    print("\n" + "="*50)
    print("LINEAR REGRESSION COMPARISON")
    print("="*50)
    
    # Get data points from user or use example
    print("\nUse example data? (1,2), (2,4), (3,5), (4,4), (5,5)")
    use_example = input("(y/n): ").lower()
    
    if use_example == 'y':
        # Use pre-made example data
        x_points = [1, 2, 3, 4, 5]
        y_points = [2, 4, 5, 4, 5]
    else:
        # Let user input their own data
        num_points = int(input("How many data points? "))
        x_points = []
        y_points = []
        for i in range(num_points):
            x = float(input(f"x{i+1}: "))
            y = float(input(f"y{i+1}: "))
            x_points.append(x)
            y_points.append(y)
    
    # Show the data points
    print(f"\nData points: {list(zip(x_points, y_points))}")
    
    # Run BOTH regression methods
    m1, b1 = analytical_regression(x_points, y_points)
    m2, b2 = iterative_regression(x_points, y_points)
    
    # Compare results
    print("\n" + "="*50)
    print("COMPARISON:")
    print(f"Analytical:  y = {m1:.4f}x + {b1:.4f}")
    print(f"Iterative:   y = {m2:.4f}x + {b2:.4f}")
    print(f"Difference in m: {abs(m1-m2):.6f}")
    print(f"Difference in b: {abs(b1-b2):.6f}")
    
    # Ask if user wants to see a graph
    show_graph = input("\nShow graph? (y/n): ").lower()
    if show_graph == 'y':
        plot_regression_results(x_points, y_points, m1, b1, m2, b2)


# ========================================
# MAIN MENU - Where the program starts
# ========================================

def main():
    """
    Main program - shows menu and calls functions
    """
    print("=" * 60)
    print("    MACHINE LEARNING & NUMERICAL METHODS LEARNING TOOL")
    print("=" * 60)
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Gaussian Elimination (Solve equations with 2-5 variables)")
        print("2. Numerical Differentiation (Forward/Backward/Central)")
        print("3. Linear Regression (Analytical vs Iterative)")
        print("4. Polynomial Regression (Fit curves to data)")
        print("5. Root Finding (Newton's & Bisection methods)")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-6): ")
        
        if choice == "1":
            gaussian_menu()
            
        elif choice == "2":
            differentiation_menu()
            
        elif choice == "3":
            regression_menu()
            
        elif choice == "4":
            polynomial_menu()
            
        elif choice == "5":
            root_finding_menu()
            
        elif choice == "6":
            print("\nThank you for using this learning tool!")
            print("Keep practicing numerical methods! 🚀")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-6.")
        
        input("\nPress Enter to continue...")

# This is where Python starts running
# __name__ == "__main__" means "if this file is run directly"
if __name__ == "__main__":
    main()