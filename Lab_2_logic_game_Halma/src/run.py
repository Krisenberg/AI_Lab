import halma
import cli

def run_game(init_game_state_filename: str):
    input_game_state = cli.input_game_state(init_game_state_filename)
    game = halma.Halma(input_game_state)
    for row in game.game_state:
        for index, cell in enumerate(row):
            if index < len(row) - 1:
                print(f'{cell}', end=' ')
            else:
                print(f'{cell}')
    # print(game.game_state)

if __name__ == '__main__':
    run_game('initial_state.txt')