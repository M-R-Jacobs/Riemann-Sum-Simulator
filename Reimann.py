# Library imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons



# Define the function

def f(x):
    return -(x - 3)**2 + 5

A = 1.0
B = 5.0 
    # Hard-coded integration bounds [A,B]. Keeping these as named constants for later.
    # The real integral is not completed in the code since it is trivial. The value of
    # 44/3 computed in the ReadMe is simply displayed and compared against.

EXACT_INTEGRAL = 44.0 / 3.0

def compute_approximation(method, n): #n subintervals, with the given "method": 'left', 'right', 'mid', or 'trap'.
    dx = (B - A) / n    # equal subintervals
    x_edges = np.linspace(A, B, n + 1)  # x-coordinates of the subinterval boundaries

# try: 
if method == "left": 
    sample_points = x_edges[:-1]
    heights = f(sample_points)
    approx_value = np.sum(heights * dx)
    
elif method == "right":
elif method == "center":
elif method == "mid":
elif method == "trap":

else:
    raise ValueError(f"Unknown method: {method}")

return approx_value, x_edges