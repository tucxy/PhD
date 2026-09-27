import math
import random
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Numerical helpers
# -----------------------------

def safe_eval(fn, x):
    try:
        y = fn(x)
        if isinstance(y, complex) or not math.isfinite(y):
            return None
        if abs(y) > 1e6:
            return None
        return float(y)
    except Exception:
        return None


def bisect_root(h, a, b, iters=50):
    fa = safe_eval(h, a)
    fb = safe_eval(h, b)
    if fa is None or fb is None:
        return None
    if abs(fa) < 1e-10:
        return a
    if abs(fb) < 1e-10:
        return b
    if fa * fb > 0:
        return None
    lo, hi = a, b
    flo, fhi = fa, fb
    for _ in range(iters):
        mid = (lo + hi) / 2
        fm = safe_eval(h, mid)
        if fm is None:
            return None
        if abs(fm) < 1e-10:
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def find_intersections(f, g, xmin, xmax, samples=1800):
    def h(x):
        a = safe_eval(f, x)
        b = safe_eval(g, x)
        if a is None or b is None:
            raise ValueError
        return a - b

    xs = [xmin + (xmax - xmin) * i / samples for i in range(samples + 1)]
    vals = []
    for x in xs:
        try:
            vals.append(h(x))
        except Exception:
            vals.append(None)

    roots = []
    for i in range(samples):
        x1, x2 = xs[i], xs[i + 1]
        y1, y2 = vals[i], vals[i + 1]
        if y1 is None or y2 is None:
            continue
        if abs(y1) < 1e-5:
            roots.append(x1)
        if y1 * y2 < 0:
            r = bisect_root(h, x1, x2)
            if r is not None:
                roots.append(r)

    # Tangency detector: local near-zero minima of |f-g|.
    for i in range(1, samples):
        if vals[i-1] is None or vals[i] is None or vals[i+1] is None:
            continue
        a, b, c = abs(vals[i-1]), abs(vals[i]), abs(vals[i+1])
        if b < a and b < c and b < 2e-3:
            roots.append(xs[i])

    roots.sort()
    dedup = []
    for r in roots:
        if not dedup or abs(r - dedup[-1]) > 2e-2:
            dedup.append(r)
    return dedup


