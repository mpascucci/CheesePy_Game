import os

# Run pygame without opening a window. Must be set before pygame is imported.
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame
import pytest

from cheesepy_game import game_status as gs


@pytest.fixture(autouse=True, scope="session")
def _pygame():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture(autouse=True)
def _reset_game_state():
    """Levels append to global lists when loaded, so start each test clean."""
    gs.items.clear()
    gs.exits.clear()
    gs.player.pos = None
    gs.player.collected_item = None
    yield