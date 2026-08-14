# 0. Library imports

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches    # for new error bar idea
from matplotlib.widgets import TextBox, Button

plt.rcParams["font.family"] = "Arial"   # set the font for all text in the figure



# 1. Define the function

def f(x):
    return (1/4) * x * np.sin(x) + 2
    # Equivalent factored form, as a note: (x-2)^3 - (x-2)^2 - (x-2) + 2

A = 1.0
B = 8.0 
    # Hard-coded integration bounds [A,B]. Keeping these as named constants for later.
    # The real integral is not completed in the code since it is trivial. The value of
    # 44/3 computed in the ReadMe is simply displayed and compared against.

EXACT_INTEGRAL = ((1/4) * (np.sin(8) - 8*np.cos(8)) + 16) - ((1/4) * (np.sin(1) - 1*np.cos(1)) + 2)



# 2. Approximation methods

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

    elif method == "simp":   # Simpson's rule requires an even number of subintervals, so n must be even
        if n % 2 != 0:      # modulo operator - returns the remainder after division. 0 even, 1 off. != 0 "not equal to 0"
            n = n - 1   # make it even, but compute, dx, x_edges need adjusting (from the top of the function) too:
            dx = (B - A) / n
            x_edges = np.linspace(A, B, n + 1)
        lefts = x_edges[:-1]
        rights = x_edges[1:]
        mids = (lefts + rights) / 2
        approx_value = np.sum((dx/6) * (f(lefts) + 4*f(mids) + f(rights)))   # Simpson's rule formula

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
plt.subplots_adjust(bottom=0.22)
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
    ax.set_title(TITLES[i], fontsize=12)
    ax.set_xlim(A - 0.5, B + 0.5)
    ax.set_ylim(0, 5)
    ax.set_xticks([1,2,3,4,5,6,7])    # integer ticks only
    ax.axhline(0, color="black", linewidth=1)   # x-axis
    ax.axvline(0, color="black", linewidth=1)   # y-axis
    ax.set_xlabel("x", fontsize=8)
    ax.set_ylabel("f(x)", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.tick_params(labelsize=7)

# error bar panel
ax_error = axes[5]
ax_error.set_title("% Error by Method", fontsize=12)
ax_error.axis("off")   # going to draw the error bars manually, so turn off the default axes

# Subtle border around error panel
for spine in ax_error.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.8)
    spine.set_color("gray")

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

    approx_values = {}   # storing each method's result in error panel

    # draw shapes & collect approximations

    for i, method in enumerate(METHODS):    
        ax = axes[i]
        approx_value, x_edges = compute_approximation(method, n)
        approx_values[method] = approx_value
        dx = x_edges[1] - x_edges[0]

        if method == "trap":    # trap and simp first, since more complicated
            y_edges = f(x_edges)
            for j in range(len(x_edges) - 1):   # len() returns the number of elements in a list or array
                xs = [x_edges[j], x_edges[j + 1], x_edges[j + 1], x_edges[j]]
                ys = [0, 0, y_edges[j + 1], y_edges[j]]
                patch = ax.fill(
                    xs, ys,
                    edgecolor="blue", 
                    facecolor="lightblue", 
                    alpha=0.5,
                    linewidth=1
                )[0]  # fill returns a list of patches, we want the first one
                shape_patches[i].append(patch)

        elif method == "simp" and n % 2 != 0:   # Simpson's reroute if n is odd
            n_even = n - 1
            dx_even = (B - A) / n_even
            x_edges_even = np.linspace(A, B, n_even + 1)

            for j in range(n_even):
                x0 = x_edges_even[j]
                x1 = x_edges_even[j + 1]
                xm = (x0 + x1) / 2
                x_arc = np.linspace(x0, x1, 30)     # 30 points to draw the parabola
                f1, fm, fr = f(x0), f(xm), f(x1)
                coeffs = np.polyfit([x0, xm, x1], [f1, fm, fr], 2)  # fit a quadratic polynomial
                y_arc = np.polyval(coeffs, x_arc)   # evaluate the polynomial at the x_arc points
                poly = ax.fill_between(
                    x_arc, 0, y_arc,
                    edgecolor="blue",
                    facecolor="lightblue",
                    alpha=0.5,
                    linewidth=1
                )
                shape_patches[i].append(poly)

        elif method == "simp":      # also just handles the case when n is even normally
            for j in range(len(x_edges) - 1):
                x0 = x_edges[j]
                x1 = x_edges[j + 1]
                xm = (x0 + x1) / 2
                x_arc = np.linspace(x0, x1, 30)     # 30 points to draw the parabola
                f1, fm, fr = f(x0), f(xm), f(x1)
                coeffs = np.polyfit([x0, xm, x1], [f1, fm, fr], 2)  # fit a quadratic polynomial
                y_arc = np.polyval(coeffs, x_arc)   # evaluate the polynomial at the x_arc points
                poly = ax.fill_between(
                    x_arc, 0, y_arc,
                    edgecolor="blue",
                    facecolor="lightblue",
                    alpha=0.5,
                    linewidth=1
                )
                shape_patches[i].append(poly)

        else:   # left, right, mid
            for j in range(len(x_edges) - 1):
                x_left = x_edges[j]
                x_right = x_edges[j + 1]

                if method == "left":
                    height = f(x_left)
                elif method == "right":
                    height = f(x_right)
                else:  # midpoint
                    height = f((x_left + x_right) / 2)

                patch = ax.bar(     # remember: ax.bar does rectangle 'start' 'height' 'width'
                    x_left, height,
                    width=dx,
                    align="edge",
                    edgecolor="blue",
                    facecolor="skyblue",
                    alpha=0.5,
                    linewidth=1
                )
                shape_patches[i].append(patch)

        pct_error = abs((approx_value - EXACT_INTEGRAL) / EXACT_INTEGRAL) * 100
        for t in list(ax.texts):  # remove previous text annotations
            t.remove()

        if method == "simp" and n % 2 != 0:
            ax.text(
                0.5, 0.93,
                f"Simpson's rule requires even n, displaying n={n-1})",
                transform=ax.transAxes,
                fontsize=6.5,
                ha="center",
                va="top",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="wheat", alpha=0.9)
            )
        
        ax.text(
            0.97, 0.05,
            f"≈ {approx_value:.3f} ({pct_error:.2f}%)",     # {variable:.Nf} - N: decimal number
            transform=ax.transAxes,
            fontsize=7,
            ha="right",
            va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8)
        )

    # error bar panel update
    ax_error.clear()
    ax_error.axis("off")
    ax_error.set_title("% Error by Method", fontsize=9, fontfamily="Arial")

    for spine in ax_error.spines.values():  # border needs to be re-enabled after clear()
        spine.set_visible(True)
        spine.set_linewidth(0.8)
        spine.set_color("gray")

    bar_max = 20.0      # bars fill 0-20%
    bar_left = 0.08     # x position where bars start (in axes fraction)
    bar_right = 0.82    # x position where bars end (in axes fraction)
    bar_width = bar_right - bar_left
    bar_thickness = 0.018
    tick_intervals = 5
    n_rows = 5      # in case I want to change later
    row_height = 0.82 / n_rows  # vertical spacing per row

    method_labels = ["Left", "Right", "Midpoint", "Trapezoid", "Simpson"]

    for i, method in enumerate(METHODS):
        pct_error = abs((approx_values[method] - EXACT_INTEGRAL) / EXACT_INTEGRAL) * 100
        approx_value = approx_values[method]

        # Make y positions for bar for easier adjustment
        y_top = 0.93 - i * row_height   # method + approx value
        y_pct = y_top - 0.05            # % errore line
        y_bar = y_pct - 0.06            # bar = below % error line

        # Method names on left approx value on right (line 1)
        ax_error.text(
            bar_left, y_top,
            method_labels[i],
            transform=ax_error.transAxes,
            fontsize=8,
            va="top",
            fontfamily="Consolas"
        )
        ax_error.text(
            bar_right, y_top,
            f"≈ {approx_value:.3f}",
            transform=ax_error.transAxes,
            fontsize=8,
            va="top",
            ha="right",
            fontfamily="Consolas"
        )

        # % error number (line 2)
        ax_error.text(
            bar_right - 0.02, y_pct,
            f"{pct_error:.2f}%",
            transform=ax_error.transAxes,
            fontsize=7,
            va="top",
            fontfamily="Consolas"
        )

        # bar track
        track = mpatches.FancyBboxPatch(
            (bar_left, y_bar - bar_thickness),
            bar_width, bar_thickness * 2,
            boxstyle="square,pad=0",
            transform=ax_error.transAxes,
            facecolor="lightgray",
            edgecolor="none"
        )
        ax_error.add_patch(track)

        # Want to fill bar and add arrowhead
        clipped = pct_error >= bar_max
        fill_width = bar_width if clipped else bar_width * (pct_error / bar_max)
        bar_color = "blue"
 
        filled = mpatches.FancyBboxPatch(
            (bar_left, y_bar - bar_thickness),
            fill_width, bar_thickness,
            boxstyle="square,pad=0",
            transform=ax_error.transAxes,
            facecolor=bar_color, edgecolor="none"
        )
        ax_error.add_patch(filled)
 
        # Arrow flush to bar end if clipped
        if clipped:
            ax_error.text(
                bar_left + fill_width + 0.01,
                y_bar - bar_thickness / 2,
                "»",    # going back to the character arrowhead
                transform=ax_error.transAxes,
                fontsize=7, va="center", ha="left",
                color=bar_color
            )
 
    # Exact integral at the bottom
    ax_error.text(
        (bar_left + bar_right) / 2, 0.04,
        f"Exact Integral = {EXACT_INTEGRAL:.4f}",
        transform=ax_error.transAxes,
        fontsize=8, ha="center", va="bottom", fontfamily="Consolas",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="wheat", alpha=0.8)
    )
 
    fig.canvas.draw_idle()   # refresh the figure to show the new shapes and error bars




