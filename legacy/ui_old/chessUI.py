import tkinter as tk

def increase():
    value = int(lbl_value["text"])
    if value < 20:
        lbl_value["text"] = f"{value + 1}"

def decrease():
    value = int(lbl_value["text"])
    if value > 1:
        lbl_value["text"] = f"{value - 1}"

window = tk.Tk()

window.rowconfigure(0, minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

label = tk.Label(text ="Set your difficulty (Min Difficulty: 1, Max Difficulty: 20")
label.grid(row = 0, column = 1)

btn_decrease = tk.Button(master=window, text="-", command = decrease)
btn_decrease.grid(row=1, column=0, sticky="nsew")

lbl_value = tk.Label(master=window, text="1")
lbl_value.grid(row=1, column=1)

btn_increase = tk.Button(master=window, text="+", command = increase)
btn_increase.grid(row=1, column=2, sticky="nsew")

btn_start = tk.Button(master=window, text="start game", bg="green")
btn_start.grid(row=2, column=1, sticky="nsew")
def handle_click(event):
    return int(lbl_value["text"])
btn_start.bind("<Button-1>", handle_click)

window.mainloop()
