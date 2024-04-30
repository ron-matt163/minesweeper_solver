import tkinter as tk
# import threading


# Global variables for GUI elements
root = None
gui_labels = []

def update_gui(state):
    global gui_labels
    for i in range(len(gui_labels)):
        for j in range(len(gui_labels[0])):
            gui_labels[i][j].config(text=str(state[i][j]))
    root.update()

def setup_gui(rows, cols, initial_state):
    global root, gui_labels
    root = tk.Tk()
    root.title("Minesweeper")
    # Create gui_labels grid
    gui_labels = [[None for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            gui_labels[i][j] = tk.Label(root, width=3, height=2, relief="raised", borderwidth=2)
            gui_labels[i][j].grid(row=i, column=j, padx=1, pady=1)

    # Initialize GUI with initial state
    update_gui(initial_state)
    # Run the main GUI event loop
    # print("Before root mainloop")
    # root.mainloop()
    # print("After root mainloop")

def gui_mainloop():
    root.mainloop()