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



# 2. try: 

def compute_approximation(method, n): #n subintervals, with the given "method": 'left', 'right', 'mid', or 'trap'.
    dx = (B - A) / n    # equal subintervals
    x_edges = np.linspace(A, B, n + 1)  # x-coordinates of the subinterval boundaries
                                        # remember linspace needs ('begin', 'end', '# of points to generate')
    if method == "left": 
        sample_points = x_edges[:-1]    # all elements except last (this corresponds to "B")
        heights = f(sample_points)      # remember that slice is [start:stop]
        approx_value = np.sum(heights * dx)
        
    elif method == "right":
        sample_points = x_edges[1:]     # drop the first one ("A")
        heights = f(sample_points)
        approx_value = np.sum(heights * dx)

    elif method == "mid":
        sample_points = (x_edges[:-1] + x_edges[1:]) / 2    # average
        heights = f(sample_points)
        approx_value = np.sum(heights * dx)

    elif method == "trap":      # trapezoids have different "base" heights, so need y edges now
        y_edges = f(x_edges)
        approx_value = np.sum(dx * (y_edges[:-1] + y_edges[1:]) / 2)

    else:
        raise ValueError(f"Unknown method: {method}")   # failsafe

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



# 3.1. Redraw rectangles & trapezoids + update info for multiple changes

def redraw(method, n):  # remove last interation's rectangles/trapezoids
    for patch in shape_patches:
        patch.remove()
    shape_patches.clear()

    approx_value, x_edges = compute_approximation(method, n)
    dx = x_edges[1] - x_edges[0]

    if method == "trap":
        y_edges = f(x_edges)
        for i in range(n):      # draw the trapezoid using the 4 corners defined below
            xs = [x_edges[i], x_edges[i+1], x_edges[i+1], x_edges[i]]
            ys = [0, 0, y_edges[i+1], y_edges[i]]
            patch = ax.fill(xs, ys, edgecolor="blue", facecolor="skyblue", alpha=0.5, linewidth=1)[0]
            shape_patches.append(patch)     # defined patch to be used here. az.fill will draw/shade each trap. [0] pulls it out of the list

    else:
        for i in range(n):
            left_edge = x_edges[i]
            right_edge = x_edges[i+1]

            if method == "left":
                height = f(left_edge)
            elif method == "right":
                height = f(right_edge)
            else:       # method == "mid"
                height = f((left_edge + right_edge) / 2)
            
            patch = ax.bar(left_edge, height, width=dx, align="edge", edgecolor="blue", facecolor="skyblue", alpha=0.5, linewidth=1)
            shape_patches.append(patch)
            # remember: ax.bar does rectangle 'start' 'height' 'width'. Align needed to start left edge there

    # percent difference:
    percent_error = abs(approx_value - EXACT_INTEGRAL) / EXACT_INTEGRAL * 100

    # method labels
    method_labels = {
        "left": "Left Riemann Sum",
        "right": "Right Riemann Sum",
        "mid": "Midpoint Riemann Sum",
        "trap": "Trapezoidal Rule",
    }

    info_text.set_text(
        f"Method: {method_labels[method]}\n"
        f"n = {n}\n"
        f"Approximation = {approx_value:.5f}\n" # {variable:.Nf} - N: decimal number
        f"Percent error = {percent_error:.3f}%"
    )

    fig.canvas.draw_idle()




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



redraw("left", 4)   # to start it off

plt.show()