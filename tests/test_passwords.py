from cheesepy_game.game_levels import levels
from cheesepy_game.password import check_level_password, get_level_password


def test_password_is_deterministic():
    assert get_level_password("Sarah", 3) == get_level_password("Sarah", 3)


def test_password_depends_on_name_and_level():
    assert get_level_password("Sarah", 3) != get_level_password("Sarah", 4)
    assert get_level_password("Sarah", 3) != get_level_password("Marco", 3)


def test_password_length():
    assert len(get_level_password("Sarah", 3)) == 8
    assert len(get_level_password("Sarah", 3, length=12)) == 12


def test_every_level_password_maps_back_to_its_level():
    # a broken mapping would lock players out of their saved progress
    for level in range(2, len(levels)):
        password = get_level_password("Sarah", level)
        assert check_level_password("Sarah", password) == level


def test_unknown_password_falls_back_to_level_1():
    assert check_level_password("Sarah", "not-a-password") == 1


def test_password_for_another_name_does_not_work():
    password = get_level_password("Sarah", 5)
    assert check_level_password("Marco", password) != 5