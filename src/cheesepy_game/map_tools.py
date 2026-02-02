from unittest import case
from . import game_status as gs
from .cell import Cell_types
from importlib.resources import files
from .position import Position
from .level import Level
from .config import DEFAULT_CELL_SIDE

DEFAULT_MAP_SAVE_FNAME = "map.ppm"

IMAGE_WALL_COLOR = "255\n0\n0"
IMAGE_WATER_COLOR = "0\n255\n255"
IMAGE_FLOOR_COLOR = "0\n0\n0"

# def setup_cells_from_matrix(ndarray):
#     """Setup the cell type given a 2D array that contains valid cell type values."""
#     for r in range(ndarray.shape[0]):
#         for c in range(ndarray.shape[1]):
#             gs._cells[r][c] = ndarray[r, c]


def save_map_to_image(fname):
    f""" save walls as PPM bitmap image in the working directory, under the name {DEFAULT_MAP_SAVE_FNAME}."""
    cells = gs._cells
    h = len(cells)
    w = len(cells[0])

    lines = ["P3", f"{w} {h}", "1"]
    for _, row in enumerate(cells):
        l = []
        for c, cell in enumerate(row):
            if cell.type == Cell_types.WALL:
                c = IMAGE_WALL_COLOR
            elif cell.type == Cell_types.WATER:
                c = IMAGE_WATER_COLOR
            else:
                c = IMAGE_FLOOR_COLOR
            l.append(c)
        lines.append("\n".join(l))

    txt = '\n'.join(lines)
    with open(DEFAULT_MAP_SAVE_FNAME, 'w', encoding="utf-8") as f:
        f.write(txt)
    print(txt)


def load_map_from_image(fname):
    """Read a PPM-ascii file in the pagkage maps folder and convert it into a 2D list.
    Values:
     - 1 represents walls
     - 2 represents water
     - whereas 0 represents FLOOR cells."""
    imagr_file = files('cheesepy_game.maps').joinpath(fname)
    txt = imagr_file.read_text(encoding="utf-8")
    lines = txt.split("\n")
    # remove comments
    lines = list(filter(lambda line: line[0:1] != '#', lines))
    w, h = [int(x) for x in lines[1].split()]
    # max_i = int(lines[2])
    pixels = lines[3:]
    cells = []
    for r in range(h):
        cells.append([])
        for c in range(w):
            i = r*w*3+3*c
            pixel = tuple(int(x) for x in pixels[i:i+3])
            match pixel:
                case (255,0,0):
                    # wall
                    v = 1
                case (0,255,255) | (0,1,1):
                    # water
                    v = 2
                case _:
                    v = 0

            cells[r].append(v)
    return cells


def walls_and_water_from_map(fname):
    """Get a list of wall-cells positions from the corresponding map file"""
    map = load_map_from_image(fname)
    h = len(map)
    w = len(map[0])
    water = []
    walls = []
    for r, row in enumerate(map):
        for c, x in enumerate(row):
            match x:
                case 1:
                    walls.append([c, r])
                case 2:
                    water.append([c, r])
    return h, w, walls, water


def new_level_from_map(fname, player_init_position: Position, exits, items, check_victory, instructions,
                       cell_side=DEFAULT_CELL_SIDE, show_grid_borders=False):
    """Create a new level using a map in the maps folder"""
    h, w, walls, water = walls_and_water_from_map(fname)
    return Level(
        ROWS=h,
        COLS=w,
        cell_side=cell_side,
        player_init_position=player_init_position,
        check_victory=check_victory,
        exits=exits,
        items=items,
        instructions=instructions,
        wall_positions=walls,
        water_positions=water,
        show_grid_borders=show_grid_borders
    )
