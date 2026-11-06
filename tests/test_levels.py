import pytest

from cheesepy_game import config
from cheesepy_game import game_status as gs
from cheesepy_game.cell import Cell_types, get_cell
from cheesepy_game.game_levels import levels

LEVEL_NUMBERS = [i for i, level in enumerate(levels) if level is not None]


def test_there_are_levels():
    assert len(LEVEL_NUMBERS) > 0


@pytest.mark.parametrize("number", LEVEL_NUMBERS)
def test_level_loads_and_is_playable(number):
    # loading reads the .ppm maps and images, so this also catches
    # data files missing from the installed package
    levels[number].load()

    pos = gs.player.pos
    assert pos is not None
    assert 0 <= pos.x < config.GRID_COLS
    assert 0 <= pos.y < config.GRID_ROWS
    assert get_cell(pos).type != Cell_types.WALL, "mouse starts inside a wall"


@pytest.mark.parametrize("number", LEVEL_NUMBERS)
def test_level_is_not_already_won_when_loaded(number):
    levels[number].load()
    assert not config.check_victory()