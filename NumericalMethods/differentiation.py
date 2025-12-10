import numpy as np

# this is for the calculation of the Mean Squared Error, serves as the 'f(x)'
def compute_cost(weights, X, y):
    predictions = X.dot(weights)
    errors = predictions - y
    return np.mean(errors ** 2)

# this calculates the cost of function with respect of each weight depending on the numerical method the user uses.
def numerical_gradients(weights, X, y, method = "central", h=1e-5):
    gradients = np.zeros_like(weights)

    for i in range(len(weights)):
        
        weights_plus = weights.copy()
        weights_minus = weights.copy()

        if method == "forward":
            # f'(x) = (f(x+deltax)+ f(x)) / (deltax)
            weights_plus[i] += h
            cost_plus = compute_cost(weights_plus, X, y)
            cost_current = compute_cost(weights, X, y)
            gradients[i] = (cost_plus - cost_current) / h

        elif method == "backward":
            # f'(x) = (f(x) - f(x - deltax)) / (deltax)
            weights_plus[i] -= h
            cost_plus       = compute_cost(weights, X, y)
            cost_minus      = compute_cost(weights_minus, X, y)
            gradients[i]    = (cost_current - cost_minus) / h

        elif method == "centralized":
            # f'(x) = (f(x + deltax) - f(x - deltax)) / 2(deltax)
            weights_plus[i] += h 
            weights_minus[i] -= h
            cost_plus = compute_cost(weights_plus, X, y)
            cost_minus = compute_cost(weights_minus, X, y)
            gradients[i]    = (cost_plus - cost_minus) / (2*h)

    return gradients