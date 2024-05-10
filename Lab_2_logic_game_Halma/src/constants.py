import os

# Check if the Test_cases directory exists
test_cases_dir = os.path.join(os.curdir, 'Test_cases')
if not os.path.exists(test_cases_dir):
    # If Test_cases directory doesn't exist, use the parent directory
    test_cases_dir = os.path.join(os.pardir, 'Test_cases')

TEST_CASE_DIR = test_cases_dir
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

EARLY_GAME_TURN_LIMIT = 30
MIDDLE_GAME_TURN_LIMIT = 85

EARLY_GAME_FORM_OBSTACLE_ESCAPE_SQUARE_SIZE = 6
EARLY_GAME_FROM_OBSTACLE_TARGET_CELL_MAX = (9,6)
EARLY_GAME_FROM_OBSTACLE_TARGET_CELL_MIN = (6,9)
EARLY_GAME_FORM_OBSTACLE_MIN_AMOUT_OF_PAWNS_OUTSIDE_DANGER_ZONE = 13

EARLY_GAME_CONQUER_CENTER_TARGET_CELL_MAX = (8,7)
EARLY_GAME_CONQUER_CENTER_TARGET_CELL_MIN = (7,8)

MIDDLE_GAME_MOVE_DIAGONAL_DIAGONAL_OFFSET = 4
MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET = 7

OBSTACLE_CELLS_MIN_PLAYER = { (5,11), (5,10), (5,9), (4,11), (4,10), (4,9) }
OBSTACLE_CELLS_MAX_PLAYER = { (10,4), (10,5), (10,6), (11,4), (11,5), (11,6) }

END_GAME_FILL_FROM_END_OUTSIDE_AREA_PENALTY = 7
END_GAME_FILL_EVERY_OTHER_PENALTY = 4

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
    (4,15) : 4,
    (2,11) : 5,
    (3,12) : 5,
    (4,13) : 5,
    (3,11) : 6,
    (4,12) : 6,
    (4,11) : 7
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
    (15,4) : 4,
    (11,2) : 5,
    (12,3) : 5,
    (13,4) : 5,
    (11,3) : 6,
    (12,4) : 6,
    (11,4) : 7
}

END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MAX_PLAYER = {
    (0,15) : 2,
    (0,14) : 0,
    (1,14) : 0,
    (1,15) : 0,
    (0,13) : 3,
    (1,13) : 3,
    (2,13) : 3,
    (2,14) : 3,
    (2,15) : 3,
    (0,12) : 1,
    (1,12) : 1,
    (2,12) : 1,
    (3,13) : 1,
    (3,14) : 1,
    (3,15) : 1,
    (0,11) : 4,
    (1,11) : 4,
    (4,14) : 4,
    (4,15) : 4
}

END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MIN_PLAYER = {
    (15,0) : 2,
    (14,0) : 0,
    (14,1) : 0,
    (15,1) : 0,
    (13,0) : 3,
    (13,1) : 3,
    (13,2) : 3,
    (14,2) : 3,
    (15,2) : 3,
    (12,0) : 1,
    (12,1) : 1,
    (12,2) : 1,
    (13,3) : 1,
    (14,3) : 1,
    (15,3) : 1,
    (11,0) : 4,
    (11,1) : 4,
    (14,4) : 4,
    (15,4) : 4
}
