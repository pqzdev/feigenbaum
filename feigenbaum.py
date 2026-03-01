import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML

# --- Parameters ---
plot_start = 3.5
plot_finish = 4.0
step = 0.0005

# --- Generate bifurcation data ---
def feigenbaum(r, warm_up=1000, capture_cycles=500):
    x = np.random.rand()
    tail = [x]
    for i in range(warm_up):
        x = r * x * (1-x)
        if x in set(tail): break
        tail.append(x)
    tail = [x]
    for i in range(capture_cycles):
        x = r * x * (1-x)
        if x in set(tail): break
        tail.append(x)
    return tail

all_data_rows = []
for r_val in np.arange(plot_start, plot_finish, step):
    new_row = pd.DataFrame({'r': [r_val], 'tail': [feigenbaum(r=r_val)]})
    all_data_rows.append(new_row)

fb_df = pd.concat(all_data_rows, ignore_index=True)

all_r_values = []
all_x_values = []
for index, row in fb_df.iterrows():
    for x_val in row['tail']:
        all_r_values.append(row['r'])
        all_x_values.append(x_val)

# --- Cobweb helper functions ---
def path_line(r):
    x_values = fb_df[fb_df['r'].round(4) == round(r, 4)]['tail'].reset_index()
    x_coords = []
    y_coords = []
    for x in x_values['tail'].iloc[0]:
        x_coords.append(x)
        x_coords.append(r * x * (1-x))
        y_coords.append(r * x * (1-x))
        y_coords.append(r * x * (1-x))
    final_x = x_values['tail'].iloc[0][0]
    x_coords.append(final_x)
    y_coords.append(r * final_x * (1-final_x))
    return x_coords, y_coords

def quadratic(r, start=0, end=1, steps=500):
    x = np.linspace(start, end, steps)
    y = r * x * (1-x)
    return x, y

def linear(start=0, end=1, steps=500):
    x = np.linspace(start, end, steps)
    y = x
    return x, y

# --- Build figure ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.set_xlim(0, 1.0)
ax1.set_ylim(0, 1.0)
ax1.set_title('Cobweb Diagram')

line, = ax1.plot([], [], lw=2)
quad_line, = ax1.plot([], [], lw=1, color='orange')
lin_line, = ax1.plot(*linear(), lw=1, color='green')

ax2.plot(all_r_values, all_x_values, ',r', alpha=0.5)
ax2.set_xlim(plot_start, plot_finish)
ax2.set_xlabel('r')
ax2.set_ylabel('x')
ax2.set_title('Feigenbaum Bifurcation Diagram')
ax2.grid(True)

r_values = sorted(fb_df['r'].round(4).unique())
r_values = [r for r in r_values if plot_start <= r <= plot_finish]
r_values = r_values[::2]  # subsample to halve frame count and file size

vline = ax2.axvline(x=r_values[0], color='blue', lw=1)

# --- Animation ---
def init():
    line.set_data([], [])
    quad_line.set_data([], [])
    vline.set_xdata([r_values[0]])
    return line, quad_line, lin_line, vline

def animate(r):
    x, y = path_line(r)
    line.set_data(x, y)
    quad_line.set_data(*quadratic(r))
    vline.set_xdata([r])
    return line, quad_line, lin_line, vline

ani = animation.FuncAnimation(
    fig, animate, init_func=init, frames=r_values, interval=20, blit=False
)

plt.tight_layout()
plt.rcParams['animation.embed_limit'] = 50  # MB

ani.save('feigenbaum.gif', writer='pillow', fps=50)
HTML(ani.to_jshtml())