# 5. User interaction programming

ax_box = plt.axes([0.40, 0.08, 0.08, 0.04])
ax_left = plt.axes([0.49, 0.08, 0.03, 0.04])
ax_right = plt.axes([0.53, 0.08, 0.03, 0.04])

n_textbox = TextBox(
    ax=ax_box,
    label="n (2-20): ",
    initial="4",
)

btn_left = Button(ax_left, "<", color="lightgray", hovercolor="gray")
btn_right = Button(ax_right, ">", color="lightgray", hovercolor="gray")

fig.text(
    0.465, 0.055,
    "* Simpson's rule requires even n - odd values draw n-1 strips",
    ha="center", va="top", fontsize=7, color="gray", style="italic"
)

def on_n_submit(text):      # validate the input since text boxes accept any string
    try:
        n = int(text)
    except ValueError:      # Not a valid integer
        return
    if n < 2 or n > 20:
        n = max(2, min(20, n))
        n_textbox.set_val(str(n))
        return      # set_val will re-trigger on_n_submit with the clamped value
    redraw(n)

def click_left(event):
    n = max(2, int(n_textbox.text) - 1)
    n_textbox.set_val(str(n))  # trigger on_n_submit

def click_right(event):
    n = min(20, int(n_textbox.text) + 1)
    n_textbox.set_val(str(n))  # trigger on_n_submit

n_textbox.on_submit(on_n_submit)
btn_left.on_clicked(click_left)
btn_right.on_clicked(click_right)

fig.text(
    0.22, 0.10,
    "f(x) = ¼ x·sin(x) + 2",
    ha="center", va="center", fontsize=12,
    bbox=dict(boxstyle="round,pad=0.4", facecolor="wheat", alpha=0.8)
)




redraw(4)   # to start it off
plt.show()