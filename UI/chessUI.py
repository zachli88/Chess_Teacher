import tkinter as tk
window = tk.Tk()

label = tk.Label(text ="Input Difficulty (1-20): ")
entry = tk.Entry()
label.pack()
entry.pack()
difficulty = entry.get()

window.mainloop()
