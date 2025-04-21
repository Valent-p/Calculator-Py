import tkinter as tk
import re

CURSOR = "_"
blinker_count = 0
had_error = False

def btn_click(value):
    global had_error
    if had_error:
        return

    screen_text.config(state="normal")
    yview = screen_text.yview()

    content = screen_text.get("1.0", "end-1c")
    content = content[:-1]  # remove old blinker
    screen_text.delete("1.0", "end")
    screen_text.insert("1.0", content + str(value) + CURSOR[0])
    screen_text.tag_add("cursor", "end-2c", "end-1c")

    screen_text.yview_moveto(yview[0])
    screen_text.config(state="disabled")
    
def delete_click():
    screen_text.config(state="normal")
    yview = screen_text.yview()
    
    global had_error
    if had_error:
        screen_text.delete("2.0", "end")
        had_error = False
    else:
        content = screen_text.get("1.0", "end-1c")[:-1]  # remove blinker
        if content:
            content = content[:-1]  # remove last character
        screen_text.delete("1.0", "end")
        screen_text.insert("1.0", content + CURSOR[0])
        screen_text.tag_add("cursor", "end-2c", "end-1c")

    screen_text.yview_moveto(yview[0])
    screen_text.config(state="disabled")

def equal_click():
    global had_error
    if had_error:
        return

    screen_text.config(state="normal")
    yview = screen_text.yview()

    try:
        content = screen_text.get("1.0", "end-1c")[:-1]  # remove blinker
        content = re.sub(r"\b0+(\d+)", r"\1", content)
        result = str(eval(content))
        screen_text.delete("1.0", "end")
        screen_text.insert("1.0",  result + CURSOR[0])
        screen_text.tag_add("cursor", "end-2c", "end-1c")
        
    except (SyntaxError, ZeroDivisionError) as e:
        #screen_text.delete("1.0", "end")
        err = "\nError: "  + ( "Invalid Math Syntax" if type(e) == SyntaxError else str(e) )
        screen_text.insert("2.0",  err+"\n")
        screen_text.tag_add("error", f"end-{len(err)+1}c", "end-1c")
        
        had_error = True
    
    screen_text.yview_moveto(yview[0])
    screen_text.config(state="disabled")

def generate_btns(frame, data):
    btns = []
    for r, row in enumerate(data):
        btns_row = []
        for c, item in enumerate(row):
            btn = tk.Button(
                frame,
                font=("Courier", 14),
                text=str(item),
                command=lambda v=item: btn_click(str(v))
            )
            btn.grid(row=r, column=c, sticky="ew", padx=5, pady=5)
            btns_row.append(btn)
        btns.append(btns_row)
    return btns

# Setup
root = tk.Tk()
screen_frame = tk.Frame(root)
screen_frame.pack(fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(screen_frame)
scrollbar.pack(side="right", fill="y")

# Scrollable text widget
screen_text = tk.Text(
    screen_frame,
    
    height=4,
    font=("Courier", 12),
    wrap="word",
    yscrollcommand=scrollbar.set
)
screen_text.pack(side="left", fill="both", expand=True)
screen_text.insert("1.0", CURSOR[0])
# colors
screen_text.tag_config("cursor", foreground="red") 
screen_text.tag_config("error", foreground="white", background="red") 

scrollbar.config(command=screen_text.yview)

btns_frame = tk.Frame(root)
btns_frame.pack()

# Buttons layout
data = [
    [1, 2, 3, "+", "*"],
    [4, 5, 6, "-", "/"],
    [7, 8, 9, "%", "//"],
    [0, '.', 'D', "="]
]

btns = generate_btns(btns_frame, data)

# Special button config
btns[3][2].configure(command=delete_click)      # 'D' delete
btns[3][3].grid(columnspan=2, sticky="ew")      # '=' spans two columns
btns[3][3].configure(command=equal_click)

root.mainloop()