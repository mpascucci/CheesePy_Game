import pytest

from cheesepy_game import config
from cheesepy_game import game_status as gs
from cheesepy_game.cell import Cell_types, get_cell
from cheesepy_game.game_controller import GameController
from cheesepy_game.game_levels import levels


@pytest.mark.parametrize("requested, expected", [
    (50, 50),
    (1, 1),
    (200, 200),
    (0, 1),
    (-5, 1),
    (1000, 200),
])
def test_set_speed_is_clamped(requested, expected):
    buddy = GameController()
    buddy.set_speed(requested)
    assert buddy._speed == expected


def test_set_name():
    buddy = GameController()
    buddy.set_name("Sarah")
    assert buddy._name == "Sarah"


def test_turning_cycles_through_four_directions():
    buddy = GameController()
    buddy.set_speed(200)
    start = buddy._direction_i
    for _ in range(4):
        buddy.turn_right()
    assert buddy._direction_i == start


def test_level_1_can_be_solved():
    config.verbose = False
    levels[1].load()
    buddy = GameController()
    buddy.set_speed(200)

    assert not config.check_victory()
    for _ in range(3):
        buddy.move_east()
    buddy.take_item()

    assert buddy.item_carried() == "cheese"
    assert config.check_victory()


def test_player_cannot_walk_through_a_wall():
    config.verbose = False
    levels[5].load()  # has a wall at (9, 2) between the mouse and the cheese
    buddy = GameController()
    buddy.set_speed(200)

    for _ in range(20):
        buddy.move_east()

    assert get_cell(gs.player.pos).type != Cell_types.WALL
    assert gs.player.pos.x < 9