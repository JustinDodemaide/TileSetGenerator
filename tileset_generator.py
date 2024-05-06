from PIL import Image

class Commands:
    COPY_FRONT: int = 0
    COPY_SIDE: int = 1
    WALL_INTERIOR_COLOR: int = 2

class Area:
    def __init__(self, top_left: tuple, bottom_right: tuple):
        self.top_left = top_left
        self.bottom_right = bottom_right

NW_CORNER = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): Commands.WALL_INTERIOR_COLOR,
}

NE_CORNER = {
    Area((0, 0), (9, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): Commands.WALL_INTERIOR_COLOR,
}

SE_CORNER = {
    Area((0, 0), (9, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): Commands.WALL_INTERIOR_COLOR,
}

SW_CORNER = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): Commands.WALL_INTERIOR_COLOR,
}

FRONT_TO_SIDE_TOP = {
    Area((0, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0),(9, 0)): Commands.COPY_SIDE
}

FRONT_TO_SIDE_BOTTOM = {
    Area((0, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 1), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): Commands.WALL_INTERIOR_COLOR,
    Area((9, 1), (9, 2)): Commands.WALL_INTERIOR_COLOR,
}

SIDE_TO_FRONT_RIGHT = {
    Area((6, 0), (15, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 15)): Commands.COPY_SIDE,
    Area((9, 1), (9, 2)): Commands.WALL_INTERIOR_COLOR,
}

SIDE_TO_FRONT_LEFT = {
    Area((0, 0), (6, 15)): Commands.COPY_FRONT,
    Area((6, 0), (9, 15)): Commands.COPY_SIDE,
    Area((6, 1), (6, 2)): Commands.WALL_INTERIOR_COLOR,
}

SIDE_END_BOTTOM = {
    Area((6, 0), (9, 2)): Commands.COPY_SIDE,
    Area((6, 3), (9, 14)): Commands.COPY_FRONT,
    Area((7, 15), (8, 15)): Commands.COPY_FRONT,
}

SIDE_END_TOP = {
    Area((6, 4), (9, 15)): Commands.COPY_SIDE,
    Area((7, 3), (8, 3)): Commands.COPY_FRONT
}

FRONT_END_LEFT = {
    Area((0, 0), (12, 15)): Commands.COPY_FRONT,
    Area((13, 1), (13, 14)): Commands.COPY_FRONT,
}

FRONT_END_RIGHT = {
    Area((3, 0), (15, 15)): Commands.COPY_FRONT,
    Area((2, 1), (2, 14)): Commands.COPY_FRONT,
}

def make_side_tile(front_pixels):
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

def make_tile(instructions: dict, info):
    front_pixels = info["front_pixels"]
    side_pixels = info["side_pixels"]
    wall_interior = info["wall_interior_color"]

    tile = Image.new(mode="RGB", size=(16, 16))
    pixels = tile.load()
    for area in instructions:
        command = instructions[area]
        if command == Commands.COPY_FRONT:
            copy_area(front_pixels, pixels, area)
        if command == Commands.COPY_SIDE:
            copy_area(side_pixels,pixels,area)
        if command == Commands.WALL_INTERIOR_COLOR:
            apply_color_to_area(pixels, area, wall_interior)
    return tile

def copy_area(copy_from, copy_to, area: Area):
    X = 0
    Y = 1
    y = area.top_left[Y]
    while y <= area.bottom_right[Y]:
        x = area.top_left[X]
        while x <= area.bottom_right[X]:
            copy_to[x, y] = copy_from[x, y]
            x += 1
        y += 1

def apply_color_to_area(to, area, color):
    X: int = 0
    Y: int = 1
    y = area.top_left[Y]
    while y <= area.bottom_right[Y]:
        x = area.top_left[X]
        while x <= area.bottom_right[X]:
            to[x, y] = color
            x += 1
        y += 1

def rounded_edge():
    pass

def generate_tileset(front_tile: Image, wall_interior_color, path="tileset.png"):
    front_pixels = front_tile.convert("RGB").load()
    side = make_side_tile(front_pixels)
    side_pixels = side.convert("RGB").load()
    info = {"front_pixels": front_pixels,
            "side_pixels": side_pixels,
            "wall_interior_color": wall_interior_color}

    map_image = Image.new(mode="RGB", size=(80, 80))
    map_image.paste(make_tile(NW_CORNER, info), (0, 0))
    map_image.paste(make_tile(FRONT_TO_SIDE_BOTTOM, info), (48, 0))
    map_image.paste(make_tile(NE_CORNER, info), (64, 0))
    map_image.paste(make_tile(SIDE_END_BOTTOM, info), (0, 16))
    map_image.paste(side, (64, 16))
    map_image.paste(make_tile(SIDE_END_TOP, info), (0, 32))
    map_image.paste(make_tile(SIDE_TO_FRONT_RIGHT, info), (0, 48))
    map_image.paste(make_tile(FRONT_TO_SIDE_TOP, info), (16, 48))
    map_image.paste(make_tile(SIDE_TO_FRONT_LEFT, info), (64, 48))
    map_image.paste(make_tile(SW_CORNER, info), (0, 64))
    map_image.paste(front_tile, (16, 64))
    map_image.paste(make_tile(FRONT_END_LEFT, info), (32, 64))
    map_image.paste(make_tile(FRONT_END_RIGHT, info), (48, 64))
    map_image.paste(make_tile(SE_CORNER, info), (64, 64))

    map_image.save(path)
    return map_image
