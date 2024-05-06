from dataclasses import dataclass
import os
from math import floor, sqrt
import constants as const

def input_game_state(game_state_filename: str):
    file_path = os.path.join(const.TEST_CASE_DIR, game_state_filename)
    game_state = []
    with open(file_path, encoding='utf8') as input_file:
        for line in input_file.read().splitlines():
            row_tab = line.split(' ')
            game_state.append([int(x) for x in row_tab])
    return game_state


def print_board(game_state: list[list[int]]):
    print("   ", " ".join([f"{x:02}" for x in range(const.BOARD_SIZE)]))
    print("   ", "------------------------------------------------")
    for i in range(const.BOARD_SIZE):
        print(f"{i:02}", "|", "  ".join([str(game_state[i][j]) for j in range(const.BOARD_SIZE)]), "|")
    print("   ", "------------------------------------------------")


def players_pawns(
        game_state: list[list[int]],
        maximizing_player: bool    
    ):
    player = 1 if maximizing_player else 2
    pawn_positions:list[tuple[int,int]] = []
    for i in range (len(game_state)):
        for j in range (len(game_state)):
            if game_state[i][j]==player:
                pawn_positions.append((i,j))
    return pawn_positions


def floor_euclidean_distance(pawn_pos: tuple[int,int], goal: tuple[int,int]):
    return floor(sqrt((pawn_pos[0] - goal[0]) ** 2 + (pawn_pos[1] - goal[1]) ** 2))  


@dataclass(frozen=True)
class Move:
    """Dataclass representing the move

    ----------
    Attributes
    ----------
        - move_from - tuple representing current position of the pawn
        - move_to - tuple representing the next position of the pawn

        In both cases: tuple[0] is the index of the row, tuple[1] represents the column's index
    """
    move_from: tuple[int, int]
    move_to: tuple[int,int]

def make_move(game_state: list[list[int]], move: Move):
    from_row, from_col = move.move_from
    to_row, to_col = move.move_to
    players_mark = game_state[from_row][from_col]
    game_state[from_row][from_col] = 0
    game_state[to_row][to_col] = players_mark

def reverse_move(game_state: list[list[int]], move: Move):
    from_row, from_col = move.move_to
    to_row, to_col = move.move_from
    players_mark = game_state[from_row][from_col]
    game_state[from_row][from_col] = 0
    game_state[to_row][to_col] = players_mark

# if __name__ == '__main__':
#     input_game_state('initial_state.txt')