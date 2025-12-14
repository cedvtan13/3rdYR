"""
PLOTTING FUNCTIONS
Creates all the graphs and visualizations
Simple matplotlib code for students to understand
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ========================================
# LINEAR REGRESSION PLOT
# ========================================

def plot_linear_regression(x_points, y_points, m, b):
    """
    Plot data points and best-fit line
    
    x_points, y_points: the data
    m, b: slope and intercept of line
    """
    # Create figure
    plt.figure(figsize=(8, 6))
    
    # Plot data points as red dots
    plt.scatter(x_points, y_points, color='red', s=100, label='Data Points')
    
    # Create line from x_min to x_max
    x_line = np.linspace(min(x_points)-1, max(x_points)+1, 100)
    y_line = m * x_line + b
    
    # Plot the line
    plt.plot(x_line, y_line, 'b-', linewidth=2, 
            label=f'Best Line: y = {m:.2f}x + {b:.2f}')
    
    # Labels and styling
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title('Linear Regression', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ========================================
# POLYNOMIAL REGRESSION PLOT
# ========================================

def plot_polynomial_regression(x_points, y_points, degree, poly_function):
    """
    Plot data points and polynomial curve
    
    degree: polynomial degree (1, 2, 3, etc.)
    poly_function: the polynomial to plot
    """
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot data points as black dots
    plt.scatter(x_points, y_points, color='black', s=100, 
               label='Data Points', zorder=3)
    
    # Create smooth curve
    x_smooth = np.linspace(min(x_points)-0.5, max(x_points)+0.5, 200)
    y_smooth = poly_function(x_smooth)
    
    # Plot the curve
    plt.plot(x_smooth, y_smooth, color='blue', linewidth=2,
            label=f'Degree {degree} Polynomial')
    
    # Labels and styling
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.title(f'Polynomial Regression (Degree {degree})', 
             fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ========================================
# 3D MULTIPLE REGRESSION PLOT
# ========================================

def plot_3d_regression(x_data, y_data, z_data, a, b, c):
    """
    Create 3D visualization of data and best-fit plane
    
    x_data, y_data, z_data: the 3D points
    a, b, c: coefficients of plane z = a*x + b*y + c
    """
    # Create 3D figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot data points as red spheres
    ax.scatter(x_data, y_data, z_data, color='red', s=100, 
              label='Data Points', alpha=0.8)
    
    # Create mesh grid for the plane
    x_range = np.linspace(min(x_data) - 1, max(x_data) + 1, 20)
    y_range = np.linspace(min(y_data) - 1, max(y_data) + 1, 20)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    
    # Calculate z values for plane: z = a*x + b*y + c
    Z_grid = a * X_grid + b * Y_grid + c
    
    # Plot the plane as blue surface
    ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.3, color='blue')
    
    # Labels
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('3D Multiple Linear Regression', 
                fontsize=14, fontweight='bold')
    
    # Add equation text
    ax.text2D(0.05, 0.95, f'Plane: z = {a:.2f}x + {b:.2f}y + {c:.2f}', 
             transform=ax.transAxes, fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()