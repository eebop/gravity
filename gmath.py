import numpy as np

# pythagorean theorom in n dimensions
def distance(start, end):
    return np.sqrt(np.sum((start - end) ** 2))
