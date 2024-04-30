import tkinter as tk
import numpy as np
# import threading


# Global variables for GUI elements
root = None
gui_labels = []

number_image_map = {
    0: "../assets/opened_blank.png",
    1: "../assets/1.png",
    2: "../assets/2.png",
    3: "../assets/3.png",
    4: "../assets/4.png",
    5: "../assets/5.png",
    6: "../assets/6.png",
    7: "../assets/7.png",
    8: "../assets/8.png",
    -1: "../assets/mine.png",
    -2: "../assets/blank.png",
    -3: "../assets/flag.png",
    -4: "../assets/win.png"
}

def update_gui(state, game_over=False):
    global gui_labels
    for i in range(len(gui_labels)):
        for j in range(len(gui_labels[0])):
            if np.isnan(state[i][j]):
                gui_labels[i][j].config(image=number_image_map[-2])
            else:
                gui_labels[i][j].config(image=number_image_map[int(state[i][j])])

    if game_over:
        # If game is won
        if -1 not in state:
            for i in range(len(gui_labels)):
                for j in range(len(gui_labels[0])):
                    if np.isnan(state[i][j]):
                        gui_labels[i][j].config(image=number_image_map[-4])
    root.update()

def setup_gui(rows, cols, initial_state):
    global root, gui_labels
    root = tk.Tk()
    root.title("Minesweeper")
    # Create gui_labels grid
    gui_labels = [[None for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            gui_labels[i][j] = tk.Label(root, width=29, height=29)
            gui_labels[i][j].grid(row=i, column=j)

    # creating image variable and storing them in the dictionary
    for key, value in number_image_map.items():
        number_image_map[key] = tk.PhotoImage(file=value).subsample(4,4)

    # Initialize GUI with initial state
    update_gui(initial_state)


def gui_mainloop():
    root.mainloop()