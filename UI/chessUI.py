import tkinter as tk
window = tk.Tk()

label = tk.Label(text ="Input Difficulty (1-20):")
entry = tk.Entry()
button = tk.Button(text = "Click to start", width = 25, height = 5, bg = "red", fg = "white")
button.pack()
label.pack()
entry.pack()
difficulty = entry.get()
entry.delete(0)
entry.insert(0, "10")

window.mainloop()