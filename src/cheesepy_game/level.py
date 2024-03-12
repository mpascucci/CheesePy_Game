from dataclasses import dataclass, field
from .position import Position
from typing import List
from .cell import Exit, Collectable_item, Cell, Cell_types, set_cell_type, get_cell
from . import config
from . import game_status as gs
from .config import DEFAULT_CELL_SIDE
import pygame


@dataclass
class Level():
    """One level of the game"""
    ROWS: int
    COLS: int
    player_init_position: Position  # set after initializing the cells
    wall_positions: list
    check_victory: object
    cell_side: int = DEFAULT_CELL_SIDE
    grid_lines_thickness: int = 1
    show_grid_borders: bool = True
    exits: List[Exit] = field(default_factory=list)
    items: List[Collectable_item] = field(default_factory=list)
    instructions: str = ''
    walls_around: bool = False
    disable_NSEW: bool = False  # disable N/S/E/W movements

    def _load_into_config(self):
        config.SCREEN_HEIGHT = self.ROWS * self.cell_side
        config.SCREEN_WIDTH = self.COLS * self.cell_side
        config.cell_side = self.cell_side
        config.GRID_ROWS = self.ROWS
        config.GRID_COLS = self.COLS

        config.screen = pygame.display.set_mode((
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        gs._cells = [[Cell(Position(c, r)) for c in range(config.GRID_COLS)]
                     for r in range(config.GRID_ROWS)]
        config.check_victory = self.check_victory
        config.grid_lines_thickness = self.grid_lines_thickness
        config.show_grid_borders = self.show_grid_borders
        gs.disable_NSEW = self.disable_NSEW

    def _setup_cells(self):

        if self.walls_around:
            for r, row in enumerate(gs._cells):
                for c, cell in enumerate(row):
                    if r == 0 or r == len(gs._cells)-1 or c == 0 or c == len(row)-1:
                        # this cell is on the border of the map
                        cell.type = Cell_types.WALL

        for t in self.wall_positions:
            pos = Position(t[0], t[1])
            set_cell_type(pos, Cell_types.WALL)

        for e in self.exits:
            cell = get_cell(e.position)
            cell.exit = e
            gs.exits.append(e)

        for item in self.items:
            cell = get_cell(item.position)
            cell.items.append(item)
            gs.items.append(item)

    def _setup_player(self):
        # run this after initializin of the matrix of cells
        gs.player.pos = self.player_init_position

    def load(self):
        self._load_into_config()
        self._setup_cells()
        self._setup_player()
