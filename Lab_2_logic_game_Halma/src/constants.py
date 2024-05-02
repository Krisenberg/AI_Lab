import os
# from enum import Enum

# TEST_CASE_DIR = os.path.join(os.pardir, 'Test_cases')
TEST_CASE_DIR = os.path.join(os.curdir, 'Test_cases')
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