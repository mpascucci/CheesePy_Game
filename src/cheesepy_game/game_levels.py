from .maze_adaptor import level_from_maze
from .victory import *
from .level import Level
from .map_tools import new_level_from_map
from .graphics import colors
from .position import Position
from .cell import Cheese, Strawberry, Cell, Exit
from .shared_functions import shuffle_and_return

levels = [
    None,
    Level(
        ROWS=3,
        COLS=6,
        cell_side=50,
        player_init_position=Position(1, 1),
        check_victory=lambda: player_has_item_id(1),
        exits=[],
        items=[Cheese(position=Position(4, 1), id=1)],
        wall_positions=[],
        instructions="Take the cheese!"
    ),
    Level(
        ROWS=3,
        COLS=6,
        cell_side=50,
        player_init_position=Position(1, 1),
        check_victory=lambda: gs.player.collected_item is not None and player_on_exit_id(1),
        exits=[Exit(position=Position(0, 1), id=1)],
        items=[Cheese(position=Position(4, 1), id=1)],
        wall_positions=[],
        instructions="Take the cheese and get back home!"
    ),
    Level(
        ROWS=6,
        COLS=4,
        cell_side=50,
        player_init_position=Position(1, 1),
        check_victory=lambda: is_item_in_exit(1, 1),
        exits=[Exit(position=Position(0, 1), id=1)],
        items=[Strawberry(position=Position(3, 5), id=1)],
        wall_positions=[],
        instructions="Take the Strawberry, go into the hole, then drop the strawberry!\n"
                     "hint: use the function Buddy.drop_item()"
    ),
    Level(
        ROWS=5,
        COLS=16,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: player_has_item_id(1),
        items=[Cheese(position=Position(14, 2), id=1)],
        wall_positions=[],
        walls_around=True,
        instructions="Who put the cheese so far from me! Go get it!\n"
                     "hint: why not use a LOOP here, to save code lines?"
    ),
    Level(
        ROWS=5,
        COLS=16,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: player_has_item_id(1),
        items=[Cheese(position=Position(14, 2), id=1)],
        wall_positions=[(9, 2)],
        walls_around=True,
        instructions="Is that a wall on my way? Let's find a walkaround to get the cheese!"
    ),
    Level(
        ROWS=5,
        COLS=16,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: player_has_item_id(1),
        items=[Cheese(position=Position(14, 2), id=1)],
        wall_positions=[(9, 2)],
        walls_around=True,
        disable_NSEW=True,
        instructions="Is this level identical to the previous? It looks like, but... wait, now you cannot use\n"
                     "the move_nort/sout/east/west functions...\n"
                     "You will have to solve it with move_forward and turn_right/left!"
    ),
    Level(
        ROWS=5,
        COLS=16,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: player_has_item_id(1),
        items=[Cheese(position=Position(14, 2), id=1)],
        wall_positions=[(4, 2), (4, 3), (9, 1), (9, 2)],
        walls_around=True,
        instructions="Nothing can take me apart from my cheese!"
    ),
    Level(
        ROWS=12,
        COLS=12,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: player_on_exit_id(1),
        exits=[Exit(position=Position(10, 10), id=1)],
        wall_positions=[],
        instructions="Let's go home!"
    ),
    new_level_from_map('stairs.ppm',
                       player_init_position=Position(1, 2),
                       check_victory=lambda: player_on_exit_id(1),
                       items=[],
                       exits=[Exit(position=Position(9, 10), id=1)],
                       instructions="Let's go back home!"
                       ),
    new_level_from_map('stairs_nested.ppm',
                       player_init_position=Position(1, 1),
                       check_victory=lambda: is_item_in_exit(1, 1),
                       items=[Cheese(Position(13, 6), id=1)],
                       exits=[Exit(position=Position(25, 9), id=1)],
                       instructions="Take the cheese in the hole!"
                       ),
    Level(
        ROWS=9,
        COLS=9,
        cell_side=50,
        player_init_position=Position(1, 7),
        check_victory=lambda: is_item_in_exit(1, 1) and is_item_in_exit(2, 2),
        items=[Cheese(Position(7, 6), id=1), Strawberry(Position(4, 3), id=2)],
        exits=[Exit(Position(1, 1), id=1, bg_color=colors.CHEESE_COLOR),
               Exit(Position(7, 1), id=2, bg_color=colors.STRAWBERRY_COLOR)],
        wall_positions=[],
        walls_around=True,
        instructions="What a mess! Bring the items in the corresponding hole."
    ),
    Level(  # 8
        ROWS=4,
        COLS=7,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: number_of_items_in_exit(1) == number_of_items_in_game(),
        items=[Cheese(Position(5, 2), id=i) for i in range(9)],
        exits=[Exit(Position(1, 1), id=1)],
        wall_positions=[],
        instructions="A lot of cheese!!! Bring it all home!"
    ),
    Level(
        ROWS=5,
        COLS=8,
        cell_side=50,
        player_init_position=Position(1, 2),
        check_victory=lambda: check_all_items_in_exit(range(3), 1) and check_all_items_in_exit(range(3, 7), 2),
        items=shuffle_and_return([Cheese(Position(5, 2), id=i) for i in range(3)] + \
                                 [Strawberry(Position(5, 2), id=i+3) for i in range(4)]),
        exits=[Exit(Position(1, 1), id=1, bg_color=colors.CHEESE_COLOR),
               Exit(Position(2, 1), id=2, bg_color=colors.STRAWBERRY_COLOR)],
        wall_positions=[],
        walls_around=True,
        instructions="The food is all mixed up, let's fix this mess."
    ),
    new_level_from_map('tunnel_monotone.ppm',
                       player_init_position=Position(1, 2),
                       check_victory=lambda: player_has_item_id(1),
                       items=[Strawberry(position=Position(22, 10), id=1)],
                       exits=[],
                       instructions="This is a long descent, let's see. I could try to go always east and if I get stuck, I might try south!\n\n\
                                    hint: try to use this while loop here:\n\
                                    while not Buddy.on_item() and not Buddy.game_over():"
                       ),
    new_level_from_map('tunnel.ppm',
                       player_init_position=Position(1, 2),
                       check_victory=lambda: player_has_item_id(1),
                       items=[Strawberry(position=Position(23, 7), id=1)],
                       exits=[],
                       instructions="Ah, now if I get stuck, must to go south, and if I get stuck again, north.\n\
                                    I think I can manage to get to the food!"
                       ),
    new_level_from_map('tunnel.ppm',
                       player_init_position=Position(1, 2),
                       check_victory=lambda: number_of_items_in_exit(1) == 2,
                       items=[Strawberry(position=Position(23, 7), id=1),
                              Cheese(position=Position(23, 6), id=2)],
                       exits=[Exit(position=Position(1, 1), id=1)],
                       instructions="Now get the food to the hole!"
                       ),
    new_level_from_map('maze.ppm',
                       player_init_position=Position(1, 1),
                       check_victory=lambda: player_has_item_id(1),
                       items=[Cheese(position=Position(4, 4), id=1)],
                       exits=[],
                       instructions="tricky path... But i'll get there!"
                       ),
    level_from_maze(4, 8, instructions='Someone told me once that there is a way to get out of a maze:\n'\
                    '"always walk forward, keeping the wall on your right", they said\n'\
                    'Let us give it a try!\n\n'\
                    'hint: https://en.wikipedia.org/wiki/Maze-solving_algorithm'),
    level_from_maze(12, 24, cell_side=25),
    # new_level_from_map('central_maze.ppm',
    #                    player_init_position=Position(29, 29),
    #                    check_victory=lambda: player_has_item_id(1),
    #                    items=[Cheese(position=Position(4, 4), id=1)],
    #                    exits=[Exit(Position(21, 37), id=1)],
    #                    instructions="tricky path... But i'll get there!"
    #                    ),
    new_level_from_map('game_over.ppm',
                       player_init_position=Position(6, 17),
                       check_victory=lambda: player_on_exit_id(1),
                       items=[Strawberry(position=Position(12, 6), id=1),
                              Cheese(position=Position(25, 16), id=2)],
                       exits=[Exit(position=Position(8, 17), id=1)],
                       cell_side=25,
                       instructions="And here we are, this is the last level.\n"\
                                    "Well done, You finished the game!"
                       ),

]
