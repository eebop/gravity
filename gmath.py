import numpy as np

# pythagorean theorom in n dimensions
def distance(start, end):
    return np.sqrt(np.sum(np.abs(start - end) ** 2))
