"""
NUMERICAL METHODS GUI APPLICATION - MAIN FILE
"""

import tkinter as tk
from tkinter import scrolledtext
from gui_windows import *

# ========================================
# MAIN GUI CLASS
# ========================================

class NumericalMethodsGUI:
    """
    Main GUI application class
    Creates the main window with buttons
    """
    
    def __init__(self, root):
        """Initialize the main GUI window"""
        self.root = root
        self.root.title("Numerical Methods Learning Tool")
        self.root.geometry("800x600")
        
        # Create title
        title_label = tk.Label(root, 
                              text="NUMERICAL METHODS LEARNING TOOL",
                              font=("Arial", 16, "bold"),
                              pady=20)
        title_label.pack()
        
        # Create button area
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        self.create_buttons(button_frame)
        
        # Create output text area
        output_label = tk.Label(root, text="Output:", font=("Arial", 12, "bold"))
        output_label.pack()
        
        self.output_text = scrolledtext.ScrolledText(root, 
                                                      width=90, 
                                                      height=20,
                                                      font=("Courier", 10))
        self.output_text.pack(pady=10)
    
    def create_buttons(self, frame):
        """Create all menu buttons"""
        
        # Button 1: Gaussian Elimination
        btn1 = tk.Button(frame, 
                        text="1. Gaussian Elimination",
                        command=lambda: create_gaussian_window(self),
                        width=30, height=2,
                        bg="#4CAF50", fg="white",
                        font=("Arial", 11, "bold"))
        btn1.grid(row=0, column=0, padx=10, pady=10)
        
        # Button 2: Differentiation
        btn2 = tk.Button(frame,
                        text="2. Numerical Differentiation",
                        command=lambda: create_differentiation_window(self),
                        width=30, height=2,
                        bg="#2196F3", fg="white",
                        font=("Arial", 11, "bold"))
        btn2.grid(row=0, column=1, padx=10, pady=10)
        
        # Button 3: Linear Regression
        btn3 = tk.Button(frame,
                        text="3. Linear Regression",
                        command=lambda: create_regression_window(self),
                        width=30, height=2,
                        bg="#FF9800", fg="white",
                        font=("Arial", 11, "bold"))
        btn3.grid(row=1, column=0, padx=10, pady=10)
        
        # Button 4: Polynomial Regression
        btn4 = tk.Button(frame,
                        text="4. Polynomial Regression",
                        command=lambda: create_polynomial_window(self),
                        width=30, height=2,
                        bg="#9C27B0", fg="white",
                        font=("Arial", 11, "bold"))
        btn4.grid(row=1, column=1, padx=10, pady=10)
        
        # Button 5: 3D Multiple Regression
        btn5 = tk.Button(frame,
                        text="5. 3D Multiple Regression",
                        command=lambda: create_multiple_regression_window(self),
                        width=30, height=2,
                        bg="#E91E63", fg="white",
                        font=("Arial", 11, "bold"))
        btn5.grid(row=2, column=0, padx=10, pady=10)
        
        # Button 6: Exit
        btn_exit = tk.Button(frame,
                            text="Exit",
                            command=self.root.quit,
                            width=30, height=2,
                            bg="#F44336", fg="white",
                            font=("Arial", 11, "bold"))
        btn_exit.grid(row=2, column=1, padx=10, pady=10)
    
    def log_output(self, text):
        """Write text to output area"""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """Clear output area"""
        self.output_text.delete(1.0, tk.END)


# ========================================
# START THE APPLICATION
# ========================================

def main():
    """Start the GUI application"""
    root = tk.Tk()
    app = NumericalMethodsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()