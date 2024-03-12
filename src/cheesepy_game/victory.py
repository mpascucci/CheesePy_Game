from .position import Position
from .cell import Cell,  get_cell, get_item_by_id, get_exit_by_id
from typing import List
from . import game_status as gs


def player_has_item_id(id) -> bool:
    "Check if the player is carrying the object with the given ID"
    item = gs.player.collected_item
    return (item is not None) and (item.id == id)


def cell_has_items(cell: Cell) -> bool:
    "Check if the given cell has any items"
    return len(cell.items) > 0


def is_item_at_position(item_id: int, position: Position) -> bool:
    """Check if the item with the given ID is in the cell at the given position
    An item with given ID must exists in the level"""
    item = get_item_by_id(id)
    return item.pos == position


def is_item_in_exit(item_id: int, exit_id: int) -> bool:
    """Check if an item is in an exit.
    An item with given ID must exists in the level"""
    item = get_item_by_id(item_id)
    exit = get_exit_by_id(exit_id)
    return item.position == exit.position


def check_all_items_in_exit(item_ids: List[int], exit_id: int) -> bool:
    """Return true if all the listed items are in the specified exit."""
    def f(item_id): return is_item_in_exit(item_id, exit_id)
    return all(map(f, item_ids))


def player_on_exit_id(exit_id: int) -> bool:
    """Check if the player is on the exit with the specified ID."""
    cell = get_cell(gs.player.pos)
    return cell.is_exit() and cell.exit.id == exit_id


def number_of_items_in_exit(exit_id: int) -> int:
    """Get the number of items in the specified exit."""
    pos = get_exit_by_id(exit_id).position
    cell = get_cell(pos)
    return len(cell.items)


def number_of_items_in_game():
    """Get the number of items defined in this level."""
    return len(gs.items)
