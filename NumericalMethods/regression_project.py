import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# ==========================================
# PART 1: NUMERICAL METHODS LOGIC
# ==========================================

class RegressionEngine:
    def __init__(self):
        self.weights = None
        self.cost_history = []
        
    def generate_dummy_data(self):
        """Generates random non-linear data for testing."""
        np.random.seed(42)
        X = 2 * np.random.rand(100, 1)
        # Create a cubic-like curve with noise
        y = 4 + 3 * X + 1.5 * X**2 - 0.5 * X**3 + np.random.randn(100, 1)
        return X, y

    def predict(self, X_poly, weights):
        return X_poly.dot(weights)

    # --- ANALYTICAL METHOD (Gaussian Elimination) ---
    def gaussian_elimination_manual(self, A, B):
        """
        Solves Ax = B using manual Gaussian Elimination (O(n^3)).
        Addresses Condition 1: Can handle 5x5 matrices (Degree 4).
        """
        n = len(B)
        # Combine into Augmented Matrix
        Aug = np.hstack([A, B.reshape(-1, 1)]).astype(float)
        
        # 1. Forward Elimination
        for i in range(n):
            if np.abs(Aug[i][i]) < 1e-10: # Simple pivot check
                continue 
            for j in range(i + 1, n):
                ratio = Aug[j][i] / Aug[i][i]
                Aug[j] = Aug[j] - ratio * Aug[i]
        
        # 2. Back Substitution
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = (Aug[i][n] - np.sum(Aug[i][i+1:n] * x[i+1:n])) / Aug[i][i]
            
        return x

    def solve_analytic(self, X_poly, y):
        # 1. Construct Normal Equations: (X^T * X) * w = (X^T * y)
        X_T = X_poly.T
        A = X_T.dot(X_poly)  # This becomes the 5x5 matrix for degree 4
        B = X_T.dot(y).flatten()
        
        start_time = time.time()
        self.weights = self.gaussian_elimination_manual(A, B)
        return time.time() - start_time

    # --- ITERATIVE METHOD (Gradient Descent) ---
    def compute_cost(self, weights, X, y):
        predictions = X.dot(weights)
        errors = predictions - y.flatten()
        return np.mean(errors ** 2)

    def numerical_gradient(self, weights, X, y, method="central", h=1e-5):
        """
        Addresses Condition 2: Computes gradient using specific numerical method.
        """
        gradients = np.zeros_like(weights)
        
        for i in range(len(weights)):
            # Create copies to nudge specific weight
            w_plus = weights.copy()
            w_minus = weights.copy()
            
            if method == "forward":
                w_plus[i] += h
                grad = (self.compute_cost(w_plus, X, y) - self.compute_cost(weights, X, y)) / h
                
            elif method == "backward":
                w_minus[i] -= h
                grad = (self.compute_cost(weights, X, y) - self.compute_cost(w_minus, X, y)) / h
                
            elif method == "central":
                w_plus[i] += h
                w_minus[i] -= h
                grad = (self.compute_cost(w_plus, X, y) - self.compute_cost(w_minus, X, y)) / (2 * h)
                
            gradients[i] = grad
            
        return gradients

    def solve_iterative(self, X_poly, y, lr=0.01, epochs=1000, diff_method="central"):
        n_samples, n_features = X_poly.shape
        self.weights = np.zeros(n_features) # Initialize weights to 0
        self.cost_history = []
        
        start_time = time.time()
        
        for _ in range(epochs):
            # Calculate Gradient using Selected Numerical Method
            grad = self.numerical_gradient(self.weights, X_poly, y, method=diff_method)
            
            # Update Weights
            self.weights -= lr * grad
            
            # Record Cost
            cost = self.compute_cost(self.weights, X_poly, y)
            self.cost_history.append(cost)
            
        return time.time() - start_time

# ==========================================
# PART 2: UI DESIGN (Tkinter)
# ==========================================

class RegressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPE 3108: Comparative Regression Engine")
        self.root.geometry("1100x700")
        
        self.engine = RegressionEngine()
        self.X_raw = None
        self.y_raw = None
        
        # --- Layout Containers ---
        # Left Panel: Controls
        self.left_panel = ttk.Frame(root, padding="15")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right Panel: Visualizations
        self.right_panel = ttk.Frame(root, padding="10")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self._setup_controls()
        self._setup_graphs()

    def _setup_controls(self):
        # 1. Data Section
        ttk.Label(self.left_panel, text="1. Data Source", font=("Arial", 10, "bold")).pack(anchor="w", pady=(0,5))
        
        btn_frame = ttk.Frame(self.left_panel)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Load CSV", command=self.load_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Gen. Random", command=self.generate_data).pack(side=tk.LEFT, padx=2)
        
        self.lbl_status = ttk.Label(self.left_panel, text="Status: No Data", foreground="red")
        self.lbl_status.pack(anchor="w", pady=5)
        
        ttk.Separator(self.left_panel, orient='horizontal').pack(fill='x', pady=10)

        # 2. Model Configuration
        ttk.Label(self.left_panel, text="2. Model Config", font=("Arial", 10, "bold")).pack(anchor="w")
        
        ttk.Label(self.left_panel, text="Polynomial Degree (1-5):").pack(anchor="w", pady=(5,0))
        self.degree_var = tk.IntVar(value=2)
        # Scale addresses Condition 1 (User selectable degree up to 5)
        tk.Scale(self.left_panel, from_=1, to=5, orient=tk.HORIZONTAL, variable=self.degree_var).pack(fill=tk.X)

        ttk.Separator(self.left_panel, orient='horizontal').pack(fill='x', pady=10)

        # 3. Method Selection
        ttk.Label(self.left_panel, text="3. Solver Method", font=("Arial", 10, "bold")).pack(anchor="w")
        
        self.method_var = tk.StringVar(value="analytic")
        r1 = ttk.Radiobutton(self.left_panel, text="Analytical (Gaussian)", variable=self.method_var, value="analytic", command=self.toggle_inputs)
        r2 = ttk.Radiobutton(self.left_panel, text="Iterative (Gradient Descent)", variable=self.method_var, value="iterative", command=self.toggle_inputs)
        r1.pack(anchor="w")
        r2.pack(anchor="w")

        # 4. Hyperparameters (Frame)
        self.param_frame = ttk.LabelFrame(self.left_panel, text="Iterative Parameters", padding="10")
        self.param_frame.pack(fill=tk.X, pady=10)

        ttk.Label(self.param_frame, text="Learning Rate:").pack(anchor="w")
        self.lr_entry = ttk.Entry(self.param_frame)
        self.lr_entry.insert(0, "0.0001")
        self.lr_entry.pack(fill=tk.X)

        ttk.Label(self.param_frame, text="Epochs:").pack(anchor="w")
        self.epochs_entry = ttk.Entry(self.param_frame)
        self.epochs_entry.insert(0, "1000")
        self.epochs_entry.pack(fill=tk.X)

        # --- CONDITION 2: Differentiation Method Selector ---
        ttk.Label(self.param_frame, text="Diff. Method:").pack(anchor="w", pady=(5,0))
        self.diff_method_var = tk.StringVar()
        self.diff_combo = ttk.Combobox(self.param_frame, textvariable=self.diff_method_var, state="readonly")
        self.diff_combo['values'] = ('central', 'forward', 'backward')
        self.diff_combo.current(0) # Default to Central
        self.diff_combo.pack(fill=tk.X)
        # ----------------------------------------------------

        self.toggle_inputs() # Set initial state

        # 5. Train Button
        self.btn_train = ttk.Button(self.left_panel, text="TRAIN MODEL", command=self.train_model, state="disabled")
        self.btn_train.pack(fill=tk.X, pady=20)

        # 6. Metrics Output
        self.lbl_rmse = ttk.Label(self.left_panel, text="RMSE: N/A", font=("Courier", 10))
        self.lbl_rmse.pack(anchor="w")
        self.lbl_time = ttk.Label(self.left_panel, text="Time: N/A", font=("Courier", 10))
        self.lbl_time.pack(anchor="w")

    def _setup_graphs(self):
        # Create Tabs
        self.tabs = ttk.Notebook(self.right_panel)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Regression Plot
        self.tab1 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Regression Fit")
        
        self.fig1, self.ax1 = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.tab1)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Tab 2: Convergence Plot
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab2, text="Convergence (Loss)")
        
        self.fig2, self.ax2 = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.tab2)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def toggle_inputs(self):
        """Enables/Disables inputs based on method selection."""
        if self.method_var.get() == "analytic":
            for child in self.param_frame.winfo_children():
                child.configure(state="disable")
        else:
            for child in self.param_frame.winfo_children():
                child.configure(state="normal")

    def generate_data(self):
        self.X_raw, self.y_raw = self.engine.generate_dummy_data()
        self.lbl_status.config(text="Status: Random Data Generated", foreground="green")
        self.btn_train.config(state="normal")
        self.plot_raw_data()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                self.X_raw = df.iloc[:, 0].values.reshape(-1, 1)
                self.y_raw = df.iloc[:, 1].values.reshape(-1, 1)
                self.lbl_status.config(text=f"Status: Loaded {file_path.split('/')[-1]}", foreground="green")
                self.btn_train.config(state="normal")
                self.plot_raw_data()
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def plot_raw_data(self):
        self.ax1.clear()
        self.ax1.scatter(self.X_raw, self.y_raw, color='blue', alpha=0.5, label='Raw Data')
        self.ax1.set_xlabel('X')
        self.ax1.set_ylabel('y')
        self.ax1.legend()
        self.canvas1.draw()

    def train_model(self):
        # 1. Prepare Polynomial Features manually
        degree = self.degree_var.get()
        X_poly = np.ones((len(self.X_raw), 1)) # Bias term (x^0)
        for d in range(1, degree + 1):
            X_poly = np.hstack((X_poly, self.X_raw ** d))

        elapsed_time = 0
        
        # 2. Run Selected Method
        if self.method_var.get() == "analytic":
            try:
                elapsed_time = self.engine.solve_analytic(X_poly, self.y_raw)
            except np.linalg.LinAlgError:
                messagebox.showerror("Math Error", "Singular Matrix encountered (Determinant is 0).")
                return
        else:
            try:
                lr = float(self.lr_entry.get())
                epochs = int(self.epochs_entry.get())
                diff_method = self.diff_method_var.get()
                elapsed_time = self.engine.solve_iterative(X_poly, self.y_raw, lr, epochs, diff_method)
            except ValueError:
                messagebox.showerror("Input Error", "Please check Learning Rate and Epochs.")
                return

        # 3. Update Metrics
        preds = self.engine.predict(X_poly, self.engine.weights)
        mse = np.mean((preds - self.y_raw.flatten()) ** 2)
        rmse = np.sqrt(mse)
        
        self.lbl_rmse.config(text=f"RMSE: {rmse:.5f}")
        self.lbl_time.config(text=f"Time: {elapsed_time:.4f} sec")

        # 4. Update Graphs
        # Regression Curve
        self.plot_raw_data() # Clear and redraw dots
        
        # Sort X for clean line plotting
        sort_idx = np.argsort(self.X_raw.flatten())
        X_sorted = self.X_raw[sort_idx]
        preds_sorted = preds[sort_idx]
        
        self.ax1.plot(X_sorted, preds_sorted, color='red', linewidth=2, label=f'Model (Deg {degree})')
        self.ax1.legend()
        self.canvas1.draw()

        # Convergence Plot (Only if Iterative)
        self.ax2.clear()
        if self.method_var.get() == "iterative":
            self.ax2.plot(self.engine.cost_history, color='green')
            self.ax2.set_title("Cost Function over Epochs")
            self.ax2.set_xlabel("Epoch")
            self.ax2.set_ylabel("MSE Cost")
            self.tabs.select(self.tab2) # Auto-switch to convergence tab
        else:
            self.ax2.text(0.5, 0.5, "Not applicable for Analytic Method", ha='center')
            self.tabs.select(self.tab1)
        self.canvas2.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = RegressionApp(root)
    root.mainloop()