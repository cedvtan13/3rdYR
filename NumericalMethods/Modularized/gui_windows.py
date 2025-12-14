"""
GUI WINDOW HELPERS
Creates popup windows for each numerical method
Keeps the main GUI file cleaner
"""

import tkinter as tk
from tkinter import messagebox
from numerical_core import *
from plotting import *

# ========================================
# GAUSSIAN ELIMINATION WINDOW
# ========================================

def create_gaussian_window(parent_gui):
    """Create window for solving equations (2-5 variables)"""
    parent_gui.clear_output()
    parent_gui.log_output("=== GAUSSIAN ELIMINATION ===\n")
    
    window = tk.Toplevel(parent_gui.root)
    window.title("Gaussian Elimination")
    window.geometry("600x500")
    
    tk.Label(window, text="Solve System of Equations (2-5 variables)", 
            font=("Arial", 14, "bold")).pack(pady=10)
    
    # Number of variables input
    tk.Label(window, text="Number of variables (2-5):").pack()
    num_vars = tk.Entry(window)
    num_vars.pack()
    
    # Scrollable frame for equation inputs
    canvas = tk.Canvas(window, height=300)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    entries = []  # Store input boxes
    
    def create_inputs():
        """Create input fields based on number of variables"""
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        entries.clear()
        
        try:
            n = int(num_vars.get())
            if n < 2 or n > 5:
                messagebox.showerror("Error", "Enter 2 to 5 variables!")
                return
            
            # Create row for each equation
            for i in range(n):
                tk.Label(scrollable_frame, text=f"Equation {i+1}:",
                        font=("Arial", 10, "bold")).grid(row=i, column=0, pady=5, sticky="w")
                
                row_entries = []
                # Create input for each coefficient
                for j in range(n):
                    var_label = chr(120 + j)  # x, y, z, w, v
                    tk.Label(scrollable_frame, text=f"{var_label}:").grid(row=i, column=j*2+1)
                    entry = tk.Entry(scrollable_frame, width=8)
                    entry.grid(row=i, column=j*2+2, padx=2)
                    row_entries.append(entry)
                
                # Answer field
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
        """Solve the system of equations"""
        try:
            n = len(entries)
            equations = []
            answers = []
            
            # Get all coefficients and answers
            for row in entries:
                coeffs = [float(entry.get()) for entry in row[:-1]]
                answer = float(row[-1].get())
                equations.append(coeffs)
                answers.append(answer)
            
            # Solve using our function
            solution = solve_gaussian(equations, answers)
            
            if solution is not None:
                parent_gui.log_output("\nSOLUTION:")
                for i, val in enumerate(solution):
                    var = chr(120 + i)
                    parent_gui.log_output(f"  {var} = {val:.4f}")
                messagebox.showinfo("Success", "Solution found! Check output below.")
            else:
                messagebox.showerror("Error", "Cannot solve system!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    # Buttons
    button_frame = tk.Frame(window)
    button_frame.pack(side="bottom", pady=10)
    
    tk.Button(button_frame, text="Create Input Fields", 
             command=create_inputs, bg="#4CAF50", fg="white").pack(side="left", padx=5)
    tk.Button(button_frame, text="Solve", 
             command=solve, bg="#2196F3", fg="white").pack(side="left", padx=5)


# ========================================
# DIFFERENTIATION WINDOW
# ========================================

def create_differentiation_window(parent_gui):
    """Create window for numerical differentiation"""
    parent_gui.clear_output()
    parent_gui.log_output("=== NUMERICAL DIFFERENTIATION ===\n")
    parent_gui.log_output("Function: f(x) = x² + 2x + 1\n")
    
    window = tk.Toplevel(parent_gui.root)
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
            
            # Calculate using different methods
            forward = differentiate_function(x, h, 'forward')
            central = differentiate_function(x, h, 'central')
            exact = exact_derivative(x)
            
            parent_gui.log_output(f"\nx = {x}, h = {h}")
            parent_gui.log_output(f"Exact derivative: {exact:.6f}")
            parent_gui.log_output(f"Forward difference: {forward:.6f}")
            parent_gui.log_output(f"Central difference: {central:.6f}")
            
            messagebox.showinfo("Done", "Results shown in output!")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    tk.Button(window, text="Calculate", command=calculate,
             bg="#2196F3", fg="white").pack(pady=10)


# ========================================
# LINEAR REGRESSION WINDOW
# ========================================

def create_regression_window(parent_gui):
    """Create window for linear regression with custom input"""
    parent_gui.clear_output()
    parent_gui.log_output("=== LINEAR REGRESSION ===\n")
    
    window = tk.Toplevel(parent_gui.root)
    window.title("Linear Regression")
    window.geometry("500x400")
    
    tk.Label(window, text="Linear Regression", 
            font=("Arial", 14, "bold")).pack(pady=10)
    
    # Data input frame
    data_frame = tk.Frame(window)
    data_frame.pack(pady=10)
    
    tk.Label(data_frame, text="Enter your data points:").grid(row=0, column=0, columnspan=2)
    tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
    x_entry = tk.Entry(data_frame, width=30)
    x_entry.grid(row=1, column=1, padx=5)
    x_entry.insert(0, "1,2,3,4,5")
    
    tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
    y_entry = tk.Entry(data_frame, width=30)
    y_entry.grid(row=2, column=1, padx=5)
    y_entry.insert(0, "2,4,5,4,5")
    
    def process_data():
        try:
            # Parse comma-separated values
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
            m, b = linear_regression(x, y)
            
            parent_gui.log_output(f"Data points: {list(zip(x, y))}")
            parent_gui.log_output(f"Best line: y = {m:.4f}x + {b:.4f}")
            
            # Plot the result
            plot_linear_regression(x, y, m, b)
            
            messagebox.showinfo("Done", "Graph displayed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    tk.Button(window, text="Calculate & Plot",
             command=process_data, bg="#FF9800", fg="white",
             width=20, height=2).pack(pady=20)


# ========================================
# POLYNOMIAL REGRESSION WINDOW
# ========================================

def create_polynomial_window(parent_gui):
    """Create window for polynomial regression"""
    parent_gui.clear_output()
    parent_gui.log_output("=== POLYNOMIAL REGRESSION ===\n")
    
    window = tk.Toplevel(parent_gui.root)
    window.title("Polynomial Regression")
    window.geometry("500x450")
    
    tk.Label(window, text="Polynomial Regression", 
            font=("Arial", 14, "bold")).pack(pady=10)
    
    # Data input frame
    data_frame = tk.Frame(window)
    data_frame.pack(pady=10)
    
    tk.Label(data_frame, text="Enter your data points:").grid(row=0, column=0, columnspan=2)
    tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
    x_entry = tk.Entry(data_frame, width=30)
    x_entry.grid(row=1, column=1, padx=5)
    x_entry.insert(0, "1,2,3,4,5")
    
    tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
    y_entry = tk.Entry(data_frame, width=30)
    y_entry.grid(row=2, column=1, padx=5)
    y_entry.insert(0, "1,4,9,16,23")
    
    tk.Label(data_frame, text="Polynomial degree (1-4):").grid(row=3, column=0, sticky="e")
    degree_entry = tk.Entry(data_frame, width=30)
    degree_entry.grid(row=3, column=1, padx=5)
    degree_entry.insert(0, "2")
    
    def process_data():
        try:
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
            
            # Calculate polynomial regression
            coeffs, poly = polynomial_regression(x, y, degree)
            
            parent_gui.log_output(f"Data points: {list(zip(x, y))}")
            parent_gui.log_output(f"Degree {degree}: {poly}")
            
            # Plot the result
            plot_polynomial_regression(x, y, degree, poly)
            
            messagebox.showinfo("Done", "Graph displayed!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    tk.Button(window, text="Calculate & Plot",
             command=process_data, bg="#9C27B0", fg="white",
             width=20, height=2).pack(pady=20)
    
    tk.Label(window, text="Tip: Try degree=1 for line, degree=2 for parabola",
            font=("Arial", 9, "italic")).pack()


# ========================================
# 3D MULTIPLE REGRESSION WINDOW
# ========================================

def create_multiple_regression_window(parent_gui):
    """Create window for 3D multiple regression"""
    parent_gui.clear_output()
    parent_gui.log_output("=== 3D MULTIPLE REGRESSION ===\n")
    parent_gui.log_output("Predict Z from X and Y: z = a*x + b*y + c\n")
    
    window = tk.Toplevel(parent_gui.root)
    window.title("3D Multiple Regression")
    window.geometry("500x450")
    
    tk.Label(window, text="3D Multiple Regression", 
            font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Label(window, text="Find best plane through 3D points",
            font=("Arial", 10)).pack()
    
    # Data input frame
    data_frame = tk.Frame(window)
    data_frame.pack(pady=10)
    
    tk.Label(data_frame, text="Enter your 3D data points:").grid(row=0, column=0, columnspan=2)
    tk.Label(data_frame, text="X values (comma separated):").grid(row=1, column=0, sticky="e")
    x_entry = tk.Entry(data_frame, width=35)
    x_entry.grid(row=1, column=1, padx=5)
    x_entry.insert(0, "1000,1500,2000,2500,3000,1200,1800,2200")
    
    tk.Label(data_frame, text="Y values (comma separated):").grid(row=2, column=0, sticky="e")
    y_entry = tk.Entry(data_frame, width=35)
    y_entry.grid(row=2, column=1, padx=5)
    y_entry.insert(0, "5,10,3,15,8,2,12,7")
    
    tk.Label(data_frame, text="Z values (comma separated):").grid(row=3, column=0, sticky="e")
    z_entry = tk.Entry(data_frame, width=35)
    z_entry.grid(row=3, column=1, padx=5)
    z_entry.insert(0, "150,200,280,220,320,170,210,260")
    
    def process_data():
        try:
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
            
            parent_gui.log_output(f"Data points: {len(x)}")
            parent_gui.log_output(f"X range: {min(x):.2f} to {max(x):.2f}")
            parent_gui.log_output(f"Y range: {min(y):.2f} to {max(y):.2f}")
            parent_gui.log_output(f"Z range: {min(z):.2f} to {max(z):.2f}\n")
            
            # Perform 3D regression
            a, b, c, r2 = multiple_regression_3d(x, y, z)
            
            parent_gui.log_output(f"\nBest plane: z = {a:.4f}*x + {b:.4f}*y + {c:.4f}")
            parent_gui.log_output(f"R-squared: {r2:.4f}")
            parent_gui.log_output("\nInterpretation:")
            parent_gui.log_output(f"- Each unit increase in X changes Z by {a:.4f}")
            parent_gui.log_output(f"- Each unit increase in Y changes Z by {b:.4f}")
            
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