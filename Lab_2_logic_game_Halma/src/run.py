from datetime import datetime
from halma import Halma, check_board_for_win, generate_valid_moves
from minmax import minimax, make_move
from utils import print_board, input_game_state, players_pawns
from strategy import PlayerStrategy, GameStrategy

def print_turn_stats_and_board(game: Halma, move_evaluation: float, nodes_count: int):
    print(f'Player: {'MAX [1]' if game.maximizing_player else 'MIN [2]'} | Turn: {game.turn_number} | Move: {game.move_number}')
    print(f'Evaluation: {move_evaluation}, nodes count: {nodes_count}')
    print_board(game.game_state)

def print_turn_stats(game: Halma, move_evaluation: float, nodes_count: int):
    print(f'Player: {'MAX [1]' if game.maximizing_player else 'MIN [2]'} | Turn: {game.turn_number} | Move: {game.move_number}')
    print(f'Evaluation: {move_evaluation}, nodes count: {nodes_count}')


def run_game(init_game_state_filename: str, max_player_strategy: GameStrategy, min_player_strategy: GameStrategy, max_depth: int = 3, debug_print: bool = False):
    input = input_game_state(init_game_state_filename)
    game = Halma(input, max_depth, max_player_strategy, min_player_strategy)

    # while (game.move_number <= 35 and check_board_for_win(game.game_state) == 0):
    while (check_board_for_win(game.game_state) == 0):
        if (game.turn_number == 75):
            pass
        start_timestamp = datetime.now()
        best_move, best_eval, nodes_count = minimax(game)
        if best_move is None and game.maximizing_player and game.max_player_strategy.switch_strategy_check(game.game_state, game.turn_number):
            game.max_player_strategy.switch_strategy()
            best_move, best_eval, nodes_count = minimax(game)
        if best_move is None and not game.maximizing_player and game.min_player_strategy.switch_strategy_check(game.game_state, game.turn_number):
            game.min_player_strategy.switch_strategy()
            best_move, best_eval, nodes_count = minimax(game)
        # if best_move is None:
        #     best_move, best_eval, nodes_count = minimax(game)
        end_timestamp = datetime.now()
        make_move(game.game_state, best_move)
        if debug_print:
            print_turn_stats_and_board(game, best_eval, nodes_count)
        else:
            print_turn_stats(game, best_eval, nodes_count)
        if game.maximizing_player:
            game.max_player_visited_nodes[game.turn_number] = nodes_count
            game.max_player_move_time[game.turn_number] = round((end_timestamp - start_timestamp).total_seconds() * 1000.0)
            # if game.max_player_strategy.is_currently_end_game_strategy():
            #     game.max_player_strategy.tabu_set_to.add(best_move.move_from)
        else:
            game.min_player_visited_nodes[game.turn_number] = nodes_count
            game.min_player_move_time[game.turn_number] = round((end_timestamp - start_timestamp).total_seconds() * 1000.0)
            # if game.min_player_strategy.is_currently_end_game_strategy():
            #     game.min_player_strategy.tabu_set_to.add(best_move.move_from)
        game.maximizing_player = not game.maximizing_player
        game.turn_number = (game.move_number // 2 ) + 1
        game.move_number += 1
    return game

def test_moves(init_game_state_filename: str, max_player_strategy: GameStrategy, min_player_strategy: GameStrategy, max_depth: int = 3):
    input = input_game_state(init_game_state_filename)
    game = Halma(input, max_depth, max_player_strategy, min_player_strategy)
    pawns = players_pawns(input, True)
    for pawn in pawns:
        if pawn == (7,6):
            print(f'POSSIBLE MOVES FOR PAWN AT: {pawn}')
            valid_moves = generate_valid_moves(game.game_state, pawn)
            print(valid_moves)

if __name__ == '__main__':
    # Link to the halma game strategy: https://www.wikihow.com/Win-at-Chinese-Checkers
    max_player_strategy = GameStrategy(True, PlayerStrategy.EARLY_GAME_CONQUER_CENTER, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_EVERY_OTHER)
    min_player_strategy = GameStrategy(False, PlayerStrategy.EARLY_GAME_CONQUER_CENTER, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_FROM_END)
    run_game('initial_state.txt', max_player_strategy, min_player_strategy, 3, debug_print=True)
    # test_moves('test_moves_from_game.txt', max_player_strategy, min_player_strategy, 3)