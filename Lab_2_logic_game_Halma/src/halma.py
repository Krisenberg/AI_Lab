import constants as const
from dataclasses import dataclass
from strategy import GameStrategy

class Halma:
    def __init__(self, game_state, max_depth, max_player_strategy, min_player_strategy):
        self.game_state: list[list[int]] = game_state
        self.minmax_depth: int = max_depth
        self.max_player_strategy: GameStrategy = max_player_strategy
        self.min_player_strategy: GameStrategy = min_player_strategy
        self.maximizing_player: bool = True
        self.board_size: int = const.BOARD_SIZE
        self.turn_number: int = 1
        self.move_number: int = 1
        self.max_player_visited_nodes: dict[int,int] = {}
        self.min_player_visited_nodes: dict[int,int] = {}
        self.max_player_move_time: dict[int,int] = {}
        self.min_player_move_time: dict[int,int] = {}


    # def __init__(self, game_state: list[list[int]], minmax_depth: int, player_who_starts: int = 1):
    #     self.game_state = game_state
    #     self.minmax_depth = minmax_depth
    #     self.player_turn = player_who_starts
    #     self.board_size = const.BOARD_SIZE
    #     self.turn_number = 1


def generate_step_moves(
        game_state: list[list[int]],
        pawn_pos: tuple[int,int]
    ):
    """Function to generate valid step moves for the pawn. Step move is a move
    onto the neighbour cell without jumping, for example: (3,4) -> (3,5).
    """
    step_moves = []
    i_offsets = [-1, 0, 1]
    j_offsets = [-1, 0, 1]
    for i in i_offsets:
        for j in j_offsets:
            if (pawn_pos[0] + i in range (len(game_state))
                and pawn_pos[1] + j in range (len(game_state))
                and game_state[pawn_pos[0] + i][pawn_pos[1] + j] == 0):
                step_moves.append((pawn_pos[0] + i, pawn_pos[1] + j))
    return step_moves


def generate_possible_jumps(
        game_state: list[list[int]],
        pawn_pos: tuple[int, int]
    ):
    """
        Function to generate possible jumps for the pawn from a certain position.
        It checks all 8 directions - if the first cell in that direction is empty
        and the second one is free, then this second cell as the ending (landing)
        one is considered a valid jump opportunity.
    """
    jump_moves = []
    i_offsets = [-1, 0, 1]
    j_offsets = [-1, 0, 1]
    for i in i_offsets:
        for j in j_offsets:
            cond_1 = pawn_pos[0] + i in range (len(game_state))
            cond_2 = pawn_pos[1] + j in range (len(game_state))
            cond_3 = pawn_pos[0] + (2 * i) in range (len(game_state))
            cond_4 = pawn_pos[1] + (2 * j) in range (len(game_state))
            if (cond_1 and cond_2 and cond_3 and cond_4
                and game_state[pawn_pos[0] + i][pawn_pos[1] + j] != 0
                and game_state[pawn_pos[0] + (2 * i)][pawn_pos[1] + (2 * j)] == 0):
                    jump_moves.append((pawn_pos[0] + (2 * i), pawn_pos[1] + (2 * j)))
    return jump_moves


def generate_jump_moves(
        game_state: list[list[int]],
        pawn_pos: tuple[int,int],
        tabu_pos: set[tuple[int,int]]
    ):
    """
        This function takes all possible jumps from a specific position and recursively
        checks if it's possible to continue such a jump (to perform multi-jump). It returns
        all positions of the cells that are achievable by jumping from the original pawn position.
    """
    possible_jumps = generate_possible_jumps(game_state, pawn_pos)
    
    moves = []
    tabu_pos.add(pawn_pos)
    for jump_pos in possible_jumps:
        if jump_pos not in tabu_pos:
            moves += [jump_pos] + generate_jump_moves(game_state, jump_pos, tabu_pos)
    return moves


def generate_valid_moves(
        game_state: list[list[int]],
        pawn_pos: tuple[int,int]
    ):
    step_moves = generate_step_moves(game_state, pawn_pos)
    jump_moves = generate_jump_moves(game_state, pawn_pos, tabu_pos=set())
    return step_moves + jump_moves


def check_corner_for_win(game_state: list[list[int]], bottom_corner: bool):
    corner_cells_offsets = {
        0 : [0, 1, 2, 3, 4],
        1 : [0, 1, 2, 3, 4],
        2 : [0, 1, 2, 3],
        3 : [0, 1, 2],
        4 : [0, 1],
    }
    base_cell = (15,0) if bottom_corner else [0,15]
    cell_mark = game_state[base_cell[0]][base_cell[1]]
    for row_offset, col_offsets in corner_cells_offsets.items():
        for col_offset in col_offsets:
            if bottom_corner:
                nex_cell_i = base_cell[0] - row_offset
                nex_cell_j = base_cell[1] + col_offset
            else:
                nex_cell_i = base_cell[0] + row_offset
                nex_cell_j = base_cell[1] - col_offset
            if game_state[nex_cell_i][nex_cell_j] != cell_mark:
                return 0
    return cell_mark


def check_board_for_win(game_state: list[list[int]]) -> int:
    bottom_corner_check = check_corner_for_win(game_state, True)
    top_corner_check = check_corner_for_win(game_state, False)
    if bottom_corner_check == 2:
        return 2
    if top_corner_check == 1:
        return 1
    return 0
    # if bottom_corner_check == 0 and top_corner_check == 0:
    #     return 0
    # if bottom_corner_check != 0:
    #     return bottom_corner_check
    # return top_corner_check


# if __name__=='__main__':
#     print('Game state:')
#     line = input().split(' ')
#     print(line)
#     print(type(line))