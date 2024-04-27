import copy
from random import Random
from dataclasses import dataclass
from math import inf
from halma import Halma, check_board_for_win, players_pawns, generate_valid_moves
from constants import PlayerStrategy


# def minmax(game: Halma):
#     """ Function to evaluate provided game state.
#         Function returns a value from range [0,100], where:
#             0 -> player 1 has won
#             100 -> player 2 has won
#         Hence player 1 wants to minimize this value and player 2 wants to maximize it
#     """
#     players_strategy = game.player_turn
#     is_game_start = game.turn_number == 1
#     random = Random()

#     @dataclass
#     class GameState:
#         game_state: list[list[int]]

#         def __hash__(self):
#             return hash(tuple(tuple(row) for row in self.game_state))

#         def __eq__(self, other):
#             return isinstance(other, GameState) and self.game_state == other.game_state

#     def minmax_rec(game_state: list[list[int]], depth: int, strategy: PlayerStrategy):
#         win_check = check_board_for_win(game_state)
#         if not is_game_start and win_check != 0:
#             return game_state, (win_check - 1) * 100
#         if depth == game.minmax_depth:
#             return game_state, random.randint(1,99)
#             # pass # return heuristic function value

#         pawns = players_pawns(game_state, strategy.value)
#         next_valid_game_states = {}
#         for pawn in pawns:
#             next_valid_moves = generate_valid_moves(game_state, pawn)
#             for move in next_valid_moves:
#                 if pawn != move:
#                     new_game_state = copy.deepcopy(game_state)
#                     new_game_state[pawn[0]][pawn[1]] = 0
#                     new_game_state[move[0]][move[1]] = strategy.value
#                     next_valid_game_states[GameState(new_game_state)] = -inf
        
#         for key in next_valid_game_states.keys():
#             next_valid_game_states[key] = minmax_rec(key.game_state, depth + 1)[1]
        
#         best_game_state = None
#         best_evaluation = inf if strategy == PlayerStrategy.MIN else -inf

#         for next_game_state, eval in next_valid_game_states.items():
#             if ((strategy == PlayerStrategy.MIN and eval < best_evaluation)
#                 or (strategy == PlayerStrategy.MAX and eval > best_evaluation)) :
#                 best_game_state = next_game_state
#                 best_evaluation = eval
#         return best_game_state.game_state, best_evaluation

#     best_game_state, best_eval = minmax_rec(game.game_state, 1)
#     game.game_state = best_game_state
#     game.player_turn = PlayerStrategy.MAX if players_strategy == PlayerStrategy.MIN else PlayerStrategy.MIN
#     game.turn_number += 1
#     return best_game_state, best_eval

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

def mockup_heuristic(game_state: list[list[int]], maximizing_player: bool) -> float:
    goal_cell = (0,15) if maximizing_player else (15,0)
    pawns = players_pawns(game_state, maximizing_player)
    dist_sum = 0
    for pawn in pawns:
        dist_sum += abs(pawn[0] - goal_cell[0]) + abs(pawn[1] - goal_cell[1])
    if maximizing_player:
        return (1.0 - ((dist_sum - 60)/ 450)) * 100.0
    else:
        return ((dist_sum - 60)/ 450) * 100.0
    

def minimax(game: Halma):

    # random = Random()

    def minimax_rec(game_state: list[list[int]], depth_left: int, maximizing_player: bool, alpha: float, beta: float):
        win_check = check_board_for_win(game_state)
        if win_check != 0:
            if maximizing_player:
                return None, 100.0
            return None, 0.0
        if depth_left == 0:
            return None, mockup_heuristic(game_state, maximizing_player)
            # pass # return heuristic function value

        pawns = players_pawns(game_state, maximizing_player)
        children = set()
        for current_pos in pawns:
            next_valid_moves = generate_valid_moves(game_state, current_pos)
            for next_pos in next_valid_moves:
                if current_pos != next_pos:
                    children.add(Move(move_from=current_pos, move_to=next_pos))
        
        best_move = None
        best_evaluation = -inf if maximizing_player else inf
        prune_flag = False
        if maximizing_player:
            for move in (move for move in children if not prune_flag):
                make_move(game_state, move)
                _, eval = minimax_rec(game_state, depth_left - 1, False, alpha, beta)
                reverse_move(game_state, move)
                if eval > best_evaluation:
                    best_move = move
                    best_evaluation = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    prune_flag = True
        else:
            for move in (move for move in children if not prune_flag):
                make_move(game_state, move)
                _, eval = minimax_rec(game_state, depth_left - 1, True, alpha, beta)
                reverse_move(game_state, move)
                if eval < best_evaluation:
                    best_move = move
                    best_evaluation = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    prune_flag = True

        return best_move, best_evaluation

    best_move, best_eval = minimax_rec(game.game_state, game.minmax_depth, game.maximizing_player, -inf, inf)
    make_move(game.game_state, best_move)
    game.maximizing_player = not game.maximizing_player
    game.turn_number += 1
    return best_eval

# In order to optimze the minmax performance I use alpha-beta pruning combined with remembering 
    # ! TO-DO:
    #   1. take all the player's pawns
    #   2. generate next valid moves for each pawn
    #   3. create a dictionary 'children' where the key is the next valid game_state
    #       and the value is initially -1
    #   4. recursively evaluate each child using minmax function
    #   5. select min or max value out of all values based on the player's perspective

