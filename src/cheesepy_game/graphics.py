import pygame
from importlib.resources import files
from . import config
from pygame import Color


def load_image(fname):
    path = files('cheesepy_game.images').joinpath(fname)
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (config.cell_side, config.cell_side))
    return image


class icons():
    mouse = load_image("mouse.png")
    cheese = load_image("cheese.png")
    strawberry = load_image("strawberry.png")
    hole = load_image("hole.png")
    wall = load_image("wall.png")


if __name__ == "__main__":
    print(load_image("mouse.png"))


class colors():
    WALL_COLOR = Color(210, 47, 39)
    FLOOR_COLOR = Color("black")
    PLAYER_COLOR_DEFAULT = Color("white")
    CHEESE_COLOR = Color("yellow")
    STRAWBERRY_COLOR = Color("pink")
    NUMBERS_COLOR = Color("blue")
    NUMBERS_BKGROUND_COLOR = Color(255, 255, 255, 50)


pygame.init()


class fonts():
    cell_font = pygame.font.SysFont(None, round(config.cell_side*0.66))
