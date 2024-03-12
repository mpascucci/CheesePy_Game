import hashlib
from .game_levels import levels
from .log import log


def get_level_password(player_name, level_number, length=8):
    """Return the password for a level"""
    s = f"{player_name + str(level_number)}".encode()
    return hashlib.sha1(s).hexdigest()[0:length]


def check_level_password(player_name, password):
    """Return the level corresponding to a given password"""
    cur_level = 1
    for i in range(2, len(levels)):
        log.debug(f"level {i}, true password: {get_level_password(player_name,i)}")
        if password == get_level_password(player_name, i):
            cur_level = i
            break
    return cur_level
