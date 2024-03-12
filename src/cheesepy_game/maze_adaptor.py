import re
from typing import List
from .config import DEFAULT_CELL_SIDE
from labyrinth import maze, grid
import numpy as np
from .position import Position
from .cell import Exit
from .victory import player_on_exit_id
from .level import Level


def maze_to_matrix(maze, cell_dimension=1) -> str:
    """Return a string representation of the maze."""
    cell_width = cell_dimension
    cell_heigth = cell_width
    maze_str = '+' + ((('-' * cell_width) + '+') * maze.width) + '\n'
    for row in range(maze.height):
        for _ in range(cell_heigth):
            maze_str += '|'
            for column in range(maze.width):
                cell = maze[row, column]
                maze_str += ' ' * cell_width
                maze_str += ' ' if grid.Direction.E in cell.open_walls else '|'
            maze_str += '\n'
        maze_str += '+'
        for column in range(maze.width):
            maze_str += (' ' if grid.Direction.S in maze[row, column].open_walls else '-') * cell_width
            maze_str += '+'
        maze_str += '\n'
    maze_str = re.sub(' ', '0', maze_str)
    maze_str = re.sub('[^\d\n]', '1', maze_str).replace('\n', '')
    return np.array([int(c) for c in maze_str]).reshape((maze.height*(cell_heigth+1)+1, maze.width*(cell_width+1)+1))


def maze_walls(m) -> List[tuple]:
    a = maze_to_matrix(m)
    a = np.vstack(a.nonzero()).transpose().tolist()
    return a


def level_from_maze(h: int, w: int, instructions="A-MAZE-ING!", cell_side=DEFAULT_CELL_SIDE) -> Level:
    m = maze.Maze(h, w)
    rows = m.width*2+1
    cols = m.height*2+1
    return Level(
        ROWS=rows, COLS=cols,
        player_init_position=Position(*m.start_cell.coordinates).add_scalar(1),
        wall_positions=maze_walls(m),
        check_victory=lambda: player_on_exit_id(1),
        exits=[Exit(position=Position(*m.end_cell.coordinates).times(2).add_scalar(1), id=1)],
        items=[],
        cell_side=cell_side,
        instructions=instructions
    )
