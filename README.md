# Tileset Generator
<p align="center">
  <img src="https://github.com/JustinDodemaide/TileSetGenerator/assets/103222511/7643fa20-cc3c-42d3-8d9c-87a907231c44" />
</p>
A tileset is a collection of textures, often of the same pixel size, that can be used to create levels in grid-based 2D games.
Creating your own tileset can be a tedious process. The goal of this program is to provide a convenient way of generating a basic set of walls and corners from a single base tile.

# How to Use
Download the executable from the latest release (tileset_editor.exe), and run it. Python isn't required because the executable contains the Python interpreter.

Running the executable opens the tile editor, where you can design the tile from which the entire tileset will be generated.

Left Mouse changes the color of a pixel to the currently selected color. Press the **Color Select** button to change the currently selected color.

Right or Middle Mouse toggles draw mode, changing the color of all hovered-over pixels without the need to left click.

You may notice the first 3 rows cannot be edited. This is ensure visual continuity of between tiles of different orientations. The 1st row is automatically updated to match the 4th row. The 2nd and 3rd rows represent the interior of the wall, the color of which can be changed by pressing **Wall Interior Color**.

**Toggle Grid** removes or adds the black outlines surrounding each pixel.

**Undo** reverses the last edited pixel to its previous color. **Redo** undoes the undo.

Pressing **Generate** creates a png of the tileset, and saves it in the executable's directory. The Preview panel is updated to display the newly generated tileset. If a tileset already exists in the directory, pressing **Generate** will overwrite it.

**Info** provides a concise version of these instructions.

This program currently only supports 16x16 pixel tiles, but you can upscale them using your preferred image editor [(Paint.NET is my go-to)](https://www.getpaint.net/). Make sure to use "Nearest Neighbor" resampling for best results.

# How it Works
Tkinter provides the GUI and input event functionalities for the tileset editor. Each pixel of the tile is a Frame. Toggling the grid involves changing the reliefs of each Frame to either solid or flat. Upon a ButtonPress-1 (left click) event, the clicked frame's background color is changed to selected_color. The location, previous color, and new color of the tile is stored in a PixelChange object, which is pushed onto the undo stack. Pressing the undo button pushes the PixelChange onto the redo stack. Pressing **Generate** calls generate_tileset() from tileset_generator.py.

80% of making a tileset is copying and pasting different parts of tiles together. I realized this process could be automated if each tile had a set of instructions of which pixels needed to be copied. The instructions are stored in a dictionary, where each key is an area (2 points, the top left and bottom right coordinates) and each value is a command thats parsed in make_tile(). The current commands are: copy from the front tile (COPY_FRONT), copy from the side tile (COPY_SIDE) or make the pixels the wall interior color (WALL_INTERIOR_COLOR). To make the tileset, each of the instruction dictionaries are processed, and the images are stitched together into one image.
