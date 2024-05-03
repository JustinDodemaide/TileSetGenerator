from tkinter import *
from tkinter import colorchooser

wall_interior_color = "grey"
selected_color = "black"
grid_on = True

def mouse_pressed(event):
    if event.widget.master == canvas_frame:
        frame = event.widget
        info = frame.grid_info()
        row = info['row']
        column = info['column']
        if row < 3:
            return
        frame.configure(bg=selected_color)
        if row == 3:
            frames[0][column].configure(bg=frames[3][column]["background"])
        for i in range(16):
            frames[0][i].configure(bg=frames[3][i]["background"])

def button_pressed():
    print("Button Pressed!")

def change_color():
    global selected_color
    selected_color = colorchooser.askcolor(title="Select Color")[1]

def change_interior_color():
    global wall_interior_color
    wall_interior_color = colorchooser.askcolor(title="Wall Interior Color")[1]
    for i in range(16):
        frames[1][i].configure(bg=wall_interior_color)
        frames[2][i].configure(bg=wall_interior_color)

def toggle_grid():
    global grid_on
    relief = "solid"
    if grid_on:
        relief = "flat"
    grid_on = not grid_on # Toggle
    for i in range(16):
        for j in range(16):
            frames[i][j]["relief"] = relief

def undo():
    pass

def redo():
    pass

root = Tk()
root.title("TileSet Generator")

# Create a Frame for the buttons
button_frame = Frame(root)
button_frame.grid(row=0, column=0, padx=10, sticky="ns")

interior_color_button = Button(button_frame, text="Wall Interior\nColor", command=change_interior_color)
interior_color_button.pack(pady=5)

color_button = Button(button_frame, text="Color Select", command=change_color)
color_button.pack(pady=5)

# Add example buttons to the button frame
toggle_grid = Button(button_frame, text="Toggle Grid", command=toggle_grid)
toggle_grid.pack(pady=10)

undo_button = Button(button_frame, text="Undo", command=undo)
undo_button.pack()

redo_button = Button(button_frame, text="Redo", command=redo)
redo_button.pack(pady=10)

# Create the canvas frame for the grid
canvas_frame = Frame(root, width=256, height=256)
canvas_frame.grid(row=0, column=1, sticky="nsew")

frames = [[None] * 16 for _ in range(16)]
for i in range(16):
    for j in range(16):
        frame = Frame(canvas_frame, width=16, height=16, borderwidth=0.5, relief="solid")
        frame.grid(row=i, column=j)
        frames[i][j] = frame

for i in range(16):
    frames[1][i].configure(bg=wall_interior_color)
    frames[2][i].configure(bg=wall_interior_color)

preview_frame = Frame(root, width=256, height=256)
preview_frame.grid(row=0, column=2, padx=10, sticky="ns")

root.bind("<ButtonPress-1>", mouse_pressed)
placeholder_label = Label(preview_frame, text="Placeholder")
placeholder_label.pack()

root.mainloop()
