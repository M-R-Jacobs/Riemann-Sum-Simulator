# Library imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons



# Define the function

def f(x):
    return -(x - 3) ** 2 + 5

A = 1.0
B = 5.0 
    # Hard-coded integration bounds [A,B]. Keeping these as named constants for later

def compute_approximation(method, n): #n subintervals, with the given method: 'left', 'right', 'mid', or 'trap'.
    dx = (B - A) / n
    x_edges = np.linspace(A, B, n + 1)

# try: 
# if method == "left": 
# elif method === "right":
# elif ...