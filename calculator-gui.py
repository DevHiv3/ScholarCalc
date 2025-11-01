import tkinter as tk
import math

root = tk.Tk()
root.title("Minimalistic Calculator")
root.geometry("600x800")
root.config(bg="#f5f5f7")
root.resizable(True, True)

display = tk.Entry(
    root,
    font=("SF Pro Display", 32, "bold"),
    bg="#f5f5f7",
    fg="#000000",
    border=0,
    justify="right",
)
display.grid(row=0, column=0, columnspan=6, pady=(30, 20), padx=20, ipady=20, sticky="nsew")

def on_click(event):
    text = event.widget.cget("text")
    if text == "C":
        display.delete(0, tk.END)
    elif text == "⌫":
        current = display.get()
        display.delete(0, tk.END)
        display.insert(tk.END, current[:-1])
    elif text == "=":
        try:
            expr = display.get().replace("×", "*").replace("÷", "/").replace("−", "-")
            expr = expr.replace("^", "**")
            expr = expr.replace("π", "math.pi").replace("e", "math.e")
            expr = expr.replace("√", "math.sqrt")
            # allow sin, cos, tan, log, ln etc.
            for fn in ["sin", "cos", "tan", "log", "ln"]:
                if fn in expr:
                    expr = expr.replace(fn + "(", f"math.{ 'log' if fn=='ln' else fn }(")
            result = eval(expr)
            display.delete(0, tk.END)
            display.insert(tk.END, str(result))
        except Exception:
            display.delete(0, tk.END)
            display.insert(tk.END, "Error")
    elif text == "x²":
        try:
            val = float(display.get())
            display.delete(0, tk.END)
            display.insert(tk.END, val ** 2)
        except:
            display.insert(tk.END, "**2")
    else:
        display.insert(tk.END, text)

def create_button(parent, text, row, col, bg, fg):
    btn = tk.Label(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        font=("SF Pro Display", 20, "bold"),
        bd=0,
        relief="flat",
        highlightthickness=0,
        cursor="hand2",
    )
    btn.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
    btn.bind("<Button-1>", on_click)
    btn.bind("<Enter>", lambda e: btn.config(bg="#e5e5e7"))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

num_color = "#ffffff"
op_color = "#ff9500"
util_color = "#d1d1d6"

frame = tk.Frame(root, bg="#f5f5f7")
frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=5)
root.grid_columnconfigure(0, weight=1)

# scientific layout
buttons = [
    ["C", "⌫", "(", ")", "÷", "×"],
    ["7", "8", "9", "−", "x²", "√("],
    ["4", "5", "6", "+", "sin(", "cos("],
    ["1", "2", "3", "=", "tan(", "log("],
    ["0", ".", "π", "e", "ln(", "^"],
]

for r in range(len(buttons)):
    frame.grid_rowconfigure(r, weight=1)
    for c in range(6):
        frame.grid_columnconfigure(c, weight=1)

for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        if not char:
            continue
        if char in {"÷", "×", "−", "+", "=", "^"}:
            create_button(frame, char, r, c, bg=op_color, fg="white")
        elif char in {"C", "⌫"}:
            create_button(frame, char, r, c, bg=util_color, fg="black")
        else:
            create_button(frame, char, r, c, bg=num_color, fg="black")

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)

root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)
display.focus_set()
root.mainloop()
