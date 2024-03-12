from .cell import Collectable_item, Exit
from typing import List
import threading
from .graphics import colors
lock = threading.Lock()

_cells = []

run = True  # the main loop (pygame) is running
gameover = False  # the game is over
editingMode = False  # the game grid is in editing mode
cheating = False  # the player cheated at leat once
move = False  # the player's solution is being run
items: List[Collectable_item] = []  # the items in this level
exits: List[Exit] = []  # the exits in this level
user_solution_ended = False  # the user solution code has finished running
disable_NSEW = True  # disable the NORTH/SOUTH/EAST/WEST movement


class player():
    pos = None
    color = colors.PLAYER_COLOR_DEFAULT
    collected_item: Collectable_item = None
