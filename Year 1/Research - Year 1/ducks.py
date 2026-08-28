import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Slider
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from itertools import product, combinations

# --- Core 3D Logic ---
def calculate_3d_vertices(p0, v0, num_bounces=300):
    pts = [np.array(p0)]
    p = np.array(p0, dtype=float)
    v = np.array(v0, dtype=float)
    
    for _ in range(num_bounces):
        tx = (1.0 - p[0]) / v[0] if v[0] > 0 else ((0.0 - p[0]) / v[0] if v[0] < 0 else float('inf'))
        ty = (1.0 - p[1]) / v[1] if v[1] > 0 else ((0.0 - p[1]) / v[1] if v[1] < 0 else float('inf'))
        tz = (1.0 - p[2]) / v[2] if v[2] > 0 else ((0.0 - p[2]) / v[2] if v[2] < 0 else float('inf'))
        
        t = min(tx, ty, tz)
        p = p + v * t
        
        if t == tx: 
            p[0] = 1.0 if v[0] > 0 else 0.0
            v[0] = -v[0]
        if t == ty: 
            p[1] = 1.0 if v[1] > 0 else 0.0
            v[1] = -v[1]
        if t == tz: 
            p[2] = 1.0 if v[2] > 0 else 0.0
            v[2] = -v[2]
            
        pts.append(p.copy())
        
    return pts

# --- State Variables ---
p0 = [0.1, 0.1, 0.1]
v0 = [1.0, np.sqrt(2), np.sqrt(3)] 

fig = plt.figure(figsize=(9, 9))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.35) # Made room for all the controls
ax.set_title("Weyl's Criterion: 3d Ray tracing", fontsize=14)

# Draw the Box Outline
r = [0, 1]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(s-e)) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="black", alpha=0.2)

# UI Elements: Start Position Sliders
axcolor = 'lightgoldenrodyellow'
ax_x0 = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
ax_y0 = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_z0 = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_x0 = Slider(ax_x0, 'Start X', 0.01, 0.99, valinit=p0[0])
s_y0 = Slider(ax_y0, 'Start Y', 0.01, 0.99, valinit=p0[1])
s_z0 = Slider(ax_z0, 'Start Z', 0.01, 0.99, valinit=p0[2])

# UI Elements: Vector Direction Inputs
ax_vx = plt.axes([0.15, 0.02, 0.15, 0.05])
ax_vy = plt.axes([0.45, 0.02, 0.15, 0.05])
ax_vz = plt.axes([0.75, 0.02, 0.15, 0.05])

txt_vx = TextBox(ax_vx, 'Vx: ', initial="1")
txt_vy = TextBox(ax_vy, 'Vy: ', initial="sqrt(2)")
txt_vz = TextBox(ax_vz, 'Vz: ', initial="sqrt(3)")

lc = None
start_point_marker = None

def update_plot(val=None):
    global lc, start_point_marker
    if lc: lc.remove()
    if start_point_marker:
        start_point_marker.remove()
    
    # Update p0 from sliders
    p0[0] = s_x0.val
    p0[1] = s_y0.val
    p0[2] = s_z0.val
    
    pts = calculate_3d_vertices(p0, v0, num_bounces=400)
    segments = [[pts[i], pts[i+1]] for i in range(len(pts)-1)]
    
    lc = Line3DCollection(segments, lw=1.5, alpha=0.7)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(segments)))
    lc.set_color(colors)
    ax.add_collection3d(lc)
    
    start_point_marker = ax.scatter([p0[0]], [p0[1]], [p0[2]], color='red', s=50, zorder=10)
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 1)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    fig.canvas.draw_idle()

def submit_vector(text):
    global v0
    try:
        v0[0] = float(eval(txt_vx.text, {"__builtins__": None}, {"sqrt": np.sqrt}))
        v0[1] = float(eval(txt_vy.text, {"__builtins__": None}, {"sqrt": np.sqrt}))
        v0[2] = float(eval(txt_vz.text, {"__builtins__": None}, {"sqrt": np.sqrt}))
        update_plot()
    except Exception:
        pass

s_x0.on_changed(update_plot)
s_y0.on_changed(update_plot)
s_z0.on_changed(update_plot)

txt_vx.on_submit(submit_vector)
txt_vy.on_submit(submit_vector)
txt_vz.on_submit(submit_vector)

update_plot()
plt.show()