import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, TextBox
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Polygon

# --- Physics & Geometry Engine ---
def ray_segment_intersect(p, v, a, b):
    v1 = p - a
    v2 = b - a
    v3 = np.array([-v[1], v[0]])
    dot = np.dot(v2, v3)
    if abs(dot) < 1e-6: return float('inf'), None
    t = (v2[0]*v1[1] - v2[1]*v1[0]) / dot
    u = np.dot(v1, v3) / dot
    if t > 1e-5 and 0 <= u <= 1:
        normal = np.array([-v2[1], v2[0]])
        return t, normal / np.linalg.norm(normal)
    return float('inf'), None

def ray_circle_intersect(p, v, center, radius):
    oc = p - center
    a = np.dot(v, v)
    b = 2.0 * np.dot(oc, v)
    c = np.dot(oc, oc) - radius**2
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        t1 = (-b - np.sqrt(discriminant)) / (2.0*a)
        t2 = (-b + np.sqrt(discriminant)) / (2.0*a)
        t = t1 if t1 > 1e-5 else t2
        if t > 1e-5:
            hit_pt = p + t*v
            return t, (hit_pt - center) / radius
    return float('inf'), None

def calculate_bounces(shape, p0, v0, num_bounces=200):
    pts = [np.array(p0)]
    p = np.array(p0)
    v = np.array(v0)
    if np.linalg.norm(v) == 0: v = np.array([1.0, 0.0])
    v = v / np.linalg.norm(v)
    
    square_segs = [(np.array([0,0]), np.array([1,0])), (np.array([1,0]), np.array([1,1])),
                   (np.array([1,1]), np.array([0,1])), (np.array([0,1]), np.array([0,0]))]
    tri_segs = [(np.array([0,0]), np.array([1,0])), (np.array([1,0]), np.array([0.5, np.sqrt(3)/2])),
                (np.array([0.5, np.sqrt(3)/2]), np.array([0,0]))]
    circ_center, circ_radius = np.array([0.5, 0.5]), 0.5

    for _ in range(num_bounces):
        best_t, best_normal = float('inf'), None
        if shape == 'Square':
            for a, b in square_segs:
                t, n = ray_segment_intersect(p, v, a, b)
                if t < best_t: best_t, best_normal = t, n
        elif shape == 'Triangle':
            for a, b in tri_segs:
                t, n = ray_segment_intersect(p, v, a, b)
                if t < best_t: best_t, best_normal = t, n
        elif shape == 'Circle':
            t, n = ray_circle_intersect(p, v, circ_center, circ_radius)
            if t < best_t: best_t, best_normal = t, n

        if best_t == float('inf'): break
        p = p + best_t * v
        v = v - 2.0 * np.dot(v, best_normal) * best_normal
        pts.append(p.copy())
    return pts

def is_inside(x, y, shape):
    if shape == 'Square': return 0.02 < x < 0.98 and 0.02 < y < 0.98
    elif shape == 'Circle': return (x - 0.5)**2 + (y - 0.5)**2 < 0.48**2
    elif shape == 'Triangle': return y > 0.02 and y < np.sqrt(3)*x - 0.02 and y < -np.sqrt(3)*(x-1) - 0.02

# --- State & UI Setup ---
current_shape = 'Square'
current_x0, current_y0 = 0.5, 0.2
current_vx, current_vy = 1.0, 0.5
drag_target = None

fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.25, bottom=0.15)
ax.set_title("Weyl's Criterion: Ray tracing", fontsize=14, pad=15)

lc = LineCollection([], lw=1.2, alpha=0.8)
ax.add_collection(lc)
start_point, = ax.plot([], [], 'ro', markersize=9, zorder=6)
hit_point, = ax.plot([], [], 'go', markersize=9, zorder=6)

ax_shape = plt.axes([0.05, 0.4, 0.15, 0.2])
radio_shape = RadioButtons(ax_shape, ('Square', 'Circle', 'Triangle'))

ax_box = plt.axes([0.35, 0.05, 0.4, 0.05])
text_slope = TextBox(ax_box, 'Slope (vy/vx): ', initial=f"{current_vy/current_vx:.4f}")

def update_plot():
    ax.clear()
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')

    if current_shape == 'Square':
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, color='black', lw=2))
    elif current_shape == 'Circle':
        ax.add_patch(Circle((0.5, 0.5), 0.5, fill=False, color='black', lw=2))
    elif current_shape == 'Triangle':
        ax.add_patch(Polygon([[0,0], [1,0], [0.5, np.sqrt(3)/2]], fill=False, color='black', lw=2))
    
    pts = calculate_bounces(current_shape, [current_x0, current_y0], [current_vx, current_vy])
    segments = [[pts[i], pts[i+1]] for i in range(len(pts)-1)]
    
    lc = LineCollection(segments, lw=1.2, alpha=0.8)
    lc.set_color(plt.cm.rainbow(np.linspace(0, 1, len(segments))))
    ax.add_collection(lc)
    
    start_point.set_data([current_x0], [current_y0])
    ax.add_line(start_point)
    
    if len(pts) > 1:
        hit_point.set_data([pts[1][0]], [pts[1][1]])
        ax.add_line(hit_point)
        
    fig.canvas.draw_idle()

def change_shape(label):
    global current_shape, current_x0, current_y0
    current_shape = label
    current_x0, current_y0 = 0.5, 0.2 
    update_plot()
radio_shape.on_clicked(change_shape)

def submit_slope(text):
    global current_vx, current_vy
    try:
        val = float(eval(text, {"__builtins__": None}, {"sqrt": np.sqrt}))
        current_vx = 1.0
        current_vy = val
        update_plot()
    except Exception:
        text_slope.set_val(f"{current_vy/current_vx:.4f}")
text_slope.on_submit(submit_slope)

# --- Mouse Drag Interaction ---
def on_press(event):
    global drag_target
    if event.inaxes != ax: return
    
    pts = calculate_bounces(current_shape, [current_x0, current_y0], [current_vx, current_vy], num_bounces=1)
    if len(pts) > 1:
        dist_hit = np.hypot(event.xdata - pts[1][0], event.ydata - pts[1][1])
        if dist_hit < 0.05:
            drag_target = 'hit'
            return

    dist_start = np.hypot(event.xdata - current_x0, event.ydata - current_y0)
    if dist_start < 0.05:
        drag_target = 'start'

def on_motion(event):
    global drag_target, current_x0, current_y0, current_vx, current_vy
    if not drag_target or event.inaxes != ax: return
    
    if drag_target == 'start':
        if is_inside(event.xdata, event.ydata, current_shape):
            current_x0, current_y0 = event.xdata, event.ydata
            update_plot()
            
    elif drag_target == 'hit':
        dx = event.xdata - current_x0
        dy = event.ydata - current_y0
        if dx != 0:
            current_vx, current_vy = dx, dy
            # Update textbox without triggering submit loop
            text_slope.set_val(f"{dy/dx:.4f}")
            update_plot()

def on_release(event):
    global drag_target
    drag_target = None

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

update_plot()
plt.show()