import tkinter as tk
from tkinter import ttk
from sympy import *
import math

class ScholarCalc(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ScholarCalc – Advanced Scientific Calculator")
        self.geometry("850x600")
        self.configure(bg="#0B0C10")
        self.resizable(True, True)
        self._expr = ""
        self.history = []
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        style.configure("TButton", font=("Segoe UI", 12), padding=3)

        # === Display ===
        self.display = tk.Entry(self, font=("Consolas", 22), bg="#1F2833", fg="#66FCF1",
                                insertbackground="#66FCF1", relief="flat", justify="right", bd=10)
        self.display.pack(fill="x", ipady=12, pady=(10, 5), padx=10)

        # === Main frame ===
        self.main_frame = tk.Frame(self, bg="#0B0C10")
        self.main_frame.pack(expand=True, fill="both", padx=8, pady=8, side="left")

        # === History Panel ===
        self.history_frame = tk.Frame(self, bg="#101820")
        self.history_frame.pack(side="right", fill="y", padx=(0, 10))
        tk.Label(self.history_frame, text="History", bg="#101820", fg="#F2AA4C",
                 font=("Segoe UI", 14, "bold")).pack(pady=(5, 5))
        self.history_box = tk.Listbox(self.history_frame, font=("Consolas", 12),
                                      bg="#1F2833", fg="#C5C6C7", selectbackground="#45A29E",
                                      relief="flat", activestyle="none")
        self.history_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.clear_history_btn = tk.Button(self.history_frame, text="Clear",
                                           bg="#F2AA4C", fg="black",
                                           font=("Segoe UI", 10, "bold"),
                                           command=self._clear_history)
        self.clear_history_btn.pack(pady=(0, 10))

        self._build_buttons()

    def _mkbtn(self, parent, text, r, c, cmd=None, bg="#1F2833", fg="#C5C6C7",
               hover="#45A29E", special=False):
        btn = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                        bg=bg, fg=fg, activebackground=hover, activeforeground="white",
                        relief="flat", width=6, height=2,
                        command=lambda: cmd(text) if cmd else None,
                        borderwidth=0, highlightthickness=0)

        # Special styling for "=" button
        if special:
            btn.configure(bg="#F2AA4C", fg="black", activebackground="#FFD580", font=("Segoe UI", 12, "bold"))

            def on_enter(e): btn.config(bg="#FFD580", fg="black")
            def on_leave(e): btn.config(bg="#F2AA4C", fg="black")
        else:
            def on_enter(e): btn.config(bg=hover)
            def on_leave(e): btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

        parent.grid_columnconfigure(c, weight=1)
        parent.grid_rowconfigure(r, weight=1)

    def _build_buttons(self):
        btns = [
            ["7", "8", "9", "/", "sin", "cos", "tan"],
            ["4", "5", "6", "*", "log", "ln", "√"],
            ["1", "2", "3", "-", "x²", "x³", "|x|"],
            ["0", ".", "=", "+", "π", "e", "!"],
            ["diff", "∫", "exp", "mod", "floor", "ceil", "frac"],
            ["(", ")", "C", "DEL", "^", "Ans", "Exit"]
        ]

        for r, row in enumerate(btns):
            for c, ch in enumerate(row):
                special = (ch == "=")
                self._mkbtn(self.main_frame, ch, r, c, self._on_click, special=special)

    def _on_click(self, ch):
        if ch == "C":
            self._expr = ""
        elif ch == "DEL":
            self._expr = self._expr[:-1]
        elif ch == "=":
            try:
                result = self._evaluate(self._expr)
                self.history.append(f"{self._expr} = {result}")
                self.history_box.insert(tk.END, f"{self._expr} = {result}")
                self._expr = str(result)
            except Exception:
                self._expr = "Error"
        elif ch == "Exit":
            self.destroy()
            return
        elif ch == "Ans":
            if self.history:
                last = self.history[-1].split(" = ")[-1]
                self._expr += last
        else:
            mapping = {
                "×": "*", "÷": "/", "−": "-", "√": "sqrt(", "π": "pi", "e": "E",
                "x²": "**2", "x³": "**3", "^": "**", "sin": "sin(", "cos": "cos(",
                "tan": "tan(", "log": "log10(", "ln": "log(", "mod": "%", "|x|": "Abs(",
                "floor": "floor(", "ceil": "ceiling(", "exp": "exp(", "frac": "fractional_part(",
                "diff": "diff(", "∫": "integrate(", "!": "factorial("
            }
            self._expr += mapping.get(ch, ch)

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self._expr)

    def _evaluate(self, expr):
        x = symbols('x')
        expr = expr.replace("fractional_part", "frac")
        expr = expr.replace("^", "**")
        try:
            res = sympify(expr, evaluate=True)
            if isinstance(res, (int, float)):
                return res
            return N(res)
        except Exception:
            return eval(expr, {"__builtins__": None}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "sqrt": math.sqrt,
                "log": math.log10, "ln": math.log, "pi": math.pi, "e": math.e,
                "factorial": math.factorial, "floor": math.floor, "ceil": math.ceil,
                "Abs": abs, "exp": math.exp
            })

    def _clear_history(self):
        self.history.clear()
        self.history_box.delete(0, tk.END)


if __name__ == "__main__":
    app = ScholarCalc()
    app.mainloop()
