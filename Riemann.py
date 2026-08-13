# 0. Library imports

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as mpatches    # for new error bar idea
from matplotlib.widgets import TextBox, Button



# 1. Define the function

def f(x):
    return x**3 - 7*x**2 + 15*x - 8
    # Equivalent factored form, as a note: (x-2)^3 - (x-2)^2 - (x-2) + 2

A = 1.0
B = 4.0 
    # Hard-coded integration bounds [A,B]. Keeping these as named constants for later.
    # The real integral is not completed in the code since it is trivial. The value of
    # 44/3 computed in the ReadMe is simply displayed and compared against.

EXACT_INTEGRAL = 21.0 / 4.0 # =5.25



# 2. try: 

def compute_approximation(method, n): # n subintervals, with the given "method": 'left', 'right', 'mid', or 'trap'.
    dx = (B - A) / n    # equal subintervals
    x_edges = np.linspace(A, B, n + 1)  # x-coordinates of the subinterval boundaries. n+1 boundary points for n strips
                                        # remember linspace needs ('begin', 'end', '# of points to generate')
    if method == "left": 
        sample_points = x_edges[:-1]    # all elements except last (this corresponds to "B")
        heights = f(sample_points)      # remember that slice notation is [start:stop]
        approx_value = np.sum(heights * dx)
        
    elif method == "right":
        sample_points = x_edges[1:]     # drop the first one ("A")
        heights = f(sample_points)
        approx_value = np.sum(heights * dx)

    elif method == "mid":
        sample_points = (x_edges[:-1] + x_edges[1:]) / 2    # average of right and left
        heights = f(sample_points)
        approx_value = np.sum(heights * dx)

    elif method == "trap":      # trapezoids have different "base" heights, so need y edges now
        y_edges = f(x_edges)
        approx_value = np.sum(dx * (y_edges[:-1] + y_edges[1:]) / 2)    # A = 1/2 * (b1 + b2) * h, where b1 and b2 are y_edges, and h is dx

    elif method == "simpson":   # Simpson's rule requires an even number of subintervals, so n must be even
        if n % 2 != 0:      # modulo operator - returns the remainder after division. 0 even, 1 off. != 0 "not equal to 0"
            raise ValueError("Simpson's rule requires n to be even).")
        x_midpoints = (x_edges[:-1] + x_edges[1:]) / 2
        y_edges = f(x_edges)
        y_midpoints = f(x_midpoints)
        approx_value = (dx / 3) * (y_edges[0] + 2 * np.sum(y_edges[1:-1:2]) + 4 * np.sum(y_midpoints) + y_edges[-1])

    else:
        raise ValueError(f"Unknown method: {method}")   # failsafe, should never happen if the radio buttons are used correctly

    return approx_value, x_edges



# 3. Graph Setup

fig, axes = plt.subplots(
    2, 3,
    figsize=(16, 9),
    gridspec_kw={"hspace": 0.45, "wspace": 0.35}    # spacing between subplots, in inches. hspace = height, wspace = width
)
axes = axes.flatten()   # flatten the 2D array of axes into a plain list to index as axes[0]..axes[5].
plt.subplots_adjust(bottom=0.30)
    # leave space for the n widget

x_smooth = np.linspace(A, B, 400)   # Shared by all 5 subplots
y_smooth = f(x_smooth)

METHODS = ["left", "right", "mid", "trap", "simp"]
TITLES = [
    "Left Riemann Sum",
    "Right Riemann Sum",
    "Midpoint Riemann Sum",
    "Trapezoidal Rule",
    "Simpson's Rule",
]

for i, ax in enumerate(axes[:5]):   # only the first 5 axes are used for the plots, the last one is for data
    ax.plot(x_smooth, y_smooth, color="black", linewidth=1.5)
    ax.set_title(TITLES[i], fontsize=9)
    ax.set_xlim(A - 1, B + 1)
    ax.set_ylim(0, 5)
    ax.axhline(0, color="black", linewidth=1)   # x-axis
    ax.axvline(0, color="black", linewidth=1)   # y-axis
    ax.set_xlabel("x", fontsize=8)
    ax.set_ylabel("f(x)", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.7)

# error bar panel
ax_error = axes[5]
ax_error.set_title("% Error by Method", fontsize=9)
ax_error.axis("off")   # going to draw the error bars manually, so turn off the default axes


shape_patches = [[] for _ in range(5)] 
    # list of lists to hold all drawings/patches for each subplot
    # Each sublist corresponds to a method's shapes
    # range(5) generates the fixed sequence [0, 1, 2, 3, 4] — one index per subplot



# 4. Redraw rectangles/trapezoids/parabolas + update info for multiple changes

def redraw(n):  # handles all n updates, and will be called by the radio button callback as well
    for i in range(5):  # Clear previous shapes
        for patch in shape_patches[i]:
            patch.remove()
        shape_patches[i].clear()

    approx_value = {}   # storing each method's result in error panel

    for i, method in enumerate(METHODS):    # draw shapes & collect approximations













# 5. User interaction programming

ax_box = plt.axes([0.42, 0.06, 0.08, 0.04])
ax_left = plt.axes([0.51, 0.06, 0.03, 0.04])
ax_right = plt.axes([0.55, 0.06, 0.03, 0.04])

n_textbox = TextBox(
    ax=ax_box,
    label="n (1-12): ",
    initial="4",
)

btn_left = Button(ax_left, "<", color="lightgray", hovercolor="gray")
btn_right = Button(ax_right, ">", color="lightgray", hovercolor="gray")

def on_n_submit(text):      # validate the input since text boxes accept any string
    try:
        n = int(text)
    except ValueError:      # Not a valid integer
        return
    if n < 1 or n > 12:
        n = max(1, min(12, n))
        n_textbox.set_val(str(n))
        return      # set_val will re-trigger on_n_submit with the clamped value
    redraw(n)

def click_left(event):
    n = max(1, int(n_textbox.text) - 1)
    n_textbox.set_val(str(n))  # trigger on_n_submit

def click_right(event):
    n = min(12, int(n_textbox.text) + 1)
    n_textbox.set_val(str(n))  # trigger on_n_submit

n_textbox.on_submit(on_n_submit)
btn_left.on_clicked(click_left)
btn_right.on_clicked(click_right)



redraw(4)   # to start it off
plt.show()
