import copy
from random import Random
from dataclasses import dataclass
from math import inf
from halma import Halma, check_board_for_win, players_pawns, generate_valid_moves
from constants import PlayerStrategy


def minmax(game: Halma):
    """ Function to evaluate provided game state.
        Function returns a value from range [0,100], where:
            0 -> player 1 has won
            100 -> player 2 has won
        Hence player 1 wants to minimize this value and player 2 wants to maximize it
    """
    players_strategy = game.player_turn
    is_game_start = game.turn_number == 1
    random = Random()

    @dataclass
    class GameState:
        game_state: list[list[int]]

        def __hash__(self):
            return hash(tuple(tuple(row) for row in self.game_state))

        def __eq__(self, other):
            return isinstance(other, GameState) and self.game_state == other.game_state

    def minmax_rec(game_state: list[list[int]], depth: int):
        win_check = check_board_for_win(game_state)
        if not is_game_start and win_check != 0:
            return game_state, (win_check - 1) * 100
        if depth == game.minmax_depth:
            return game_state, random.randint(1,99)
            # pass # return heuristic function value

        pawns = players_pawns(game_state, players_strategy.value)
        next_valid_game_states = {}
        for pawn in pawns:
            next_valid_moves = generate_valid_moves(game_state, pawn)
            for move in next_valid_moves:
                if pawn != move:
                    new_game_state = copy.deepcopy(game_state)
                    new_game_state[pawn[0]][pawn[1]] = 0
                    new_game_state[move[0]][move[1]] = players_strategy.value
                    next_valid_game_states[GameState(new_game_state)] = -inf
        
        for key in next_valid_game_states.keys():
            next_valid_game_states[key] = minmax_rec(key.game_state, depth + 1)[1]
        
        best_game_state = None
        best_evaluation = inf if players_strategy == PlayerStrategy.MIN else -inf

        for next_game_state, eval in next_valid_game_states.items():
            if ((players_strategy == PlayerStrategy.MIN and eval < best_evaluation)
                or (players_strategy == PlayerStrategy.MAX and eval > best_evaluation)) :
                best_game_state = next_game_state
                best_evaluation = eval
        return best_game_state.game_state, best_evaluation

    best_game_state, best_eval = minmax_rec(game.game_state, 1)
    game.game_state = best_game_state
    game.player_turn = PlayerStrategy.MAX if players_strategy == PlayerStrategy.MIN else PlayerStrategy.MIN
    game.turn_number += 1
    return best_game_state, best_eval
    # ! TO-DO:
    #   1. take all the player's pawns
    #   2. generate next valid moves for each pawn
    #   3. create a dictionary 'children' where the key is the next valid game_state
    #       and the value is initially -1
    #   4. recursively evaluate each child using minmax function
    #   5. select min or max value out of all values based on the player's perspective

