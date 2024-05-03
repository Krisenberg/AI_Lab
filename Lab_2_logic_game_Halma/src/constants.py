import os
# from enum import Enum

# TEST_CASE_DIR = os.path.join(os.pardir, 'Test_cases')
TEST_CASE_DIR = os.path.join(os.pardir, 'Test_cases')
BOARD_SIZE = 16
MAX_PAWN_DIST_SUM = 352
MIN_PAWN_DIST_SUM = 47

MAXIMIZING_PLAYER_CAMP = {
    (15,0), (15,1), (15,2), (15,3), (15,4),
    (14,0), (14,1), (14,2), (14,3), (14,4),
    (13,0), (13,1), (13,2), (13,3),
    (12,0), (12,1), (12,2),
    (11,0), (11,1)
}

MINIMIZING_PLAYER_CAMP = {
    (0,15), (0,14), (0,13), (0,12), (0,11),
    (1,15), (1,14), (1,13), (1,12), (1,11),
    (2,15), (2,14), (2,13), (2,12),
    (3,15), (3,14), (3,13),
    (4,15), (4,14)
}

MAXIMIZING_PLAYER_MARK = 1
MINIMIZING_PLAYER_MARK = 2

EARLY_GAME_TURN_LIMIT = 15
MIDDLE_GAME_TURN_LIMIT = 30
# END_GAME_TURN_LIMIT = 15

EARLY_GAME_FORM_OBSTACLE_PENALTY_SQUARE_SIZE = 4
MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET = 6

END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MAX_PLAYER = {
    (0,15) : 0,
    (0,14) : 1,
    (1,14) : 1,
    (1,15) : 1,
    (0,13) : 2,
    (1,13) : 2,
    (2,13) : 2,
    (2,14) : 2,
    (2,15) : 2,
    (0,12) : 3,
    (1,12) : 3,
    (2,12) : 3,
    (3,13) : 3,
    (3,14) : 3,
    (3,15) : 3,
    (0,11) : 4,
    (1,11) : 4,
    (4,14) : 4,
    (4,15) : 4
}

END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MIN_PLAYER = {
    (15,0) : 0,
    (14,0) : 1,
    (14,1) : 1,
    (15,1) : 1,
    (13,0) : 2,
    (13,1) : 2,
    (13,2) : 2,
    (14,2) : 2,
    (15,2) : 2,
    (12,0) : 3,
    (12,1) : 3,
    (12,2) : 3,
    (13,3) : 3,
    (14,3) : 3,
    (15,3) : 3,
    (11,0) : 4,
    (11,1) : 4,
    (14,4) : 4,
    (15,4) : 4
}

# class PlayerStrategy(Enum):
#     """ Enum representing player's strategy

#     Options
#     -------
#     MIN = 1
#         means player 1
#     MAX = 2
#         means player 2
#     """
#     MIN = 1
#     MAX = 2