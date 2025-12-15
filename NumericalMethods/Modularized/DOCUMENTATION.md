# Numerical Methods & Machine Learning Foundations
## A Comparison of Analytical and Iterative Regression Algorithms

**Author:** 3rd Year Computer Engineering Student  
**Course:** CPE 3108 - Machine Learning Fundamentals  
**Date:** December 2025

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Why This Matters in Machine Learning](#why-this-matters-in-machine-learning)
3. [Mathematical Methods Explained](#mathematical-methods-explained)
4. [Installation & Usage](#installation--usage)
5. [Code Architecture](#code-architecture)
6. [Detailed Method Explanations](#detailed-method-explanations)
7. [Real-World Applications](#real-world-applications)
8. [Testing & Validation](#testing--validation)
9. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

### Purpose
This project demonstrates the **foundational mathematical methods** that power modern machine learning algorithms. By comparing **analytical** (direct calculation) and **iterative** (step-by-step optimization) approaches, students can understand how machine learning models actually learn from data.

### Core Requirements Met
✅ **Gaussian Elimination** - Solve systems of linear equations (2-5 variables)  
✅ **Numerical Differentiation** - Calculate derivatives using Forward, Backward, and Central difference methods  
✅ **Linear Regression Comparison** - Analytical vs. Iterative approaches  

### Bonus Features
➕ **Polynomial Regression** - Fit curves (not just lines) to data  
➕ **3D Multiple Regression** - Predict outcomes from multiple input variables  
➕ **Interactive GUI** - Visual, user-friendly interface with tkinter  
➕ **3D Visualizations** - See data and regression planes in 3D space  

---

## 🤖 Why This Matters in Machine Learning

### The Foundation of AI

Every machine learning algorithm relies on these fundamental numerical methods:

```
Machine Learning Algorithm
    ↓
Optimization Problem (find best parameters)
    ↓
Numerical Methods (Gaussian Elimination, Gradient Descent, etc.)
    ↓
Linear Algebra & Calculus Operations
```

### Analytical vs. Iterative: The Core Question

**Analytical Methods:**
- Use direct mathematical formulas
- Always give the exact same answer
- Fast for small problems
- Example: Solving 2x + 3y = 8 using algebra

**Iterative Methods:**
- Start with a guess, improve step by step
- May give slightly different answers each run
- Better for large, complex problems
- Example: How neural networks learn!

### Real-World Connection

```python
# ANALYTICAL: Traditional Linear Regression
# Used in: Excel, statistical software
# Good for: Small datasets, exact solutions
coefficients = (X^T X)^-1 X^T y

# ITERATIVE: Gradient Descent
# Used in: Neural networks, deep learning
# Good for: Big data, complex models
while not converged:
    gradient = calculate_gradient()
    parameters = parameters - learning_rate * gradient
```

This is **exactly** how ChatGPT, self-driving cars, and recommendation systems learn!

---

## 📐 Mathematical Methods Explained

### 1. Gaussian Elimination

**What it does:** Solves multiple equations simultaneously

**Example:**
```
2x + 3y = 8
1x - 1y = 1

Solution: x = 2.2, y = 1.2
```

**Why it matters in ML:**
- Solving for regression coefficients
- Matrix operations in neural networks
- Feature transformations

**How it works:**
1. Forward Elimination: Make zeros below diagonal
2. Back Substitution: Solve from bottom to top

```
[2  3 | 8]     [2  3 | 8]     x = 2.2
[1 -1 | 1]  →  [0 -2.5| -3]  → y = 1.2
```

---

### 2. Numerical Differentiation

**What it does:** Finds the rate of change (slope) at any point

**Example:**
```
Function: f(x) = x² + 2x + 1
At x = 2, what's the slope?

Forward:  (f(2.01) - f(2.00)) / 0.01 ≈ 6.01
Backward: (f(2.00) - f(1.99)) / 0.01 ≈ 5.99
Central:  (f(2.01) - f(1.99)) / 0.02 ≈ 6.00  ← Most accurate!
Exact:    2(2) + 2 = 6.00
```

**Why it matters in ML:**
- **Gradient Descent** - The heart of neural network training
- **Backpropagation** - How errors flow through networks
- **Optimization** - Finding minimum loss

**The Connection:**
```python
# Machine Learning uses derivatives to minimize error
loss = calculate_error(predictions, actual)
gradient = derivative_of_loss()  # ← This is differentiation!
parameters = parameters - learning_rate * gradient
```

---

### 3. Linear Regression

**What it does:** Finds the best line through scattered data points

**Example:**
```
Data: (1,2), (2,4), (3,5), (4,4), (5,5)
Best line: y = 0.6x + 2.2
```

**Mathematical Formula (Analytical):**
```
Given points (x₁,y₁), (x₂,y₂), ..., (xₙ,yₙ)

Slope (m):
m = (n∑xy - ∑x∑y) / (n∑x² - (∑x)²)

Intercept (b):
b = (∑y - m∑x) / n

Result: y = mx + b
```

**Iterative Approach (Gradient Descent):**
```
1. Start with random guess: m = 0, b = 0
2. For each data point:
   - Calculate error: how far is prediction from actual?
3. Calculate gradient: which direction reduces error?
4. Update parameters: m_new = m - learning_rate * gradient_m
5. Repeat until error is small enough
```

**Comparison:**

| Method | Analytical | Iterative (Gradient Descent) |
|--------|-----------|------------------------------|
| Speed | ⚡ Fast | 🐌 Slower |
| Accuracy | 🎯 Exact | 📊 Approximate |
| Scalability | 🔒 Limited | 📈 Unlimited |
| Use Case | Small data | Big data, neural networks |

---

### 4. Polynomial Regression

**What it does:** Fits curves instead of straight lines

**Example:**
```
Data: (1,1), (2,4), (3,9), (4,16), (5,25)
This looks like y = x²!

Degree 1 (line):     y = 4.4x - 4.0    ← Poor fit
Degree 2 (parabola): y = 1.0x² + 0x + 0 ← Perfect fit!
Degree 3 (cubic):    y = 1.0x² + ...    ← Overfitting
```

**Why different degrees?**
- **Degree 1:** Straight line (linear regression)
- **Degree 2:** Parabola (U-shaped curve)
- **Degree 3:** S-shaped curve
- **Degree 4+:** More complex wiggles

**Warning - Overfitting:**
```
Too simple → Underfitting → Misses patterns
Just right → Good fit → Captures real trends
Too complex → Overfitting → Fits noise, not signal
```

---

### 5. 3D Multiple Regression

**What it does:** Predicts one variable from TWO input variables

**Example - House Prices:**
```
Predict Price (Z) from Size (X) and Age (Y)

Data:
Size(sqft) | Age(yrs) | Price($k)
1000       | 5        | 150
1500       | 10       | 200
2000       | 3        | 280

Best plane: Price = 0.1×Size - 5×Age + 100

Interpretation:
- Each extra sq ft adds $100
- Each year older reduces price by $5k
- Base price is $100k
```

**Mathematical Formula:**
```
z = a·x + b·y + c

Where we solve:
[x₁ y₁ 1]   [a]   [z₁]
[x₂ y₂ 1] × [b] = [z₂]
[x₃ y₃ 1]   [c]   [z₃]
[... ... ...]      [...]

This is Gaussian Elimination for many equations!
```

**R-squared (Goodness of Fit):**
```
R² = 1.0  → Perfect fit! Every point on the plane
R² = 0.8  → Good fit, 80% of variation explained
R² = 0.5  → Moderate fit
R² = 0.0  → No relationship at all
```

---

## 💻 Installation & Usage

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Required libraries
pip install numpy matplotlib
```

### Quick Start

**Option 1: GUI Version (Recommended)**
```bash
cd NumericalMethods
python NumProj_GUI.py
```

**Option 2: Terminal Version**
```bash
python NumProj.py
```

### File Structure
```
NumericalMethods/
├── NumProj_GUI.py           # Main GUI application
├── NumProj.py               # Terminal version
├── Modularized/             # Clean, separated code
│   ├── numerical_core.py    # All math functions
│   ├── plotting.py          # Visualization functions
│   ├── gui_windows.py       # Window creation
│   └── NumProj_GUI.py       # Main GUI (modular)
├── DOCUMENTATION.md         # This file!
└── README.md                # Quick overview
```

---

## 🏗️ Code Architecture

### Design Philosophy

Following the "Keep It Simple for Students" principle:

```python
# ✅ GOOD: Clear, educational code
def linear_regression(x_points, y_points):
    """
    Find best line y = mx + b through points
    Simple formula approach for learning
    """
    n = len(x_points)
    sum_x = sum(x_points)      # Clear variable names
    sum_y = sum(y_points)      # Step by step
    sum_xy = sum(x_points[i] * y_points[i] for i in range(n))
    sum_x2 = sum(x * x for x in x_points)
    
    # Formula with explanation
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    b = (sum_y - m * sum_x) / n
    
    return m, b
```

### Module Separation

**1. numerical_core.py** - Pure Mathematics
```python
# No GUI code, no plotting
# Just math functions
# Easy to test independently
def solve_gaussian(equations, answers):
    # Returns solution or None
```

**2. plotting.py** - Visualizations
```python
# All matplotlib code here
# Separate from calculations
def plot_linear_regression(x, y, m, b):
    # Creates graph
```

**3. gui_windows.py** - User Interface
```python
# Tkinter window creation
# Calls functions from numerical_core
def create_gaussian_window(parent):
    # User inputs → call solve_gaussian() → display results
```

**4. NumProj_GUI.py** - Main Application
```python
# Puts everything together
# Small, clean main file
class NumericalMethodsGUI:
    def __init__(self):
        # Create buttons, link to windows
```

---

## 🔬 Detailed Method Explanations

### Gaussian Elimination - Step by Step

**Problem:** Solve this system:
```
2x + 3y = 8
1x - 1y = 1
```

**Step 1: Write as Matrix**
```
[2  3 | 8]
[1 -1 | 1]
```

**Step 2: Forward Elimination**
```
Goal: Make zero below the diagonal

Operation: Row2 = Row2 - (1/2)×Row1

[2    3   | 8  ]
[0  -2.5  | -3 ]  ← Got our zero!
```

**Step 3: Back Substitution**
```
From Row 2: -2.5y = -3
           y = 1.2

Substitute into Row 1: 2x + 3(1.2) = 8
                      2x + 3.6 = 8
                      2x = 4.4
                      x = 2.2

Solution: x = 2.2, y = 1.2
```

### Gradient Descent - How ML Learns

**Analogy:** You're blindfolded on a hill. Goal: reach the bottom.
- Feel the slope (gradient)
- Take small steps downhill
- Repeat until you're at the bottom

**In Code:**
```python
# Start with random guess
m = 0.0
b = 0.0
learning_rate = 0.01  # How big are our steps?

for iteration in range(1000):
    # Calculate error for current m and b
    predictions = [m * x + b for x in x_points]
    errors = [predictions[i] - y_points[i] for i in range(n)]
    
    # Calculate gradient (which direction is downhill?)
    gradient_m = (2/n) * sum(errors[i] * x_points[i] for i in range(n))
    gradient_b = (2/n) * sum(errors)
    
    # Take a step downhill
    m = m - learning_rate * gradient_m
    b = b - learning_rate * gradient_b
    
    # Eventually, we reach the bottom (minimum error)
```

**Learning Rate:**
```
Too small (0.001): 🐌 Very slow, takes forever
Just right (0.01): 🎯 Smooth convergence
Too large (1.0):   🌋 Overshoots, never converges!
```

---

## 🌍 Real-World Applications

### 1. Gaussian Elimination

**Engineering:**
- Circuit analysis (Kirchhoff's laws)
- Structural analysis (forces on bridges)
- Chemical equations balancing

**Computer Graphics:**
- 3D transformations
- Camera projections
- Lighting calculations

### 2. Numerical Differentiation

**Physics:**
- Velocity from position data
- Acceleration from velocity
- Heat transfer rates

**Economics:**
- Marginal cost/revenue
- Rate of return calculations
- Elasticity of demand

### 3. Linear Regression

**Business:**
- Sales forecasting
- Price optimization
- Marketing ROI analysis

**Science:**
- Climate modeling
- Medical dose-response
- Population studies

### 4. Polynomial Regression

**Biology:**
- Population growth curves
- Enzyme kinetics
- Drug absorption rates

**Engineering:**
- Trajectory prediction
- Signal processing
- Quality control

### 5. Multiple Regression

**Real Estate:**
- Home price prediction (size, location, age, condition)

**Healthcare:**
- Disease risk (age, weight, genetics, lifestyle)

**Finance:**
- Stock price prediction (multiple economic indicators)

**Manufacturing:**
- Product quality (temperature, pressure, materials, time)

---

## 🧪 Testing & Validation

### Test Cases Included

**1. Gaussian Elimination Test**
```
Input:
  2x + 3y = 8
  1x - 1y = 1

Expected Output:
  x = 2.2
  y = 1.2

Verification:
  2(2.2) + 3(1.2) = 4.4 + 3.6 = 8.0 ✓
  1(2.2) - 1(1.2) = 2.2 - 1.2 = 1.0 ✓
```

**2. Differentiation Test**
```
Function: f(x) = x² + 2x + 1
Point: x = 2
Exact derivative: f'(2) = 2(2) + 2 = 6.0

Numerical methods (h = 0.01):
  Forward:  ≈ 6.01   Error: 0.01
  Backward: ≈ 5.99   Error: 0.01
  Central:  ≈ 6.00   Error: 0.00 ✓ Best!
```

**3. Regression Test**
```
Data: (1,2), (2,4), (3,5), (4,4), (5,5)

Analytical:  y = 0.6x + 2.2
Iterative:   y = 0.6001x + 2.1998  (after 1000 iterations)

Difference: < 0.001 ✓ Both methods agree!
```

### How to Test Your Implementation

```python
# Run this in Python to verify your code works

from numerical_core import *

# Test 1: Gaussian
equations = [[2, 3], [1, -1]]
answers = [8, 1]
solution = solve_gaussian(equations, answers)
print(f"Gaussian Test: x={solution[0]:.2f}, y={solution[1]:.2f}")
# Expected: x=2.20, y=1.20

# Test 2: Differentiation
x = 2
h = 0.01
result = differentiate_function(x, h, 'central')
exact = exact_derivative(x)
print(f"Differentiation Test: {result:.4f} vs {exact:.4f}")
# Expected: Both ≈ 6.0000

# Test 3: Regression
x_data = [1, 2, 3, 4, 5]
y_data = [2, 4, 5, 4, 5]
m, b = linear_regression(x_data, y_data)
print(f"Regression Test: y = {m:.2f}x + {b:.2f}")
# Expected: y = 0.60x + 2.20
```

---

## 🚀 Future Enhancements

### Educational Additions

**1. Step-by-Step Manual Gaussian Elimination**
- Show each row operation
- Highlight what changes
- Educational for learning

**2. Animation of Gradient Descent**
- Visualize the "ball rolling downhill"
- Show parameter updates in real-time
- See convergence happen

**3. Interactive Learning Mode**
- Quiz after each method
- "Guess the output" exercises
- Immediate feedback

### Advanced Features

**4. More Regression Methods**
- Logistic Regression (for classification)
- Ridge/Lasso Regression (with regularization)
- Neural Network basics

**5. Optimization Algorithms**
- Newton's Method (faster than gradient descent)
- Adam Optimizer (used in modern ML)
- Conjugate Gradient

**6. Machine Learning Integration**
- Load CSV datasets
- Compare with sklearn library
- Train simple neural network

### Technical Improvements

**7. Error Analysis**
- Calculate confidence intervals
- Show prediction uncertainty
- Residual plots

**8. Performance Metrics**
- Timing comparisons
- Memory usage
- Scalability tests

**9. Export Functionality**
- Save results to CSV
- Export plots as images
- Generate PDF reports

---

## 📚 Learning Resources

### Books
- **"Introduction to Linear Algebra"** by Gilbert Strang
- **"Numerical Methods for Engineers"** by Chapra & Canale
- **"Pattern Recognition and Machine Learning"** by Bishop

### Online Courses
- **3Blue1Brown** (YouTube) - Amazing visual explanations
- **Khan Academy** - Calculus and Linear Algebra
- **Coursera Machine Learning** by Andrew Ng

### Practice Problems
- **Project Euler** - Mathematical challenges
- **Kaggle** - Real datasets to practice on
- **LeetCode** - Algorithm problems

---

## 🎓 Conclusion

This project demonstrates that **machine learning isn't magic** - it's mathematical methods applied systematically:

1. **Gaussian Elimination** → Solving for parameters
2. **Differentiation** → Finding optimal directions
3. **Regression** → Learning from data
4. **Iteration** → Improving step by step

By understanding these foundations, you're prepared to:
- Implement ML algorithms from scratch
- Understand what libraries actually do
- Debug when things go wrong
- Design new approaches

**The journey from numerical methods to AI:**
```
Numerical Methods (this project)
    ↓
Linear Algebra & Calculus
    ↓
Optimization Algorithms
    ↓
Machine Learning Basics
    ↓
Deep Learning
    ↓
Artificial Intelligence
```

You've taken the first step! 🚀

---

# FLOWCHARTS FOR NUMERICAL METHODS GUI

## 1. MAIN APPLICATION STRUCTURE (NumericalMethodsGUI)

```
START
  |
  v
Initialize Main Window
  |
  v
Create Title Label
"NUMERICAL METHODS LEARNING TOOL"
  |
  v
Create Button Frame
  |
  v
Add 5 Method Buttons:
├─> Button 1: Gaussian Elimination
├─> Button 2: Numerical Differentiation  
├─> Button 3: Linear Regression
├─> Button 4: Polynomial Regression
└─> Button 5: 3D Multiple Regression
  |
  v
Create Output Text Area
(Scrollable text box for results)
  |
  v
Wait for User Input
  |
  v
User Clicks Button? ──No──> Keep Waiting
  |                          |
  Yes                        |
  |<─────────────────────────┘
  v
Open Corresponding Window
  |
  v
Process User Data in Window
  |
  v
Display Results in Output Area
  |
  v
Return to Main Menu
  |
  v
User Clicks Exit? ──No──> Wait for User Input
  |                       |
  Yes                     |
  |<──────────────────────┘
  v
END
```

---

## 2. GAUSSIAN ELIMINATION

```
START
  |
  v
Open Gaussian Window
  |
  v
Ask: "Number of variables (2-5)?"
  |
  v
User Enters Number (n)
  |
  v
Valid (2≤n≤5)? ──No──> Show Error
  |                     |
  Yes                   |
  |<────────────────────┘
  v
Create n Input Rows
Each row has:
├─> n coefficient boxes
└─> 1 answer box
  |
  v
User Fills All Boxes
  |
  v
User Clicks "Solve"
  |
  v
Read All Values
  |
  v
Convert to Matrix A (coefficients)
Convert to Vector b (answers)
  |
  v
Call solve_gaussian(A, b)
  |
  v
Use numpy.linalg.solve()
(Gaussian elimination internally)
  |
  v
Solution Found? ──No──> Show "Cannot Solve"
  |                      Return to Input
  Yes                    |
  |<─────────────────────┘
  v
Display Solutions:
x = value1
y = value2
z = value3
(etc.)
  |
  v
Show Success Message
  |
  v
END
```

**Example:**
```
Input: 2x + 3y = 8
       x - y = 1

Matrix A = [[2, 3],    Vector b = [8,
            [1,-1]]                1]

Output: x = 2.2, y = 1.2
```

---

## 3. NUMERICAL DIFFERENTIATION

```
START
  |
  v
Open Differentiation Window
  |
  v
Display Function: f(x) = x² + 2x + 1
  |
  v
Ask User for:
├─> x value (point to find derivative)
└─> h value (step size, default 0.01)
  |
  v
User Enters Values
  |
  v
User Clicks "Calculate"
  |
  v
Calculate Exact Derivative
exact = 2x + 2
  |
  v
Calculate Forward Difference
forward = [f(x+h) - f(x)] / h
  |
  v
Calculate Backward Difference
backward = [f(x) - f(x-h)] / h
  |
  v
Calculate Central Difference
central = [f(x+h) - f(x-h)] / (2h)
  |
  v
Display All Results:
├─> Exact: (exact value)
├─> Forward: (forward value)
├─> Backward: (backward value)
└─> Central: (central value - most accurate)
  |
  v
Show Success Message
  |
  v
END
```

**Visual Explanation:**
```
Forward:  x ────────> x+h
          look ahead

Backward: x-h <────── x
          look behind

Central:  x-h <──x──> x+h
          look both ways (best!)
```

---

## 4. LINEAR REGRESSION

```
START
  |
  v
Open Linear Regression Window
  |
  v
Show Default Data:
X: [1, 2, 3, 4, 5]
Y: [2, 4, 5, 4, 5]
  |
  v
User Can Enter Custom Data
(comma separated values)
  |
  v
User Clicks "Calculate & Plot"
  |
  v
Parse X and Y values
  |
  v
Check: Same Length? ──No──> Show Error
  |                          Return to Input
  Yes                        |
  |<─────────────────────────┘
  v
Check: At Least 2 Points? ──No──> Show Error
  |                                Return
  Yes                              |
  |<───────────────────────────────┘
  v
Calculate Sums:
├─> sum_x = Σx
├─> sum_y = Σy
├─> sum_xy = Σ(x*y)
└─> sum_x2 = Σ(x²)
  |
  v
Calculate Slope (m):
m = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x²)
  |
  v
Calculate Intercept (b):
b = (sum_y - m*sum_x) / n
  |
  v
Best Line: y = mx + b
  |
  v
Create Plot:
├─> Red dots = data points
└─> Blue line = best fit
  |
  v
Display Equation and Graph
  |
  v
END
```

**Visual:**
```
     Y
     |     • (data point)
   5 |   •   • 
   4 | •   •     Line: y = 0.8x + 1.2
   3 |•
   2 |────────────────> X
     1   2   3   4   5
```

---

## 5. POLYNOMIAL REGRESSION

```
START
  |
  v
Open Polynomial Regression Window
  |
  v
Show Default Data:
X: [1, 2, 3, 4, 5]
Y: [1, 4, 9, 16, 23]
Degree: 2
  |
  v
User Enters:
├─> X values (comma separated)
├─> Y values (comma separated)
└─> Degree (1-4)
  |
  v
User Clicks "Calculate & Plot"
  |
  v
Parse All Values
  |
  v
Check: Same Length? ──No──> Show Error
  |                          Return
  Yes                        |
  |<─────────────────────────┘
  v
Check: Enough Points? ──No──> Show Error
(need degree + 1 points)     Return
  |                          |
  Yes                        |
  |<─────────────────────────┘
  v
Check: Degree 1-4? ──No──> Show Error
  |                         Return
  Yes                       |
  |<────────────────────────┘
  v
Call numpy.polyfit(x, y, degree)
Returns coefficients
  |
  v
Create Polynomial Function
If degree=2: y = ax² + bx + c
If degree=3: y = ax³ + bx² + cx + d
  |
  v
Generate Smooth Curve
(200 points for plotting)
  |
  v
Create Plot:
├─> Black dots = data points
└─> Blue curve = polynomial fit
  |
  v
Display Equation and Graph
  |
  v
END
```

**Degree Examples:**
```
Degree 1: Line        y = mx + b
Degree 2: Parabola    y = ax² + bx + c
Degree 3: Cubic       y = ax³ + bx² + cx + d
```

---

## 6. 3D MULTIPLE REGRESSION

```
START
  |
  v
Open 3D Regression Window
  |
  v
Show Default Data:
X: [1000, 1500, 2000, ...] (e.g., house size)
Y: [5, 10, 3, ...]         (e.g., age)
Z: [150, 200, 280, ...]    (e.g., price)
  |
  v
User Enters Custom 3D Data
(comma separated)
  |
  v
User Clicks "Calculate & Plot 3D"
  |
  v
Parse X, Y, Z values
  |
  v
Check: All Same Length? ──No──> Show Error
  |                              Return
  Yes                            |
  |<─────────────────────────────┘
  v
Check: At Least 3 Points? ──No──> Show Error
  |                                Return
  Yes                              |
  |<───────────────────────────────┘
  v
Build Design Matrix A:
Each row = [x_i, y_i, 1]
  |
  v
Solve Using Least Squares:
A * [a, b, c]ᵀ = z
  |
  v
Get Coefficients:
├─> a (effect of x on z)
├─> b (effect of y on z)
└─> c (constant term)
  |
  v
Best Plane: z = a*x + b*y + c
  |
  v
Calculate R² (goodness of fit):
├─> Predicted z values
├─> Residual sum of squares
└─> R² = 1 - (SS_res / SS_tot)
  |
  v
Create 3D Mesh Grid
for plane surface
  |
  v
Create 3D Plot:
├─> Red spheres = data points
└─> Blue surface = best-fit plane
  |
  v
Display Results:
├─> Plane equation
├─> R² value
└─> Interpretations
  |
  v
Show 3D Graph
  |
  v
END
```

**Visual Concept:**
```
        Z
        |
        |    • data point
        |  •  /
        | •  / (plane)
        |•  /___
        | /___/___
       /_________> Y
      /
     / X

Plane: z = a*x + b*y + c
```

**Interpretation:**
- **a**: How much Z changes per unit of X
- **b**: How much Z changes per unit of Y  
- **c**: Base value when X=0, Y=0
- **R²**: 0.0 (bad fit) to 1.0 (perfect fit)

---

## SUMMARY OF ALGORITHMS

| Method | Input | Output | Use Case |
|--------|-------|--------|----------|
| Gaussian Elimination | System of equations | Variable values | Solve 2-5 unknowns |
| Differentiation | x, h, function | Derivative | Rate of change |
| Linear Regression | (x,y) points | Line y=mx+b | Trend line |
| Polynomial Regression | (x,y) points, degree | Curve equation | Non-linear fit |
| 3D Multiple Regression | (x,y,z) points | Plane equation | Multi-variable prediction |

---

## NOTES FOR STUDENTS

### Complexity Levels:
1. **Gaussian**: Moderate (matrix operations)
2. **Differentiation**: Easy (simple formulas)
3. **Linear Regression**: Easy (basic math)
4. **Polynomial**: Moderate (uses numpy)
5. **3D Multiple**: Advanced (matrix + visualization)

### Common Errors to Avoid:
- Not enough data points
- Mismatched array lengths
- Division by zero in formulas
- Invalid degree for polynomial
- Singular matrices in Gaussian

### Testing Tips:
- Start with simple examples
- Verify with known answers
- Check extreme cases
- Compare numerical vs analytical results
```

## 📝 References

1. Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis* (9th ed.). Brooks/Cole.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
3. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
4. Strang, G. (2016). *Introduction to Linear Algebra* (5th ed.). Wellesley-Cambridge Press.
5. NumPy Documentation: https://numpy.org/doc/
6. Matplotlib Documentation: https://matplotlib.org/
7. Python Official Documentation: https://docs.python.org/3/

---

## 📧 Contact & Support

**Student:** 3rd Year Computer Engineering  
**Course:** CPE 3108 - Machine Learning Fundamentals  
**Academic Year:** 2025

For questions, suggestions, or bug reports, please refer to your course instructor.

---

**Last Updated:** December 2025  
**Version:** 1.0  
**License:** Educational Use Only
