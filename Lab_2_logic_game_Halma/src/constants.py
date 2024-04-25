import os
from enum import Enum

# TEST_CASE_DIR = os.path.join(os.pardir, 'Test_cases')
TEST_CASE_DIR = os.path.join(os.curdir, 'Test_cases')
BOARD_SIZE = 16

class PlayerStrategy(Enum):
    """ Enum representing player's strategy

    Options
    -------
    MIN = 1
        means player 1
    MAX = 2
        means player 2
    """
    MIN = 1
    MAX = 2