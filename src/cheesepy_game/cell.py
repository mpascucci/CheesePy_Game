from .position import Position
from .graphics import icons, colors
from typing import List
from dataclasses import dataclass
from . import game_status as gs


class Cell_types():
    """represents one case of the game's chessboard"""
    FLOOR = 0
    WALL = 1


class Cell():
    def __init__(self, position_xy) -> None:
        self.position = position_xy
        self.color = None  # None for default
        self.items: List[Collectable_item] = []  # a list of Collectable_items
        self.exit: Exit = None
        self.type: Cell_types = Cell_types.FLOOR

    def __str__(self):
        return f"Cell {self.position}"

    def has_items(self):
        return len(self.items) > 0

    # def hosts_player(self):
    #     return self.position == gs.player.pos

    def is_exit(self):
        return self.exit is not None

    def is_blocking(self):
        return self.type in [Cell_types.WALL]


class Collectable_item():
    def __init__(self, position: Position, name: str, image, bg_color=None):
        self.name = name
        self.image = image
        self.bg_color = bg_color
        self.position = position

    def __str__(self) -> str:
        return self.name


class Cheese(Collectable_item):
    def __init__(self, position, id: int = None):
        self.id = id
        super().__init__(position=position, name='cheese', image=icons.cheese, bg_color=colors.CHEESE_COLOR)


class Strawberry(Collectable_item):
    def __init__(self, position, id=None):
        self.id = id
        super().__init__(position=position, name='strawberry', image=icons.strawberry, bg_color=colors.STRAWBERRY_COLOR)


@dataclass
class Exit():
    position: Position
    image: object = icons.hole
    id: int = None
    bg_color: object = colors.FLOOR_COLOR


def get_cell(position: Position) -> Cell:
    c = position.x
    r = position.y
    if c < 0 or r < 0:
        raise IndexError()
    return gs._cells[r][c]


def set_cell(position, cell):
    c = position.x
    r = position.y
    if c < 0 or r < 0:
        raise IndexError()
    gs._cells[r][c] = cell


def FLOOR_cell(cell):
    """Overwrite the cell with a new FLOOR one in the same position"""
    set_cell(cell.position, Cell(cell.position))


def set_cell_type(position, cell_type):
    get_cell(position).type = cell_type


def set_cell_color(position, color):
    get_cell(position).color = color


def get_cell_type(position):
    return get_cell(position).type


def edit_cell(position, new_type=None, new_color=None):
    cell = get_cell(position)
    if new_color is not None:
        cell.color = new_color
    if new_type is not None:
        cell.type = new_type


def player_on_cell(cell: Cell) -> bool:
    """Return true if the player is on the cell"""
    return gs.player.pos == cell.position


def is_cell_FLOOR(pos_xy):
    return get_cell_type(pos_xy) == Cell_types.FLOOR


def get_exit_by_id(exit_id: int) -> Exit:
    """Return the Exit object corresponding to the specified ID.
    An Exit witht the given ID must exist in the level."""
    return next(filter(lambda e: e.id == exit_id, gs.exits))


def get_item_by_id(id: int) -> Collectable_item:
    """Return the Item object corresponding to the specified ID.
    An Item with the given ID must exist in the level."""
    return next(filter(lambda i: i.id == id, gs.items))
