import tkinter as tk

window = tk.Tk()

btn_resign = tk.Button(master=window, text="RESIGN", bg="red")
btn_resign.grid(row=0, column=6, sticky="nsew")
def handle_click1(event):
    print ("You have resigned. Better luck next time!")
btn_resign.bind("<Button-1>", handle_click1)

btn_draw = tk.Button(master=window, text="DRAW", bg="yellow")
btn_draw.grid(row=1, column=6, sticky="nsew")
def handle_click2(event):
    print ("It is a draw!")
btn_draw.bind("<Button-1>", handle_click2)

btn_reset = tk.Button(master=window, text="RESTART", bg="green")
btn_reset.grid(row=2, column=6, sticky="nsew")
def handle_click3(event):
    print("Your game will reset now!")
btn_reset.bind("<Button-1>", handle_click3)

window.mainloop()
