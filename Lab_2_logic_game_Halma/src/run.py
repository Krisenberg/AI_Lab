from halma import Halma
import cli

def run_game(init_game_state_filename: str):
    input_game_state = cli.input_game_state(init_game_state_filename)
    game = Halma(input_game_state)
    for row in game.game_state:
        for index, cell in enumerate(row):
            if index < len(row) - 1:
                print(f'{cell}', end=' ')
            else:
                print(f'{cell}')
    # players_pawns = game.players_pawns()
    # for pawn in players_pawns:
    #     print(f'POSSIBLE MOVES FOR PAWN AT: {pawn}')
    #     valid_moves = game.generate_valid_moves(pawn)
    #     print(valid_moves)
    win_check = game.check_board_for_win(game.game_state)
    print(f'Result of the win check:  {win_check}')
    # print(game.game_state)

if __name__ == '__main__':
    # Link to the halma game strategy: https://www.wikihow.com/Win-at-Chinese-Checkers
    run_game('win_check_no_win.txt')