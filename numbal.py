import tkinter as tk
from tkinter import messagebox
import random
import math

WIDTH = 980
HEIGHT = 680

OPS = {
    "+": lambda a,b: a+b,
    "-": lambda a,b: a-b,
    "×": lambda a,b: a*b,
    "÷": lambda a,b: None if b == 0 else a/b,
}

JOKERS = {
    "Floor Half": {
        "cost": 8,
        "desc": "Once per round: committed value x -> floor(x/2)."
    },
    "Successor": {
        "cost": 7,
        "desc": "Once per round: committed value x -> x+1."
    },
    "Predecessor": {
        "cost": 7,
        "desc": "Once per round: committed value x -> x-1."
    },
    "Reroll": {
        "cost": 6,
        "desc": "Once per round: reroll the current 3 numbers."
    },
    "Wild Operator": {
        "cost": 10,
        "desc": "Once per round: replace current operator with any basic operator."
    },
    "Memory": {
        "cost": 14,
        "desc": "Stored value no longer replaces a random number."
    },
}

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Exact Arithmetic Roguelike")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)

        self.round = 1
        self.hp = 4
        self.money = 0
        self.target = 1
        self.hand_no = 1
        self.max_hands = 4

        self.stored = None
        self.committed = None

        self.numbers = []
        self.op = "+"
        self.selected = []
        self.result = None

        self.jokers = []
        self.used_this_round = set()
        self.in_shop = False

        self.make_ui()
        self.start_round()

    def make_ui(self):
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#111318", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.header = self.canvas.create_text(
            30, 25, anchor="nw", fill="white",
            font=("Segoe UI", 18, "bold"),
            text=""
        )
        self.status = self.canvas.create_text(
            30, 65, anchor="nw", fill="#c7ccd6",
            font=("Segoe UI", 12),
            text=""
        )

        self.target_text = self.canvas.create_text(
            WIDTH//2, 115, fill="#ffd166",
            font=("Segoe UI", 40, "bold"),
            text="TARGET: 0"
        )

        self.commit_text = self.canvas.create_text(
            WIDTH//2, 170, fill="#9fd3ff",
            font=("Segoe UI", 14, "bold"),
            text=""
        )

        self.op_text = self.canvas.create_text(
            WIDTH//2, 225, fill="white",
            font=("Segoe UI", 30, "bold"),
            text="+"
        )

        self.number_buttons = []
        for x in (300, 490, 680):
            b = tk.Button(
                self.root,
                width=8, height=2,
                font=("Segoe UI", 18, "bold"),
                command=lambda i=len(self.number_buttons): self.select_number(i)
            )
            self.number_buttons.append(b)
            self.canvas.create_window(x, 305, window=b)

        self.result_text = self.canvas.create_text(
            WIDTH//2, 390, fill="#95f29a",
            font=("Segoe UI", 22, "bold"),
            text=""
        )

        self.submit_btn = tk.Button(self.root, text="SUBMIT", width=14, height=2,
                                    command=self.submit_result, state="disabled")
        self.store_btn = tk.Button(self.root, text="STORE", width=14, height=2,
                                   command=self.store_result, state="disabled")
        self.commit_btn = tk.Button(self.root, text="COMMIT", width=14, height=2,
                                    command=self.commit_result, state="disabled")

        self.canvas.create_window(340, 455, window=self.submit_btn)
        self.canvas.create_window(490, 455, window=self.store_btn)
        self.canvas.create_window(640, 455, window=self.commit_btn)

        self.joker_frame = tk.Frame(self.root, bg="#111318")
        self.canvas.create_window(WIDTH//2, 560, window=self.joker_frame)

        self.help_text = self.canvas.create_text(
            WIDTH//2, 645, fill="#727985",
            font=("Segoe UI", 10),
            text="Choose two numbers. If committed, choose one number to combine with the committed value."
        )

    def fmt(self, x):
        if x is None:
            return "-"
        if isinstance(x, float) and abs(x-round(x)) < 1e-9:
            return str(int(round(x)))
        if isinstance(x, float):
            return f"{x:.3f}".rstrip("0").rstrip(".")
        return str(x)

    def start_round(self):
        self.in_shop = False
        self.hand_no = 1
        self.stored = None
        self.committed = None
        self.used_this_round = set()
        self.target = random.randint(1, 5*self.round)
        self.new_hand()

    def new_hand(self):
        if self.hand_no > self.max_hands:
            self.fail_round()
            return

        self.selected = []
        self.result = None

        # Draw 3, with stored replacing one slot unless Memory is owned.
        fresh_count = 3
        nums = [random.randint(1,5) for _ in range(fresh_count)]
        if self.stored is not None and "Memory" not in self.jokers:
            nums[0] = self.stored
        elif self.stored is not None and "Memory" in self.jokers:
            nums.append(self.stored)

        self.numbers = nums[:]
        self.op = random.choice(list(OPS))
        self.refresh()

    def refresh(self):
        self.canvas.itemconfig(self.header,
            text=f"Round {self.round}    HP {self.hp}    ${self.money}    Hand {self.hand_no}/{self.max_hands}")
        self.canvas.itemconfig(self.status,
            text=f"Stored: {self.fmt(self.stored)}    Jokers: {', '.join(self.jokers) if self.jokers else 'None'}")
        self.canvas.itemconfig(self.target_text, text=f"TARGET: {self.target}")

        if self.committed is None:
            self.canvas.itemconfig(self.commit_text, text="No committed value")
        else:
            self.canvas.itemconfig(self.commit_text, text=f"COMMITTED: {self.fmt(self.committed)}  (must use next operation)")

        self.canvas.itemconfig(self.op_text, text=self.op)
        self.canvas.itemconfig(self.result_text,
            text="" if self.result is None else f"RESULT: {self.fmt(self.result)}")

        # recreate number buttons if hand has 4 due to Memory
        for b in self.number_buttons:
            b.destroy()
        self.number_buttons = []

        count = len(self.numbers)
        spacing = 150
        start_x = WIDTH//2 - spacing*(count-1)/2

        for i, val in enumerate(self.numbers):
            b = tk.Button(
                self.root,
                text=self.fmt(val),
                width=7, height=2,
                font=("Segoe UI", 18, "bold"),
                command=lambda i=i: self.select_number(i)
            )
            if i in self.selected:
                b.config(relief="sunken", bg="#cfe8ff")
            self.number_buttons.append(b)
            self.canvas.create_window(start_x+i*spacing, 305, window=b)

        state = "normal" if self.result is not None else "disabled"
        self.submit_btn.config(state=state)
        self.store_btn.config(state=state)
        self.commit_btn.config(state=state)

        for w in self.joker_frame.winfo_children():
            w.destroy()

        for name in self.jokers:
            usable = name not in self.used_this_round
            btn = tk.Button(
                self.joker_frame,
                text=name,
                state="normal" if usable else "disabled",
                command=lambda n=name: self.use_joker(n)
            )
            btn.pack(side="left", padx=5)

    def select_number(self, idx):
        if self.result is not None:
            return

        if self.committed is not None:
            # committed mode: choose exactly one fresh/stored number
            self.selected = [idx]
            b = self.numbers[idx]
            self.result = self.apply_op(self.committed, b, self.op)
            if self.result is None:
                self.result = self.apply_op(b, self.committed, self.op)
            self.refresh()
            return

        if idx in self.selected:
            self.selected.remove(idx)
        else:
            if len(self.selected) < 2:
                self.selected.append(idx)

        if len(self.selected) == 2:
            a = self.numbers[self.selected[0]]
            b = self.numbers[self.selected[1]]
            self.result = self.apply_op(a, b, self.op)
            if self.result is None:
                self.result = self.apply_op(b, a, self.op)

        self.refresh()

    def apply_op(self, a, b, op):
        try:
            r = OPS[op](a,b)
            if r is None or not math.isfinite(float(r)):
                return None
            return r
        except Exception:
            return None

    def submit_result(self):
        if self.result is None:
            return
        if abs(float(self.result) - self.target) < 1e-9:
            unused = self.max_hands - self.hand_no
            gain = 5 + 2*unused
            self.money += gain
            messagebox.showinfo("Exact!", f"Hit {self.target} exactly.\n+${gain}")
            self.round += 1
            if self.round % 3 == 1:
                self.open_shop()
            else:
                self.start_round()
        else:
            messagebox.showinfo("Miss", f"{self.fmt(self.result)} is not {self.target}.")
            self.advance_hand()

    def store_result(self):
        if self.result is None:
            return
        self.stored = self.result
        self.committed = None
        self.advance_hand()

    def commit_result(self):
        if self.result is None:
            return
        self.committed = self.result
        self.advance_hand()

    def advance_hand(self):
        self.hand_no += 1
        self.new_hand()

    def fail_round(self):
        self.hp -= 1
        if self.hp <= 0:
            messagebox.showinfo("Run Over", f"You reached round {self.round}.")
            self.restart_run()
        else:
            messagebox.showinfo("Failed", f"Target {self.target} missed.\nLose 1 HP.")
            self.start_round()

    def restart_run(self):
        self.round = 1
        self.hp = 4
        self.money = 0
        self.jokers = []
        self.start_round()

    def use_joker(self, name):
        if name in self.used_this_round:
            return

        if name == "Floor Half":
            if self.committed is None:
                messagebox.showinfo("Floor Half", "You need a committed value.")
                return
            self.committed = math.floor(self.committed/2)

        elif name == "Successor":
            if self.committed is None:
                messagebox.showinfo("Successor", "You need a committed value.")
                return
            self.committed += 1

        elif name == "Predecessor":
            if self.committed is None:
                messagebox.showinfo("Predecessor", "You need a committed value.")
                return
            self.committed -= 1

        elif name == "Reroll":
            base = [random.randint(1,5) for _ in range(3)]
            if self.stored is not None and "Memory" not in self.jokers:
                base[0] = self.stored
            elif self.stored is not None and "Memory" in self.jokers:
                base.append(self.stored)
            self.numbers = base
            self.selected = []
            self.result = None

        elif name == "Wild Operator":
            top = tk.Toplevel(self.root)
            top.title("Choose Operator")
            tk.Label(top, text="Choose this hand's operator").pack(pady=8)
            for op in OPS:
                tk.Button(top, text=op, width=10,
                          command=lambda o=op, t=top: self.choose_op(o,t)).pack(padx=15,pady=3)
            return

        elif name == "Memory":
            return

        self.used_this_round.add(name)
        self.selected = []
        self.result = None
        self.refresh()

    def choose_op(self, op, top):
        self.op = op
        self.used_this_round.add("Wild Operator")
        self.selected = []
        self.result = None
        top.destroy()
        self.refresh()

    def open_shop(self):
        self.in_shop = True
        shop = tk.Toplevel(self.root)
        shop.title("Shop")
        shop.geometry("520x430")
        shop.configure(bg="#181b22")
        shop.transient(self.root)
        shop.grab_set()

        tk.Label(shop, text=f"SHOP   ${self.money}",
                 font=("Segoe UI", 20, "bold"),
                 fg="white", bg="#181b22").pack(pady=15)

        choices = random.sample(list(JOKERS), k=min(3, len(JOKERS)))
        for name in choices:
            data = JOKERS[name]
            frame = tk.Frame(shop, bg="#232733", padx=10, pady=8)
            frame.pack(fill="x", padx=15, pady=6)

            tk.Label(frame, text=f"{name}  ${data['cost']}",
                     font=("Segoe UI", 13, "bold"),
                     fg="white", bg="#232733").pack(anchor="w")
            tk.Label(frame, text=data["desc"],
                     fg="#c7ccd6", bg="#232733",
                     wraplength=440, justify="left").pack(anchor="w")

            state = "disabled" if name in self.jokers else "normal"
            tk.Button(frame, text="BUY", state=state,
                      command=lambda n=name, s=shop: self.buy_joker(n,s)).pack(anchor="e")

        tk.Button(shop, text="LEAVE SHOP", width=18,
                  command=lambda: self.leave_shop(shop)).pack(pady=15)

    def buy_joker(self, name, shop):
        cost = JOKERS[name]["cost"]
        if name in self.jokers:
            return
        if self.money < cost:
            messagebox.showinfo("Shop", "Not enough money.")
            return
        self.money -= cost
        self.jokers.append(name)
        shop.destroy()
        self.open_shop()

    def leave_shop(self, shop):
        shop.destroy()
        self.start_round()

if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()