def simpson_area(f, g, a, b, n=600):
    if b <= a:
        return 0.0
    if n % 2:
        n += 1
    h = (b - a) / n

    def integrand(x):
        y1 = safe_eval(f, x)
        y2 = safe_eval(g, x)
        if y1 is None or y2 is None:
            return 0.0
        return abs(y1 - y2)

    s = integrand(a) + integrand(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * integrand(a + i * h)
    return s * h / 3


# -----------------------------
# Function model
# -----------------------------

class Curve:
    def __init__(self, expr, fn):
        self.expr = expr
        self.fn = fn

    def transformed(self, card):
        kind, value, label = card
        old_fn = self.fn
        old_expr = self.expr

        if kind == 'add_const':
            return Curve(f"({old_expr}) + {value}", lambda x, f=old_fn, v=value: f(x) + v)
        if kind == 'mul_const':
            return Curve(f"{value}({old_expr})", lambda x, f=old_fn, v=value: v * f(x))
        if kind == 'add_x':
            coeff = value
            sign = '+' if coeff >= 0 else '-'
            return Curve(f"({old_expr}) {sign} {abs(coeff)}x", lambda x, f=old_fn, c=coeff: f(x) + c*x)
        if kind == 'square':
            return Curve(f"({old_expr})^2", lambda x, f=old_fn: f(x) ** 2)
        if kind == 'abs':
            return Curve(f"|{old_expr}|", lambda x, f=old_fn: abs(f(x)))
        if kind == 'shift_x':
            return Curve(f"{old_expr.replace('x', f'(x-{value})')}", lambda x, f=old_fn, v=value: f(x - v))
        if kind == 'widen':
            return Curve(f"{old_expr.replace('x', f'({value}x)')}", lambda x, f=old_fn, v=value: f(v*x))
        return self


def starter_curve():
    pool = [
        Curve("x", lambda x: x),
        Curve("x^2", lambda x: x*x),
        Curve("-x", lambda x: -x),
        Curve("2", lambda x: 2.0),
        Curve("4", lambda x: 4.0),
    ]
    return random.choice(pool)


CARD_POOL = [
    ('add_const', 1, '+1'), ('add_const', -1, '-1'),
    ('add_const', 2, '+2'), ('add_const', -2, '-2'),
    ('mul_const', 2, '×2'), ('mul_const', 0.5, '×1/2'),
    ('add_x', 1, '+x'), ('add_x', -1, '-x'),
    ('abs', None, '|f|'),
    ('shift_x', 1, 'shift right 1'), ('shift_x', -1, 'shift left 1'),
    ('widen', 0.5, 'widen'), ('widen', 2, 'narrow'),
]

SHOP_ITEMS = [
    ('Extra Move', 8, 'extra_move'),
    ('Bigger Hand', 10, 'bigger_hand'),
    ('Area Mult +0.25', 12, 'mult'),
    ('Unlock Square', 14, 'square'),
]


# -----------------------------
# Game UI
# -----------------------------

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title('Area Rogue')
        self.root.geometry('1120x760')
        self.root.configure(bg='#171717')

        self.xmin, self.xmax = -6, 6
        self.ymin, self.ymax = -8, 12
        self.round = 1
        self.hp = 3
        self.money = 0
        self.area_mult = 1.0
        self.base_moves = 4
        self.hand_size = 3
        self.moves_left = self.base_moves
        self.selected_curve = 'f'
        self.cards = []
        self.regions = []
        self.selected_region = None
        self.extra_cards = []

        self.build_layout()
        self.new_round()

    def build_layout(self):
        top = tk.Frame(self.root, bg='#171717')
        top.pack(fill='x', padx=12, pady=8)
        self.status = tk.Label(top, text='', fg='white', bg='#171717', font=('Segoe UI', 13, 'bold'))
        self.status.pack(side='left')
        self.target_label = tk.Label(top, text='', fg='#ffd166', bg='#171717', font=('Segoe UI', 13, 'bold'))
        self.target_label.pack(side='right')

        body = tk.Frame(self.root, bg='#171717')
        body.pack(fill='both', expand=True, padx=12, pady=4)

        self.canvas = tk.Canvas(body, bg='#0f0f0f', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        panel = tk.Frame(body, width=330, bg='#222222')
        panel.pack(side='right', fill='y', padx=(10,0))
        panel.pack_propagate(False)

        tk.Label(panel, text='CURVES', fg='white', bg='#222222', font=('Segoe UI', 14, 'bold')).pack(pady=(14,6))
        self.f_btn = tk.Button(panel, text='', command=lambda: self.select_curve('f'))
        self.f_btn.pack(fill='x', padx=12, pady=4)
        self.g_btn = tk.Button(panel, text='', command=lambda: self.select_curve('g'))
        self.g_btn.pack(fill='x', padx=12, pady=4)

        tk.Label(panel, text='Choose a card, then apply it to the selected curve.', fg='#cccccc', bg='#222222', wraplength=290).pack(padx=12, pady=(10,6))
        self.card_frame = tk.Frame(panel, bg='#222222')
        self.card_frame.pack(fill='x', padx=12)

        self.region_label = tk.Label(panel, text='No bounded region selected.', fg='#9fd3ff', bg='#222222', wraplength=290, font=('Segoe UI', 11, 'bold'))
        self.region_label.pack(padx=12, pady=14)

        self.score_btn = tk.Button(panel, text='SCORE SELECTED REGION', command=self.score_region, bg='#2f7d32', fg='white', font=('Segoe UI', 11, 'bold'))
        self.score_btn.pack(fill='x', padx=12, pady=4)

        self.end_btn = tk.Button(panel, text='END ROUND / TAKE HIT', command=self.fail_round, bg='#7d2f2f', fg='white')
        self.end_btn.pack(fill='x', padx=12, pady=4)

        self.help_label = tk.Label(panel, text='Click a shaded bounded region on the graph to select it.', fg='#aaaaaa', bg='#222222', wraplength=290)
        self.help_label.pack(side='bottom', padx=12, pady=12)

    def new_round(self):
        self.moves_left = self.base_moves
        self.selected_region = None
        # Generate a pair likely to intersect.
        self.f = starter_curve()
        self.g = starter_curve()
        tries = 0
        while tries < 100:
            roots = find_intersections(self.f.fn, self.g.fn, self.xmin, self.xmax)
            if len(roots) >= 2:
                break
            self.f = starter_curve(); self.g = starter_curve(); tries += 1
        self.target = 4 + self.round * 2.25
        self.draw_cards()
        self.refresh()

    def select_curve(self, which):
        self.selected_curve = which
        self.refresh_curve_buttons()

    def refresh_curve_buttons(self):
        sel_bg = '#4a4a4a'
        unsel_bg = '#2e2e2e'
        self.f_btn.config(text=f"f(x) = {self.f.expr}", bg=sel_bg if self.selected_curve == 'f' else unsel_bg, fg='white')
        self.g_btn.config(text=f"g(x) = {self.g.expr}", bg=sel_bg if self.selected_curve == 'g' else unsel_bg, fg='white')

    def draw_cards(self):
        pool = CARD_POOL + self.extra_cards
        self.cards = random.sample(pool, k=min(self.hand_size, len(pool)))
        for w in self.card_frame.winfo_children():
            w.destroy()
        for idx, card in enumerate(self.cards):
            b = tk.Button(self.card_frame, text=card[2], command=lambda i=idx: self.play_card(i), bg='#353535', fg='white', font=('Segoe UI', 11, 'bold'))
            b.pack(fill='x', pady=3)

    def play_card(self, idx):
        if self.moves_left <= 0:
            return
        card = self.cards[idx]
        if self.selected_curve == 'f':
            self.f = self.f.transformed(card)
        else:
            self.g = self.g.transformed(card)
        self.moves_left -= 1
        self.selected_region = None
        if self.moves_left > 0:
            self.draw_cards()
        else:
            for w in self.card_frame.winfo_children():
                w.destroy()
            tk.Label(self.card_frame, text='No moves left. Pick a region and score it.', bg='#222222', fg='white', wraplength=280).pack(pady=8)
        self.refresh()

    def refresh(self):
        self.status.config(text=f"Round {self.round}   HP {self.hp}   $ {self.money}   Moves {self.moves_left}")
        self.target_label.config(text=f"Target area: {self.target:.1f}   ×{self.area_mult:.2f}")
        self.refresh_curve_buttons()
        self.compute_regions()
        self.draw_graph()
        if self.selected_region is None:
            self.region_label.config(text=f"Bounded regions found: {len(self.regions)}")

    def compute_regions(self):
        roots = find_intersections(self.f.fn, self.g.fn, self.xmin, self.xmax)
        regions = []
        for a, b in zip(roots, roots[1:]):
            mid = (a+b)/2
            y1, y2 = safe_eval(self.f.fn, mid), safe_eval(self.g.fn, mid)
            if y1 is None or y2 is None:
                continue
            area = simpson_area(self.f.fn, self.g.fn, a, b)
            if area > 0.01 and math.isfinite(area):
                regions.append((a, b, area))
        self.regions = regions

    def world_to_canvas(self, x, y):
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        px = (x - self.xmin) / (self.xmax - self.xmin) * w
        py = h - (y - self.ymin) / (self.ymax - self.ymin) * h
        return px, py

    def canvas_to_world(self, px, py):
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())
        x = self.xmin + px / w * (self.xmax - self.xmin)
        y = self.ymin + (h - py) / h * (self.ymax - self.ymin)
        return x, y

    def draw_graph(self):
        self.canvas.delete('all')
        w = max(1, self.canvas.winfo_width())
        h = max(1, self.canvas.winfo_height())

        # grid
        for x in range(math.ceil(self.xmin), math.floor(self.xmax)+1):
            px, _ = self.world_to_canvas(x, 0)
            self.canvas.create_line(px, 0, px, h, fill='#242424')
        for y in range(math.ceil(self.ymin), math.floor(self.ymax)+1):
            _, py = self.world_to_canvas(0, y)
            self.canvas.create_line(0, py, w, py, fill='#242424')
        x0,_ = self.world_to_canvas(0,0); _,y0 = self.world_to_canvas(0,0)
        self.canvas.create_line(x0, 0, x0, h, fill='#777777', width=2)
        self.canvas.create_line(0, y0, w, y0, fill='#777777', width=2)

        # shade bounded regions
        for idx, (a,b,area) in enumerate(self.regions):
            pts = []
            steps = 90
            for j in range(steps+1):
                x = a + (b-a)*j/steps
                y = safe_eval(self.f.fn, x)
                if y is not None:
                    pts.extend(self.world_to_canvas(x,y))
            for j in range(steps, -1, -1):
                x = a + (b-a)*j/steps
                y = safe_eval(self.g.fn, x)
                if y is not None:
                    pts.extend(self.world_to_canvas(x,y))
            if len(pts) >= 6:
                fill = '#6b5d2f' if self.selected_region == idx else '#33445a'
                self.canvas.create_polygon(pts, fill=fill, outline='')
                mx = (a+b)/2
                fy = safe_eval(self.f.fn,mx); gy=safe_eval(self.g.fn,mx)
                if fy is not None and gy is not None:
                    px,py=self.world_to_canvas(mx,(fy+gy)/2)
                    self.canvas.create_text(px,py,text=f"{area*self.area_mult:.1f}",fill='white',font=('Segoe UI',10,'bold'))

        self.draw_curve(self.f.fn, '#5dade2', width=3)
        self.draw_curve(self.g.fn, '#ec7063', width=3)

    def draw_curve(self, fn, color, width=2):
        w = max(1, self.canvas.winfo_width())
        prev = None
        for px in range(w):
            x = self.xmin + px / max(1,w-1) * (self.xmax-self.xmin)
            y = safe_eval(fn,x)
            if y is None or y < self.ymin-20 or y > self.ymax+20:
                prev = None
                continue
            point = self.world_to_canvas(x,y)
            if prev is not None:
                self.canvas.create_line(prev[0],prev[1],point[0],point[1],fill=color,width=width)
            prev = point

    def on_canvas_click(self, event):
        x,y = self.canvas_to_world(event.x,event.y)
        for idx,(a,b,area) in enumerate(self.regions):
            if a <= x <= b:
                fval = safe_eval(self.f.fn,x); gval=safe_eval(self.g.fn,x)
                if fval is None or gval is None: continue
                lo,hi=sorted((fval,gval))
                if lo <= y <= hi:
                    self.selected_region=idx
                    self.region_label.config(text=f"Selected area: {area:.3f} × {self.area_mult:.2f} = {area*self.area_mult:.3f}")
                    self.draw_graph()
                    return

    def score_region(self):
        if self.selected_region is None:
            messagebox.showinfo('Select a region','Click one shaded bounded region first.')
            return
        area = self.regions[self.selected_region][2] * self.area_mult
        if area >= self.target:
            payout = max(3, int(area/3)) + self.moves_left
            self.money += payout
            messagebox.showinfo('Round cleared', f"Area {area:.2f} beat {self.target:.2f}.\nYou earned ${payout}.")
            self.round += 1
            if self.round % 3 == 0:
                self.open_shop()
            self.new_round()
        else:
            self.hp -= 1
            messagebox.showinfo('Miss', f"Area {area:.2f} did not reach {self.target:.2f}.\nLost 1 HP.")
            if self.hp <= 0:
                self.game_over()
            else:
                self.round += 1
                self.new_round()

    def fail_round(self):
        self.hp -= 1
        if self.hp <= 0:
            self.game_over()
        else:
            self.round += 1
            self.new_round()

    def game_over(self):
        messagebox.showinfo('Run over', f"You reached round {self.round}. Restarting.")
        self.round=1; self.hp=3; self.money=0; self.area_mult=1.0; self.base_moves=4; self.hand_size=3; self.extra_cards=[]
        self.new_round()

    def open_shop(self):
        win=tk.Toplevel(self.root); win.title('Shop'); win.configure(bg='#202020'); win.grab_set()
        tk.Label(win,text=f"SHOP   ${self.money}",bg='#202020',fg='white',font=('Segoe UI',15,'bold')).pack(padx=20,pady=14)

        offered=random.sample(SHOP_ITEMS,3)
        for name,cost,key in offered:
            def buy(k=key,c=cost,w=win):
                if self.money<c:
                    messagebox.showinfo('Shop','Not enough money.'); return
                self.money-=c
                if k=='extra_move': self.base_moves+=1
                elif k=='bigger_hand': self.hand_size=min(self.hand_size+1,5)
                elif k=='mult': self.area_mult+=0.25
                elif k=='square' and ('square',None,'square') not in self.extra_cards: self.extra_cards.append(('square',None,'square'))
                w.destroy()
            tk.Button(win,text=f"{name}   ${cost}",command=buy,bg='#343434',fg='white',width=30).pack(padx=20,pady=5)
        tk.Button(win,text='Skip',command=win.destroy,bg='#555555',fg='white').pack(pady=14)
        win.wait_window()


if __name__ == '__main__':
    root = tk.Tk()
    game = Game(root)
    root.after(100, game.refresh)
    root.mainloop()