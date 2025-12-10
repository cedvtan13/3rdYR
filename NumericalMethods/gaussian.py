import numpy as np

def gaussian_elimination(A,B):
    n = len(B)

    # create augmented matrix
    Aug = np.hstack([A, B.reshape(-1, 1)]).astype(float)

    # forward elim
    for i in range(n):
        # pivot checking
        if Aug[i][i] == 0.0:
            print('Error, Divide by 0 detected...')
            return None
        
        for j in range(i + 1, n):
            ratio = Aug[j][i] / Aug[i][i]
            Aug[j] = Aug[j] - ratio*Aug[i] #ratio * row i subtracted by row j

    x = np.zeros(n)

    # this starts from last row then goes backward
    for i in range(n -1, -1, -1):
        x[i] = (Aug[i][n] - np.sum(Aug[i][i+1:n]*x[i+1:n])) / Aug[i][i] #(right side - sum of knowns) / coeff of unknown

    return x
