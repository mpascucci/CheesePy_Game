from . import game_status as gs
from .cell import Cell_types
from importlib.resources import files
from .position import Position
from .level import Level
from .config import DEFAULT_CELL_SIDE

DEFAULT_MAP_SAVE_FNAME = "map.ppm"


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
                c = "1\n1\n1"
            else:
                c = "0\n0\n0"
            l.append(c)
        lines.append("\n".join(l))

    txt = '\n'.join(lines)
    with open(DEFAULT_MAP_SAVE_FNAME, 'w', encoding="utf-8") as f:
        f.write(txt)
    print(txt)


def load_map_from_image(fname):
    """Read a PPM-ascii file in the pagkage maps folder and convert it into a 2D list of 0 and 1.
    The value 1 represents walls, whereas 0 represents FLOOR cells."""
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
            pixel = pixels[i:i+3]

            if int(pixel[0]) > 0:
                v = 1
            else:
                v = 0

            cells[r].append(v)
    return cells


def walls_from_map(fname):
    """Get a list of wall-cells positions from the corresponding map file"""
    map = load_map_from_image(fname)
    h = len(map)
    w = len(map[0])
    walls = []
    for r, row in enumerate(map):
        for c, x in enumerate(row):
            if x > 0:
                walls.append([c, r])
    return h, w, walls


def new_level_from_map(fname, player_init_position: Position, exits, items, check_victory, instructions,
                       cell_side=DEFAULT_CELL_SIDE, show_grid_borders=False):
    """Create a new level using a map in the maps folder"""
    h, w, walls = walls_from_map(fname)
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
        show_grid_borders=show_grid_borders
    )
