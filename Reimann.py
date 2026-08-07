# 0. Library imports

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, RadioButtons



# 1. Define the function

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



# 2. try: 

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



# 3. Graph

fig, ax = plt.subplots(figsize=(9, 7))
plt.subplots_adjust(left=0.1, bottom=0.30, right=0.78)
    # subplots_adjust shrinks the main plot area so there's empty space below it and to the right (for the slider and radio buttons)

x_smooth = np.linspace(A, B, 400)
y_smooth = f(x_smooth)

curve_line, = ax.plot(x_smooth, y_smooth, color="black", linewidth=2, label="f(x) = -(x-3)² + 5")

# simple graph boundaries/labels
ax.set_xlim(A - 1, B + 1)
ax.set_ylim(0, 6)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.legend(loc="upper right")

# textbox to display approximation, exact value, percent error
info_text = ax.text(
    0.02, 0.95, "", transform=ax.transAxes,
    fontsize=10, verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8)
)

shape_patches = []



# 4. User interaction programming


textbox_ax = plt.axes([0.35, 0.12, 0.15, 0.05])
n_textbox = TextBox(
    ax=textbox_ax,
    label="n (1-12): ",
    initial="4",
)

radio_ax = plt.axes([0.82, 0.5, 0.16, 0.2])
radio_ax.set_title("Method", fontsize=10)
method_radio = RadioButtons(
    radio_ax,
    labels=["left", "right", "mid", "trap"],
)

def on_n_submit(text):      # validate the input since text boxes accept any string
    try:
        n = int(text)
    except ValueError:      # Not a valid integer
        return
    if n < 1 or n > 12:
        n = max(1, min(12, n))
        n_textbox.set_val(str(n))
        return      # set_val will re-trigger on_n_submit with the clamped value

    redraw(method_radio.value_selected, n)

def on_method_change(label):
    redraw(label, int(n_textbox.text))

n_textbox.on_submit(on_n_submit)
method_radio.on_clicked(on_method_change)