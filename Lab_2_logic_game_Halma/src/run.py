from datetime import datetime
from halma import Halma, check_board_for_win
# from constants import PlayerStrategy
from minmax import minimax, make_move
from utils import print_board, input_game_state
from strategy import PlayerStrategy, GameStrategy

def print_turn_stats(game: Halma, move_evaluation: float):
    print(f'Player: {'MAX [1]' if game.maximizing_player else 'MIN [2]'} | Turn: {game.turn_number} | Move: {game.move_number}')
    print(f'Evaluation: {move_evaluation}')
    print_board(game.game_state)


def run_game(init_game_state_filename: str, max_player_strategy: GameStrategy, min_player_strategy: GameStrategy, max_depth: int = 3, debug_print: bool = False):
    input = input_game_state(init_game_state_filename)
    game = Halma(input, max_depth, max_player_strategy, min_player_strategy)
    # if debug_print:
    #     print_board(game.game_state)
    # for row in game.game_state:
    #     for index, cell in enumerate(row):
    #         if index < len(row) - 1:
    #             print(f'{cell}', end=' ')
    #         else:
    #             print(f'{cell}')

    # players_pawns = game.players_pawns()
    # for pawn in players_pawns:
    #     print(f'POSSIBLE MOVES FOR PAWN AT: {pawn}')
    #     valid_moves = generate_valid_moves(game.game_state, pawn)
    #     print(valid_moves)
    # win_check = check_board_for_win(game.game_state)
    # print(f'Result of the win check:  {win_check}')
    # print(game.game_state)

    # while (game.move_number <= 35 and check_board_for_win(game.game_state) == 0):
    while (check_board_for_win(game.game_state) == 0):
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
            print_turn_stats(game, best_eval)
        if game.maximizing_player:
            game.max_player_visited_nodes[game.turn_number] = nodes_count
            game.max_player_move_time[game.turn_number] = round((end_timestamp - start_timestamp).total_seconds() * 1000.0)
        else:
            game.min_player_visited_nodes[game.turn_number] = nodes_count
            game.min_player_move_time[game.turn_number] = round((end_timestamp - start_timestamp).total_seconds() * 1000.0)
        game.maximizing_player = not game.maximizing_player
        game.turn_number = (game.move_number // 2 ) + 1
        game.move_number += 1
    return game
        # for row in game.game_state:
        #     for index, cell in enumerate(row):
        #         if index < len(row) - 1:
        #             print(f'{cell}', end=' ')
        #         else:
        #             print(f'{cell}')

if __name__ == '__main__':
    # Link to the halma game strategy: https://www.wikihow.com/Win-at-Chinese-Checkers
    max_player_strategy = GameStrategy(True, PlayerStrategy.EARLY_GAME_FORM_OBSTACLE, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_FROM_END)
    min_player_strategy = GameStrategy(False, PlayerStrategy.EARLY_GAME_CONQUER_CENTER, PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL, PlayerStrategy.END_GAME_FILL_FROM_END)
    run_game('initial_state.txt', max_player_strategy, min_player_strategy, 3, debug_print=True)