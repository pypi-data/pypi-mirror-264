import numpy as np

def sum_error_square(x:np.array, mean):
    x_distance = x - mean
    x_distance_square = x_distance**2
    return np.sum(x_distance_square)
    
    