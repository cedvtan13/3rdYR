import numpy as np

def main():
    print("Welcome to the Machine Learning Library Comparison Tool!")
    while True:
        print("\nSelect an option:")
        print("1. Gaussian Elimination")
        print("2. Numerical Differentiation")
        print("3. Compare Regression Algorithms")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            gaussian_elimination()
        elif choice == '2':
            numerical_differentiation()
        elif choice == '3':
            compare_regression_algorithms()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()