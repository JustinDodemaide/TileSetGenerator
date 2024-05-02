from PIL import Image

WALL_INTERIOR: tuple = (91, 91, 109)

class Commands:
    COPY_FRONT: int = 0
    COPY_SIDE: int = 1

class Area:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.top_left = top_left
        self.bottom_right = bottom_right

NW_CORNER = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): WALL_INTERIOR,
}

NE_CORNER = {
    Area((0, 0), (9, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): WALL_INTERIOR,
}

SE_CORNER = {
    Area((0, 0), (9, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): WALL_INTERIOR,
}

SW_CORNER = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): WALL_INTERIOR,
}

FRONT_TO_SIDE_TOP = {
    Area((0, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0),(9, 0)): Commands.COPY_SIDE
}

FRONT_TO_SIDE_BOTTOM = {
    Area((0, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): WALL_INTERIOR,
    Area((9, 1), (9, 2)): WALL_INTERIOR,
}

SIDE_TO_FRONT_RIGHT = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 15)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): WALL_INTERIOR,
}

SIDE_TO_FRONT_LEFT = {
    Area((0, 0), (6, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): WALL_INTERIOR,
}

SIDE_END_BOTTOM = {
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((6, 3), (9, 14)): Commands.COPY_FRONT,
    Area((7, 15), (8, 15)): Commands.COPY_FRONT,
}

SIDE_END_TOP = {
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((7, 3), (8, 3)): Commands.COPY_FRONT
}

FRONT_END_RIGHT = {
    Area((0, 0), (12, 15)): Commands.COPY_FRONT,
}

FRONT_END_LEFT = {

}

def make_side_tile():
    # Decided that making the side tile a special case was a
    # better alternative to a >32 line dictionary
    tile = Image.new(mode="RGB", size=(16, 16))
    pixels = tile.load()

    # Left column
    LEFT_X = 6
    RIGHT_X = 9
    x = LEFT_X
    front_y = 0
    while x <= RIGHT_X:
        for i in range(16):
           pixels[x, i] = front_pixels[i, front_y]
        x += 1
        front_y += 1
    return tile

def make_tile(instructions: dict):
    tile = Image.new(mode="RGB", size=(16, 16))
    pixels = tile.load()
    for area in instructions:
        command = instructions[area]
        match command:
            case Commands.COPY_FRONT:
                copy_area(front_pixels, pixels, area)
            case Commands.COPY_SIDE:
                copy_area(side_pixels,pixels,area)
            case WALL_INTERIOR:
                apply_color_to_area(pixels, area, WALL_INTERIOR)
    return tile

def copy_area(copy_from, copy_to, area: Area):
    X = 0
    Y = 1
    y = area.top_left[Y]
    while(y <= area.bottom_right[Y]):
        x = area.top_left[X]
        while(x <= area.bottom_right[X]):
            # print("applying ", copy_from[x, y], " to (", x, ", ", y, ")")
            copy_to[x, y] = copy_from[x, y]
            x += 1
        y += 1

def apply_color_to_area(to, area, color):
    X = 0
    Y = 1
    y = area.top_left[Y]
    while(y <= area.bottom_right[Y]):
        x = area.top_left[X]
        while(x <= area.bottom_right[X]):
            # print("applying ", color, " to (", x, ", ", y, ")")
            to[x, y] = color
            x += 1
        y += 1

front = Image.open("C:\\Users\\jmdod\\Desktop\\front.png")
front_pixels = front.convert("RGB").load()

side = make_side_tile()
side_pixels = side.convert("RGB").load()

map_image = Image.new(mode="RGB", size=(80, 80))
map_image.paste(make_tile(NW_CORNER),(0, 0))
map_image.paste(make_tile(FRONT_TO_SIDE_BOTTOM),(48, 0))
map_image.paste(make_tile(NE_CORNER),(64, 0))
map_image.paste(make_tile(SIDE_END_BOTTOM),(0, 16))
map_image.paste(side,(64, 16))
#map_image.paste(make_tile(SIDE_END_TOP),(0, 32))
#make_tile(SIDE_END_TOP).show()
map_image.paste(make_tile(SIDE_TO_FRONT_RIGHT),(0, 48))
map_image.paste(make_tile(FRONT_TO_SIDE_TOP),(16, 48))
map_image.paste(make_tile(SIDE_TO_FRONT_LEFT),(64, 48))
map_image.paste(make_tile(SW_CORNER),(0, 64))
map_image.paste(front,(16, 64))
map_image.paste(make_tile(FRONT_END_RIGHT),(32, 64))
map_image.paste(make_tile(FRONT_END_LEFT),(48, 64))
map_image.paste(make_tile(SE_CORNER),(64, 64))

map_image.show()
map_image.save("test.png")