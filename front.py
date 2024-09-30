import tkinter as tk

root = tk.Tk()
root.title("Simple GUI")

def on_button_click():
    print("Button clicked!")

button = tk.Button(root, text="Click Me", command=on_button_click)

button.pack(pady=20)

root.mainloop()
