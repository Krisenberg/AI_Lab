import cli
from halma import Halma, generate_valid_moves, check_board_for_win
from constants import PlayerStrategy
from minmax import minmax


def run_game(init_game_state_filename: str):
    input_game_state = cli.input_game_state(init_game_state_filename)
    game = Halma(input_game_state, 3, PlayerStrategy.MIN)
    for row in game.game_state:
        for index, cell in enumerate(row):
            if index < len(row) - 1:
                print(f'{cell}', end=' ')
            else:
                print(f'{cell}')
    # players_pawns = game.players_pawns()
    # for pawn in players_pawns:
    #     print(f'POSSIBLE MOVES FOR PAWN AT: {pawn}')
    #     valid_moves = generate_valid_moves(game.game_state, pawn)
    #     print(valid_moves)
    # win_check = check_board_for_win(game.game_state)
    # print(f'Result of the win check:  {win_check}')
    # print(game.game_state)
    while (check_board_for_win(game.game_state) == 0):
        print(f'Turn number: {game.turn_number}')
        print(f'Player: {game.player_turn.value} [{game.player_turn.name}]')
        new_gamestate, eval = minmax(game)
        print(f'Evaluation: {eval}, new game state:')
        for row in new_gamestate:
            for index, cell in enumerate(row):
                if index < len(row) - 1:
                    print(f'{cell}', end=' ')
                else:
                    print(f'{cell}')

if __name__ == '__main__':
    # Link to the halma game strategy: https://www.wikihow.com/Win-at-Chinese-Checkers
    run_game('initial_state.txt')