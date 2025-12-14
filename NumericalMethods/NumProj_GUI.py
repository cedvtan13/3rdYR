"""
NUMERICAL METHODS GUI APPLICATION
This is a graphical version with buttons and windows
Plus 3D visualization for multiple regression!
"""

# IMPORTS - Tools we need
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # For 3D plots
import tkinter as tk  # GUI library (comes with Python!)
from tkinter import ttk, messagebox, scrolledtext

# ========================================
# CORE NUMERICAL METHODS (Same as before)
# ========================================

def solve_gaussian_quick(equations, answers):
    """Quick Gaussian solver for GUI"""
    try:
        A = np.array(equations)
        b = np.array(answers)
        solution = np.linalg.solve(A, b)
        return solution
    except:
        return None


def analytical_regression(x_points, y_points):
    """Analytical linear regression"""
    n = len(x_points)
    sum_x = sum(x_points)
    sum_y = sum(y_points)
    sum_xy = sum(x_points[i] * y_points[i] for i in range(n))
    sum_x2 = sum(x * x for x in x_points)
    
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    b = (sum_y - m * sum_x) / n
    
    return m, b


def polynomial_regression_quick(x_points, y_points, degree):
    """Quick polynomial regression"""
    coefficients = np.polyfit(x_points, y_points, degree)
    poly_function = np.poly1d(coefficients)
    return coefficients, poly_function


# ========================================
# NEW: 3D MULTIPLE REGRESSION
# Predict Z from X and Y: z = a*x + b*y + c
# ========================================

def multiple_regression_3d(x_data, y_data, z_data):
    """
    MULTIPLE LINEAR REGRESSION (3D)
    Find the best plane through 3D points
    Equation: z = a*x + b*y + c
    
    x_data = list of x coordinates
    y_data = list of y coordinates
    z_data = list of z coordinates (what we want to predict)
    
    Example: Predict house price (z) from size (x) and age (y)
    """
    print("\n--- 3D MULTIPLE REGRESSION ---")
    print("Finding best plane: z = a*x + b*y + c")
    
    n = len(x_data)
    
    # Build the design matrix (mathematical way to solve this)
    # Each row is [x, y, 1] for the equation z = a*x + b*y + c
    A = np.column_stack([x_data, y_data, np.ones(n)])
    
    # z_data is what we want to predict
    z = np.array(z_data)
    
    # Solve using least squares (finds best a, b, c)
    # This is like Gaussian elimination but for overdetermined systems
    coefficients, residuals, rank, s = np.linalg.lstsq(A, z, rcond=None)
    
    a, b, c = coefficients
    
    print(f"Best plane: z = {a:.4f}*x + {b:.4f}*y + {c:.4f}")
    
    # Calculate how good the fit is (R-squared)
    z_predicted = a * np.array(x_data) + b * np.array(y_data) + c
    ss_res = np.sum((z - z_predicted) ** 2)  # Sum of squared residuals
    ss_tot = np.sum((z - np.mean(z)) ** 2)   # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"R-squared (goodness of fit): {r_squared:.4f}")
    print("(1.0 = perfect fit, 0.0 = no fit)")
    
    return a, b, c, r_squared


