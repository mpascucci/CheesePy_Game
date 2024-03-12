
from time import sleep
import numpy as np
import threading

if True:
    # keep imports in this order
    from os import environ
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame as pg
    from . import config
    from . import game_status as gs

from .shared_functions import *
from .game_controller import GameController, move_player
from .position import Position
from .game_levels import levels
from .password import get_level_password, check_level_password
from .graphics import colors, fonts
from .map_tools import save_map_to_image
from .graphics import icons
from .exceptions import Cheese_ValueError
from . import messanger
from .cell import *  # import this at the end

import logging
log = logging.getLogger(__name__)
logging.basicConfig()


Buddy = GameController()


def is_point_in_cell(cell, x, y):
    l = config.cell_side
    cx = cell.position.x*l
    cy = cell.position.y*l
    return y > cx and y < cx+l and x > cy and x < cy+l


def draw_grid():
    """Draw a grid on the screen"""
    r_step = config.screen.get_height() // config.GRID_ROWS
    c_step = config.screen.get_width() // config.GRID_COLS

    for r in range(0, config.GRID_ROWS):
        for c in range(0, config.GRID_COLS):
            pos = Position(c, r)
            cur_cell = get_cell(pos)

            # BACKGROUND COLOR
            color = None
            if cur_cell.type == Cell_types.WALL:
                color = colors.WALL_COLOR
            elif player_on_cell(cur_cell):
                color = gs.player.color
            elif cur_cell.is_exit():
                color = cur_cell.exit.bg_color
            elif cur_cell.has_items():
                color = cur_cell.items[-1].bg_color
            elif cur_cell.type == Cell_types.FLOOR:
                color = colors.FLOOR_COLOR
            else:
                raise Cheese_ValueError("Cell background color not defined")

            image = None
            # IMAGE
            if player_on_cell(cur_cell):
                image = icons.mouse
            elif cur_cell.has_items():
                image = cur_cell.items[-1].image
            elif cur_cell.is_exit():
                image = cur_cell.exit.image
            elif cur_cell.type == Cell_types.WALL:
                image = icons.wall
            elif cur_cell.type is not None:
                pass
            else:
                raise Cheese_ValueError("Cell image not inferentiable")

            # the cell rectangular surface
            rect = pg.Rect(c * c_step, r * r_step, c_step, r_step)
            # fill the surface
            config.screen.fill(color, rect)
            # draw the borders
            if config.show_grid_borders:
                pg.draw.rect(config.screen, (50, 50, 50), rect, width=1)
            # set the image
            if image:
                image = pg.transform.scale_by(image, config.cell_side/config.DEFAULT_CELL_SIDE)
                config.screen.blit(image, rect)

            # carried objects
            if player_on_cell(cur_cell) and (gs.player.collected_item is not None):
                # player is on this cell and is carrying an item
                image = gs.player.collected_item.image
                image = pg.transform.scale_by(image, 0.5)
                config.screen.blit(image, rect)

            # display items number
            if len(cur_cell.items) > 1:
                text = fonts.cell_font.render(str(len(cur_cell.items)), True, colors.NUMBERS_COLOR)
                rect.width //= 2
                rect.height //= 2
                rect.right += config.cell_side//2
                config.screen.fill(colors.NUMBERS_BKGROUND_COLOR, rect)
                # alpha is TOO complicated
                text_rect = text.get_rect(center=rect.center)
                config.screen.blit(text, text_rect)

    # display Buddy's direction
    player_pos = gs.player.pos

    center = Position(0, 0)
    center.x = player_pos.x * c_step + c_step//2
    center.y = player_pos.y * r_step + r_step//2

    center.x += Buddy._direction[0]*(r_step//2)
    center.y += Buddy._direction[1]*(c_step//2)

    pg.draw.circle(config.screen, pg.Color("white"), center.to_tuple(), r_step//8)


def save_maps_to_np(fname):
    # save walls as matrix
    v = np.zeros(
        (config.GRID_ROWS, config.GRID_COLS), dtype=np.int8
    )
    for r, row in enumerate(gs._cells):
        for c, cell in enumerate(row):
            v[r, c] = cell.type == Cell_types.WALL
    np.savetxt(fname, v, fmt="%i", delimiter=",")
    print(v)


def user_thread_target(solution_callback):
    while (not gs.move) and gs.run and not gs.gameover:
        # the user solution is not started yet and the main loop is running
        sleep(0.1)

    if gs.run:
        if not gs.cheating:
            print()
            print(f"Your solution started.")
            print("------------------------")
            solution_callback()
        gs.user_solution_ended = True


def ctlr_key_pressed():
    return pg.key.get_mods() & pg.KMOD_CTRL


def handle_events():
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONUP and gs.editingMode:
            # click in editing mode
            x, y = pg.mouse.get_pos()
            for r in gs._cells:
                for c in r:
                    if is_point_in_cell(c, y, x):
                        if c.type == Cell_types.FLOOR:
                            c.type = Cell_types.WALL
                        elif c.type == Cell_types.WALL:
                            c.type = Cell_types.FLOOR
        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            # SPACE BAR
            gs.move = True
        elif event.type == pg.KEYDOWN:
            # OTHER KEYS
            gs.cheating = True
            log.debug(f"keypress: {event.key}")
            match event.key:
                case pg.K_LEFT:
                    move_player(h=-1)
                case pg.K_RIGHT:
                    move_player(h=1)
                case pg.K_UP:
                    move_player(v=-1)
                case pg.K_DOWN:
                    move_player(v=1)
                case pg.K_g:
                    Buddy.take_item()
                case pg.K_d:
                    Buddy.drop_item()
                case pg.K_r:
                    Buddy._turn(1)
                case pg.K_l:
                    Buddy._turn(-1)
                case pg.K_f:
                    Buddy._move_forward()
                case pg.K_e:
                    if ctlr_key_pressed():
                        # enable wall editing
                        gs.editingMode = not gs.editingMode
                        messanger.say(f'Editing mode: {"ON" if gs.editingMode else "OFF"}')
                case pg.K_s:
                    if ctlr_key_pressed():
                        fname = "./map.ppm"
                        save_map_to_image(fname)
                        messanger.say(f"Matrix saved in {fname}")
                case pg.K_q:
                    gs.run = False
                case _:
                    pass
        elif event.type == pg.QUIT:
            gs.run = False


def clear_terminal():
    # from https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
    print("\033[H\033[J", end="")


def victory_end(cur_level):
    print("------------------------")
    print("GAME OVER")
    print(f"Congrats {Buddy._name}, You solved level {cur_level}!")
    print(f"Your password for level {cur_level+1} is {get_level_password(Buddy._name, cur_level+1)}")
    print("(press Q to quit.)")
    gs.player.color = pg.Color("green")


def check_victory(cur_level, user_thread):
    victory = config.check_victory()
    if not gs.gameover:
        # check victory
        if gs.user_solution_ended:
            gs.gameover = True
            if not victory:
                print("You lost Try again...")
                gs.player.color = pg.Color("red")
            else:
                victory_end(cur_level)
        else:
            if victory:
                # vicrory, but player solution still running
                gs.gameover = True
                if gs.cheating:
                    gs.player.color = pg.Color("green")
                    print("OK, This is what you need to do to pass this level. Now try with code only!")
                else:
                    victory_end(cur_level)


def start_game(solution=None, password=None):
    """Start one level of CheesePy.

    Parameters:
    - `solution` : a user defined function with the instructions to solve the current level
    - `password` : a string to access the corresponding level.

    When you complete one level, you will get a password to access the following.
    Notice that the password is linked to your Mouse's name, so if you change your name, the password will change too.
    """

    if solution is None:
        def solution(): return None

    user_thread = threading.Thread(target=user_thread_target, args=[solution])
    user_thread.start()

    cur_level = check_level_password(Buddy._name, password)

    pg.display.set_caption(f"Cheese Py - level {cur_level}")
    levels[cur_level].load()

    pg.key.set_repeat()  # disable repeat keydown when holding keys

    clear_terminal()
    print(f"Game started! You are playing level {cur_level}. Good luck, {Buddy._name}!")
    print()
    print(levels[cur_level].instructions)

    while gs.run:
        sleep(1 / config.FRAMES_PER_SECOND)  # frame
        handle_events()

        with gs.lock:
            check_victory(cur_level, user_thread)
            draw_grid()

        pg.display.update()

    user_thread.join()
    pg.quit()
