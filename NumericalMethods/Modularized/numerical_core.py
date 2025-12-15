
# NUMERICAL CORE FUNCTIONS


import numpy as np

# ========================================
# GAUSSIAN ELIM
# ========================================

def solve_gaussian(equations, answers):
    # Solve system of equations using Gaussian Elimination
    
    # equations: list of lists [[2,3], [1,-1]] means 2x+3y, x-y
    # answers: list [8, 1] means = 8, = 1
    
    # Returns: list of solutions [x, y] or None if can't solve
    
    try:
        # Convert to numpy arrays for calculation
        A = np.array(equations)  # Coefficient matrix
        b = np.array(answers)    # Answer vector
        
        # Solve using numpy (it uses Gaussian elimination internally)
        solution = np.linalg.solve(A, b)
        return solution
    except:
        # Return None if system can't be solved
        return None


# ========================================
# NUMERICAL DIFF
# ========================================

def differentiate_function(x, h, method='central'):

    # Calculate derivative of f(x) = x² + 2x + 1
    
    # x: point where we want the derivative
    # h: step size (small number like 0.01)
    # method: 'forward', 'backward', or 'central'
    
    # Returns: approximate derivative value

    # Define the function
    def f(x):
        return x**2 + 2*x + 1
    
    if method == 'forward':
        # Forward difference: look ahead
        derivative = (f(x + h) - f(x)) / h
    elif method == 'backward':
        # Backward difference: look behind
        derivative = (f(x) - f(x - h)) / h
    else:  # central
        # Central difference: look both ways (most accurate)
        derivative = (f(x + h) - f(x - h)) / (2 * h)
    
    return derivative


def exact_derivative(x):

    # Exact derivative of f(x) = x² + 2x + 1
    # This is f'(x) = 2x + 2
    # Used for comparison with numerical methods

    return 2*x + 2


# ========================================
# LINEAR REG
# ========================================

def linear_regression(x_points, y_points):

    # Find best line y = mx + b through points
    # Uses analytical method (direct formula)
    
    # x_points: list of x coordinates [1, 2, 3, 4, 5]
    # y_points: list of y coordinates [2, 4, 5, 4, 5]
    
    # Returns: (m, b) where m is slope, b is y-intercept

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
    
    return m, b


# ========================================
# POLY REG
# ========================================

def polynomial_regression(x_points, y_points, degree):

    # Find best polynomial curve through points
    
    # degree = 1: line (y = mx + b)
    # degree = 2: parabola (y = ax² + bx + c)
    # degree = 3: cubic curve
    
    # Returns: (coefficients, polynomial_function)

    # Use numpy's polyfit to find coefficients
    coefficients = np.polyfit(x_points, y_points, degree)
    
    # Create polynomial function from coefficients
    poly_function = np.poly1d(coefficients)
    
    return coefficients, poly_function


# ========================================
# 3D MULT REG
# ========================================

def multiple_regression_3d(x_data, y_data, z_data):
 
    # Find best plane through 3D points: z = a*x + b*y + c
    
    # Example: Predict house price (z) from size (x) and age (y)
    
    # Returns: (a, b, c, r_squared)
    # - a: coefficient for x
    # - b: coefficient for y
    # - c: constant term
    # - r_squared: goodness of fit (0 to 1, higher is better)

    n = len(x_data)
    
    # Build design matrix: each row is [x, y, 1]
    A = np.column_stack([x_data, y_data, np.ones(n)])
    z = np.array(z_data)
    
    # Solve using least squares (like Gaussian elimination)
    coefficients, residuals, rank, s = np.linalg.lstsq(A, z, rcond=None)
    a, b, c = coefficients
    
    # Calculate R-squared (how good is the fit?)
    z_predicted = a * np.array(x_data) + b * np.array(y_data) + c
    ss_res = np.sum((z - z_predicted) ** 2)  # Residual sum of squares
    ss_tot = np.sum((z - np.mean(z)) ** 2)   # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)
    
    return a, b, c, r_squared