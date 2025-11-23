import tkinter as tk
import math

fontSetting = ('Comic Sans MS', 14)

# Colors / theme
BG = "#0f1720"
ENTRY_BG = "#1f2937"
BTN_BG = "#027429"        # main green for buttons
BTN_HOVER = "#12CB53"     # hover green
ACCENT = "#03A63A"        # accent / '=' button green
TEXT = "white"
CLEAR_BG = "#b03a3a"      # clear button red
CLEAR_ACTIVE = "#ff6b6b"

def on_button_click(value, btn):
    entry.insert(tk.END, value)
    btn.config(bg=BTN_HOVER)
    btn.after(150, lambda: btn.config(bg=BTN_BG))

def calculate(event=None):
    try:
        expr = entry.get()
        # Replace math functions with math.<func>
        expr = expr.replace('sin', 'math.sin')
        expr = expr.replace('cos', 'math.cos')
        expr = expr.replace('tan', 'math.tan')
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('log', 'math.log')
        expr = expr.replace('pi', 'math.pi')
        expr = expr.replace('e', 'math.e')
        result = eval(expr)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        #result_label.config(text=f"= {result}", fg=ACCENT)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        #result_label.config(text="= Error", fg="red")

def clear(event=None):
    entry.delete(0, tk.END)
    #result_label.config(text="")

def backspace(event=None):
    cur = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, cur[:-1])

root = tk.Tk()
root.title("Science Calculator")
root.configure(bg=BG)

# Make resize behave nicely
root.rowconfigure(0, weight=0)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

entry = tk.Entry(root, width=25, font=fontSetting, bd=5, relief=tk.RIDGE, justify='right',
                 bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT)
entry.grid(row=0, column=0, columnspan=5, padx=12, pady=(12,6), sticky="we")

#result_label = tk.Label(root, text="", font=("Consolas", 14), bg=BG, fg=ACCENT, anchor="e")
#result_label.grid(row=1, column=0, columnspan=5, sticky="we", padx=12, pady=(0,8))

buttons = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('sin', 2, 4),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('cos', 3, 4),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('tan', 4, 4),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('log', 5, 4),
    ('(', 6, 0), (')', 6, 1), ('pi', 6, 2), ('e', 6, 3), ('sqrt', 6, 4),
]

btn_refs = {}

def make_button(text, r, c):
    btn = tk.Button(root, text=text, width=5, height=2, font=fontSetting,
                    bg=BTN_BG, fg=TEXT, activebackground=BTN_HOVER, bd=0, relief='flat')
    btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
    root.grid_rowconfigure(r, weight=0)
    root.grid_columnconfigure(c, weight=1)
    btn_refs[text] = btn
    # hover effect
    btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_BG))
    btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_BG))
    if text == '=':
        # make '=' visually distinct but still green
        btn.config(command=calculate, bg=BTN_BG, fg="white", activebackground=BTN_HOVER)
    else:
        btn.config(command=lambda t=text, b=btn: on_button_click(t, b))

for (text, row, col) in buttons:
    make_button(text, row, col)

# clear button stays red
clear_btn = tk.Button(root, text='C', width=5, height=2, font=fontSetting, command=clear,
                      bg=CLEAR_BG, fg="white", bd=0, relief='flat', activebackground=CLEAR_ACTIVE, activeforeground="white")
clear_btn.grid(row=7, column=0, columnspan=5, sticky='we', padx=12, pady=(6,12))

# Key bindings for convenience
def bind_keys():
    for ch in "0123456789.+-*/()":
        root.bind(ch, lambda e, c=ch: entry.insert(tk.END, c))
    root.bind("<Return>", calculate)
    root.bind("<KP_Enter>", calculate)
    root.bind("<space>", clear)
    root.bind("<BackSpace>", backspace)
    # map letters for functions
    root.bind("s", lambda e: entry.insert(tk.END, "sin"))
    root.bind("c", lambda e: entry.insert(tk.END, "cos"))
    root.bind("t", lambda e: entry.insert(tk.END, "tan"))
    root.bind("p", lambda e: entry.insert(tk.END, "pi"))

bind_keys()

root.mainloop()