def plot_3d_regression(x_data, y_data, z_data, a, b, c):
    """
    Create a 3D visualization of multiple regression
    Shows data points and the best-fit plane
    """
    print("\n📊 Creating 3D graph...")
    
    # Create 3D figure
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the actual data points as red dots
    ax.scatter(x_data, y_data, z_data, color='red', s=100, 
               label='Data Points', alpha=0.8)
    
    # Create a mesh grid for the plane
    # This makes a grid of x and y values
    x_range = np.linspace(min(x_data) - 1, max(x_data) + 1, 20)
    y_range = np.linspace(min(y_data) - 1, max(y_data) + 1, 20)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    
    # Calculate z values for the plane: z = a*x + b*y + c
    Z_grid = a * X_grid + b * Y_grid + c
    
    # Plot the plane (semi-transparent blue surface)
    ax.plot_surface(X_grid, Y_grid, Z_grid, alpha=0.3, color='blue',
                    label=f'Plane: z = {a:.2f}x + {b:.2f}y + {c:.2f}')
    
    # Add labels
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title('3D Multiple Linear Regression', fontsize=14, fontweight='bold')
    
    # Add legend (workaround because 3D plots don't show legend easily)
    ax.text2D(0.05, 0.95, f'Plane: z = {a:.2f}x + {b:.2f}y + {c:.2f}', 
              transform=ax.transAxes, fontsize=10, 
              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()
    
    print("✅ 3D graph displayed!")


# ========================================
# GUI APPLICATION USING TKINTER
# ========================================

class NumericalMethodsGUI:
    """
    Main GUI class - creates windows and buttons
    """
    
    def __init__(self, root):
        """
        Initialize the GUI
        root = the main window
        """
        self.root = root
        self.root.title("Numerical Methods Learning Tool")
        self.root.geometry("800x600")
        
        # Create main title
        title_label = tk.Label(root, 
                              text="NUMERICAL METHODS LEARNING TOOL",
                              font=("Arial", 16, "bold"),
                              pady=20)
        title_label.pack()
        
        # Create button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # Add buttons for each method
        self.create_buttons(button_frame)
        
        # Create output text area (shows results)
        output_label = tk.Label(root, text="Output:", font=("Arial", 12, "bold"))
        output_label.pack()
        
        self.output_text = scrolledtext.ScrolledText(root, 
                                                      width=90, 
                                                      height=20,
                                                      font=("Courier", 10))
        self.output_text.pack(pady=10)
    
    def create_buttons(self, frame):
        """Create all the menu buttons"""
        
        # Button 1: Gaussian Elimination
        btn1 = tk.Button(frame, 
                        text="1. Gaussian Elimination",
                        command=self.gaussian_window,
                        width=30,
                        height=2,
                        bg="#4CAF50",
                        fg="white",
                        font=("Arial", 11, "bold"))
        btn1.grid(row=0, column=0, padx=10, pady=10)
        
        # Button 2: Differentiation
        btn2 = tk.Button(frame,
                        text="2. Numerical Differentiation",
                        command=self.differentiation_window,
                        width=30,
                        height=2,
                        bg="#2196F3",
                        fg="white",
                        font=("Arial", 11, "bold"))
        btn2.grid(row=0, column=1, padx=10, pady=10)
        
        # Button 3: Linear Regression
        btn3 = tk.Button(frame,
                        text="3. Linear Regression",
                        command=self.regression_window,
                        width=30,
                        height=2,
                        bg="#FF9800",
                        fg="white",
                        font=("Arial", 11, "bold"))
        btn3.grid(row=1, column=0, padx=10, pady=10)
        
        # Button 4: Polynomial Regression
        btn4 = tk.Button(frame,
                        text="4. Polynomial Regression",
                        command=self.polynomial_window,
                        width=30,
                        height=2,
                        bg="#9C27B0",
                        fg="white",
                        font=("Arial", 11, "bold"))
        btn4.grid(row=1, column=1, padx=10, pady=10)
        
        # Button 5: 3D Multiple Regression (NEW!)
        btn5 = tk.Button(frame,
                        text="5. 3D Multiple Regression",
                        command=self.multiple_regression_window,
                        width=30,
                        height=2,
                        bg="#E91E63",
                        fg="white",
                        font=("Arial", 11, "bold"))
        btn5.grid(row=2, column=0, padx=10, pady=10)
        
        # Button 6: Exit
        btn_exit = tk.Button(frame,
                            text="Exit",
                            command=self.root.quit,
                            width=30,
                            height=2,
                            bg="#F44336",
                            fg="white",
                            font=("Arial", 11, "bold"))
        btn_exit.grid(row=2, column=1, padx=10, pady=10)
    
    def log_output(self, text):
        """Write text to the output area"""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)  # Scroll to bottom
    
    def clear_output(self):
        """Clear the output area"""
        self.output_text.delete(1.0, tk.END)
    
    # ========================================
    # WINDOW 1: GAUSSIAN ELIMINATION (FIXED - NOW UP TO 5)
    # ========================================
    
    def gaussian_window(self):
        """Open window for Gaussian Elimination - UP TO 5 VARIABLES"""
        self.clear_output()
        self.log_output("=== GAUSSIAN ELIMINATION ===\n")
        
        # Create new window with scrollbar
        window = tk.Toplevel(self.root)
        window.title("Gaussian Elimination")
        window.geometry("600x500")
        
        tk.Label(window, text="Solve System of Equations (2-5 variables)", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Number of variables
        tk.Label(window, text="Number of variables (2-5):").pack()
        num_vars = tk.Entry(window)
        num_vars.pack()
        
        # Create a frame with scrollbar for inputs
        canvas = tk.Canvas(window, height=300)
        scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        entries = []  # Store entry boxes
        
        def create_inputs():
            """Create input boxes based on number of variables"""
            # Clear previous inputs
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            entries.clear()
            
            try:
                n = int(num_vars.get())
                if n < 2 or n > 5:
                    messagebox.showerror("Error", "Enter 2 to 5 variables!")
                    return
                
                # Create input boxes for each equation
                for i in range(n):
                    tk.Label(scrollable_frame, 
                            text=f"Equation {i+1}:",
                            font=("Arial", 10, "bold")).grid(row=i, column=0, pady=5, sticky="w")
                    
                    row_entries = []
                    for j in range(n):
                        var_label = chr(120 + j)  # x, y, z, w, v
                        tk.Label(scrollable_frame, text=f"{var_label}:").grid(row=i, column=j*2+1)
                        entry = tk.Entry(scrollable_frame, width=8)
                        entry.grid(row=i, column=j*2+2, padx=2)
                        row_entries.append(entry)
                    
                    tk.Label(scrollable_frame, text="=").grid(row=i, column=n*2+1)
                    answer_entry = tk.Entry(scrollable_frame, width=8)
                    answer_entry.grid(row=i, column=n*2+2)
                    row_entries.append(answer_entry)
                    
                    entries.append(row_entries)
                
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number!")
        
        def solve():
            """Solve the system"""
            try:
                n = len(entries)
                equations = []
                answers = []
                
                for row in entries:
                    coeffs = [float(entry.get()) for entry in row[:-1]]
                    answer = float(row[-1].get())
                    equations.append(coeffs)
                    answers.append(answer)
                
                solution = solve_gaussian_quick(equations, answers)
                
                if solution is not None:
                    self.log_output("\nSOLUTION:")
                    for i, val in enumerate(solution):
                        var = chr(120 + i)
                        self.log_output(f"  {var} = {val:.4f}")
                    messagebox.showinfo("Success", "Solution found! Check output below.")
                else:
                    messagebox.showerror("Error", "Cannot solve system!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        # Buttons at bottom
        button_frame = tk.Frame(window)
        button_frame.pack(side="bottom", pady=10)
        
        tk.Button(button_frame, text="Create Input Fields", 
                 command=create_inputs, bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Solve", 
                 command=solve, bg="#2196F3", fg="white").pack(side="left", padx=5)
    
    # ========================================
    # WINDOW 2: DIFFERENTIATION
    # ========================================
    
    def differentiation_window(self):
        """Open window for Differentiation"""
        self.clear_output()
        self.log_output("=== NUMERICAL DIFFERENTIATION ===\n")
        self.log_output("Function: f(x) = x² + 2x + 1\n")
        
        window = tk.Toplevel(self.root)
        window.title("Numerical Differentiation")
        window.geometry("300x250")
        
        tk.Label(window, text="Numerical Differentiation", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(window, text="x value:").pack()
        x_entry = tk.Entry(window)
        x_entry.pack()
        
        tk.Label(window, text="Step size h:").pack()
        h_entry = tk.Entry(window)
        h_entry.insert(0, "0.01")
        h_entry.pack()
        
        def calculate():
            try:
                x = float(x_entry.get())
                h = float(h_entry.get())
                
                # Simple function: f(x) = x² + 2x + 1
                f = lambda x: x**2 + 2*x + 1
                
                # Forward difference
                forward = (f(x + h) - f(x)) / h
                # Central difference
                central = (f(x + h) - f(x - h)) / (2 * h)
                # Exact
                exact = 2*x + 2
                
                self.log_output(f"\nx = {x}, h = {h}")
                self.log_output(f"Exact derivative: {exact:.6f}")
                self.log_output(f"Forward difference: {forward:.6f}")
                self.log_output(f"Central difference: {central:.6f}")
                
                messagebox.showinfo("Done", "Results shown in output!")
                
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        tk.Button(window, text="Calculate", command=calculate,
                 bg="#2196F3", fg="white").pack(pady=10)
    
    # ========================================
    # WINDOW 3: LINEAR REGRESSION (FIXED - CUSTOM INPUT)
    # ========================================
    
    def regression_window(self):
        """Open window for Linear Regression with custom input"""
        self.clear_output()
        self.log_output("=== LINEAR REGRESSION ===\n")
        
        window = tk.Toplevel(self.root)
        window.title("Linear Regression")
        window.geometry("500x400")
        
        tk.Label(window, text="Linear Regression", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame for data input
        data_frame = tk.Frame(window)
        data_frame.pack(pady=10)
        
        tk.Label(data_frame, text="Enter your data points:").grid(row=0, column=0, columnspan=2)
        tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
        x_entry = tk.Entry(data_frame, width=30)
        x_entry.grid(row=1, column=1, padx=5)
        x_entry.insert(0, "1,2,3,4,5")  # Example default
        
        tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
        y_entry = tk.Entry(data_frame, width=30)
        y_entry.grid(row=2, column=1, padx=5)
        y_entry.insert(0, "2,4,5,4,5")  # Example default
        
        def process_data():
            try:
                # Parse input
                x_str = x_entry.get().strip()
                y_str = y_entry.get().strip()
                
                x = [float(val.strip()) for val in x_str.split(',')]
                y = [float(val.strip()) for val in y_str.split(',')]
                
                if len(x) != len(y):
                    messagebox.showerror("Error", "X and Y must have same number of points!")
                    return
                
                if len(x) < 2:
                    messagebox.showerror("Error", "Need at least 2 data points!")
                    return
                
                # Calculate regression
                m, b = analytical_regression(x, y)
                
                self.log_output(f"Data points: {list(zip(x, y))}")
                self.log_output(f"Best line: y = {m:.4f}x + {b:.4f}")
                
                # Plot
                plt.figure(figsize=(8, 6))
                plt.scatter(x, y, color='red', s=100, label='Data')
                x_line = np.linspace(min(x)-1, max(x)+1, 100)
                y_line = m * x_line + b
                plt.plot(x_line, y_line, 'b-', linewidth=2, 
                        label=f'y = {m:.2f}x + {b:.2f}')
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('Linear Regression')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.show()
                
                messagebox.showinfo("Done", "Graph displayed!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        tk.Button(window, text="Calculate & Plot",
                 command=process_data, bg="#FF9800", fg="white",
                 width=20, height=2).pack(pady=20)
    
    # ========================================
    # WINDOW 4: POLYNOMIAL REGRESSION (FIXED - CUSTOM INPUT)
    # ========================================
    
    def polynomial_window(self):
        """Open window for Polynomial Regression with custom input"""
        self.clear_output()
        self.log_output("=== POLYNOMIAL REGRESSION ===\n")
        
        window = tk.Toplevel(self.root)
        window.title("Polynomial Regression")
        window.geometry("500x450")
        
        tk.Label(window, text="Polynomial Regression", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame for data input
        data_frame = tk.Frame(window)
        data_frame.pack(pady=10)
        
        tk.Label(data_frame, text="Enter your data points:").grid(row=0, column=0, columnspan=2)
        tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
        x_entry = tk.Entry(data_frame, width=30)
        x_entry.grid(row=1, column=1, padx=5)
        x_entry.insert(0, "1,2,3,4,5")  # Example default
        
        tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
        y_entry = tk.Entry(data_frame, width=30)
        y_entry.grid(row=2, column=1, padx=5)
        y_entry.insert(0, "1,4,9,16,23")  # Example default (roughly x²)
        
        tk.Label(data_frame, text="Polynomial degree (1-4):").grid(row=3, column=0, sticky="e")
        degree_entry = tk.Entry(data_frame, width=30)
        degree_entry.grid(row=3, column=1, padx=5)
        degree_entry.insert(0, "2")
        
        def process_data():
            try:
                # Parse input
                x_str = x_entry.get().strip()
                y_str = y_entry.get().strip()
                degree = int(degree_entry.get().strip())
                
                x = [float(val.strip()) for val in x_str.split(',')]
                y = [float(val.strip()) for val in y_str.split(',')]
                
                if len(x) != len(y):
                    messagebox.showerror("Error", "X and Y must have same number of points!")
                    return
                
                if len(x) < degree + 1:
                    messagebox.showerror("Error", f"Need at least {degree+1} points for degree {degree}!")
                    return
                
                if degree < 1 or degree > 4:
                    messagebox.showerror("Error", "Degree must be 1-4!")
                    return
                
                self.log_output(f"Data points: {list(zip(x, y))}")
                
                # Plot with different degrees for comparison
                plt.figure(figsize=(10, 6))
                plt.scatter(x, y, color='black', s=100, label='Data', zorder=3)
                
                x_smooth = np.linspace(min(x)-0.5, max(x)+0.5, 100)
                
                # Plot the requested degree
                coeffs, poly = polynomial_regression_quick(x, y, degree)
                y_smooth = poly(x_smooth)
                plt.plot(x_smooth, y_smooth, color='blue', linewidth=2,
                        label=f'Degree {degree}', linestyle='-')
                self.log_output(f"Degree {degree}: {poly}")
                
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('Polynomial Regression')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.show()
                
                messagebox.showinfo("Done", "Graph displayed!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        tk.Button(window, text="Calculate & Plot",
                 command=process_data, bg="#9C27B0", fg="white",
                 width=20, height=2).pack(pady=20)
        
        tk.Label(window, text="Tip: Try degree=1 for line, degree=2 for parabola",
                font=("Arial", 9, "italic")).pack()
    
    # ========================================
    # WINDOW 5: 3D MULTIPLE REGRESSION (FIXED - CUSTOM INPUT)
    # ========================================
    
    def multiple_regression_window(self):
        """Open window for 3D Multiple Regression with custom input"""
        self.clear_output()
        self.log_output("=== 3D MULTIPLE REGRESSION ===\n")
        self.log_output("Predict Z from X and Y: z = a*x + b*y + c\n")
        
        window = tk.Toplevel(self.root)
        window.title("3D Multiple Regression")
        window.geometry("500x450")
        
        tk.Label(window, text="3D Multiple Regression", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(window, text="Find best plane through 3D points",
                font=("Arial", 10)).pack()
        
        # Frame for data input
        data_frame = tk.Frame(window)
        data_frame.pack(pady=10)
        
        tk.Label(data_frame, text="Enter your 3D data points:").grid(row=0, column=0, columnspan=2)
        tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
        x_entry = tk.Entry(data_frame, width=35)
        x_entry.grid(row=1, column=1, padx=5)
        x_entry.insert(0, "1000,1500,2000,2500,3000,1200,1800,2200")  # Example
        
        tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
        y_entry = tk.Entry(data_frame, width=35)
        y_entry.grid(row=2, column=1, padx=5)
        y_entry.insert(0, "5,10,3,15,8,2,12,7")  # Example
        
        tk.Label(data_frame, text="Z values (comma separated):").grid(row=3, column=0, sticky="e")
        z_entry = tk.Entry(data_frame, width=35)
        z_entry.grid(row=3, column=1, padx=5)
        z_entry.insert(0, "150,200,280,220,320,170,210,260")  # Example
        
        def process_data():
            try:
                # Parse input
                x_str = x_entry.get().strip()
                y_str = y_entry.get().strip()
                z_str = z_entry.get().strip()
                
                x = [float(val.strip()) for val in x_str.split(',')]
                y = [float(val.strip()) for val in y_str.split(',')]
                z = [float(val.strip()) for val in z_str.split(',')]
                
                if not (len(x) == len(y) == len(z)):
                    messagebox.showerror("Error", "X, Y, and Z must have same number of points!")
                    return
                
                if len(x) < 3:
                    messagebox.showerror("Error", "Need at least 3 data points!")
                    return
                
                self.log_output(f"Data points: {len(x)}")
                self.log_output(f"X range: {min(x):.2f} to {max(x):.2f}")
                self.log_output(f"Y range: {min(y):.2f} to {max(y):.2f}")
                self.log_output(f"Z range: {min(z):.2f} to {max(z):.2f}\n")
                
                # Perform regression
                a, b, c, r2 = multiple_regression_3d(x, y, z)
                
                self.log_output(f"\nBest plane: z = {a:.4f}*x + {b:.4f}*y + {c:.4f}")
                self.log_output(f"R-squared: {r2:.4f}")
                self.log_output("\nInterpretation:")
                self.log_output(f"- Each unit increase in X changes Z by {a:.4f}")
                self.log_output(f"- Each unit increase in Y changes Z by {b:.4f}")
                
                # Plot 3D
                plot_3d_regression(x, y, z, a, b, c)
                
                messagebox.showinfo("Done", "Check output and 3D graph!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        tk.Button(window, text="Calculate & Plot 3D",
                 command=process_data, bg="#E91E63", fg="white",
                 width=20, height=2).pack(pady=20)
        
        tk.Label(window, text="Example: House prices (size, age, price)\nOr any 3D relationship!",
                font=("Arial", 9, "italic")).pack(pady=5)


# ========================================
# START THE GUI APPLICATION
# ========================================

def main():
    """
    Start the GUI application
    """
    # Create the main window
    root = tk.Tk()
    
    # Create the application
    app = NumericalMethodsGUI(root)
    
    # Start the GUI loop (waits for user to click buttons)
    root.mainloop()


# Run the program
if __name__ == "__main__":
    main()