import time
from . import config
from . import game_status as gs
from .cell import get_cell, Cell_types, Position, Collectable_item
from . import messanger
from typing import List
from .shared_functions import random_name
from .config import FRAMES_PER_SECOND


class Action_types:
    MOVE_DOWN = 0
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    END = 4


Action_names = {
    Action_types.MOVE_DOWN: "Move Downward",
    Action_types.MOVE_UP: "Move Upward",
    Action_types.MOVE_RIGHT: "Move to the right",
    Action_types.MOVE_LEFT: "Move to the left",
    Action_types.END: "End"
}


def player_has_item() -> bool:
    return gs.player.collected_item is not None


def move_player(h=0, v=0, direction_str=''):
    if gs.disable_NSEW and direction_str != 'FORWARD':
        messanger.say(
            "Movement towards North/S/E/W not allowed in this level! You can only use move_forward() and turn_left() or turn_right()")
        return

    player = gs.player
    new_xy = Position(player.pos.x + h, player.pos.y + v)
    try:
        new_cell = get_cell(new_xy)
    except IndexError as e:
        messanger.say(f"Impossible to move {direction_str}, I cannot go outside of the map.")
        return

    if new_cell.type != Cell_types.WALL:
        # move the player
        with gs.lock:
            player.pos = new_xy
        # remember what is below the player

        s = ''
        if direction_str:
            s += f'Moved {direction_str}. '
        messanger.say(s + f"New position: {player.pos}")
    else:
        messanger.say(f"Impossible to move {direction_str}, there is a wall there!")


class GameController():
    """@public Player's interface to control the mouse movement."""

    _directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # (h,v)

    def __init__(self) -> None:
        self._name: str = random_name(8)
        self._speed: int = 1  # steps per second
        self._colltected_items: List[Collectable_item] = []
        self._done: bool = False
        self._direction_i: int = 1
        self._first_action: bool = False

    @property
    def _direction(self):
        return GameController._directions[self._direction_i]

    def _move_forward(self):
        h, v = self._direction
        move_player(h=h, v=v, direction_str="FORWARD")

    def _wait(self):
        if self._speed > 0:
            if not self._first_action:
                time.sleep(1/self._speed)
            else:
                self._first_action = False
        else:
            # stop moving
            pass

    def _turn(self, i: int):
        self._direction_i = (self._direction_i+i) % 4
        s = 'ERROR'
        match i:
            case 1:
                s = "right"
            case -1:
                s = "left"
        messanger.say(f"Turned {s}.")

    def move_east(self):
        """Move the mouse EAST one step"""
        self._wait()
        # self.actions.append(Action_types.MOVE_RIGHT)
        move_player(h=1, direction_str='EAST')

    def move_forward(self):
        """Move mouse forward along its current direction."""
        self._wait()
        self._move_forward()

    def move_north(self):
        """Move the mouse Nord one step"""
        self._wait()
        move_player(v=-1, direction_str='NORTH')

    def move_south(self):
        """Move the mouse SOUTH one step"""
        self._wait()
        move_player(v=1, direction_str='SOUTH')

    def move_west(self):
        """Move the mouse WEST one step"""
        self._wait()
        move_player(h=-1, direction_str="WEST")

    def display_messages(self, on=True):
        """Set wether the mouse should display messages about its actions or not."""
        config.verbose = on

    def drop_item(self):
        """Drop the item the mouse is carrying.

        If the mouse is carrying an item, the item will be dropped on
        the cell currently occupied by the mouse."""
        cell = get_cell(gs.player.pos)
        if gs.player.collected_item is not None:
            with gs.lock:
                item = gs.player.collected_item
                cell.items.append(item)
                item.position = gs.player.pos
                gs.player.collected_item = None

    # def done(self):
    #     """Tell the game the mouse has ended the instructions.
    #     This might be  Useful to exit a loop."""
    #     self._done = True

    def game_over(self) -> bool:
        """Return True if the game is over.
        The game is over when the mouse completes the level or if the Game window gets closed.

        This function can be useful to create loops that do not end untill the level is solved:

        ```python
        while not Buddy.game_over():
            Buddy.move_forward()
        ```

        Tf you put this loop in your solution, the mouse will try to move forward untill it solves
        the level or until you close the game window.
        """
        return gs.gameover or not gs.run

    def item_carried(self) -> str:
        """Return a string describing what item the mouse is carrying now.
        If the mouse is not carrying anything, return an empty string."""
        try:
            item = gs.player.collected_item.name
        except AttributeError:
            item = ''
        return item

    def get_position(self):
        """Return the coordinates of the mouse at the current time.

        The coordinates are returned as a tuple of two integers (x,y) representing the x and y coordinate of the mouse.
        The coordinates (0,0) represent the top left tail of the maze.
        """
        return gs.player.pos.to_tuple()

    def on_item(self) -> bool:
        """Return True if the mouse is on an item (e.g cheese)"""

        return len(get_cell(gs.player.pos).items) > 0

    def on_exit(self) -> bool:
        """Return True if the mouse is on an exit (a hole)"""

        return get_cell(gs.player.pos).exit is not None

    def set_name(self, name):
        """Set the player name.
        The level passwords are generated using the player's name, if you change name the passwords will not work.
        """
        self._name = name

    def set_speed(self, speed):
        """Set the player's movement speed as movements-per-second.

        The minimum speed it 1, the maximum speed is 200.
        """
        self._speed = max(speed, 1)
        self._speed = min(speed, 200)

    def take_item(self):
        """Take the item from the cell where the player is standing.

        If there is an item on the current cell, the player will take it, otherwise nothing happens.
        """
        cell = get_cell(gs.player.pos)
        if len(cell.items) > 0:
            item = cell.items[-1]
            if not player_has_item():
                with gs.lock:
                    item = cell.items.pop()
                gs.player.collected_item = item
                messanger.say(f"Got {item.name}!")
            else:
                messanger.say(f"I cannot take the {item.name}. I am already carrying {gs.player.collected_item.name}.")
        else:
            messanger.say(f"There is nothing to take here on cell {gs.player.pos}")

    def turn_left(self):
        """Turn the direction of Buddy 90 degrees to the left"""
        self._wait()
        self._turn(-1)

    def turn_right(self):
        """Turn the direction of Buddy 90 degrees to the right"""
        self._wait()
        self._turn(1)
