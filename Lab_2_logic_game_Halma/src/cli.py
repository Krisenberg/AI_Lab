import constants as const
import os

def input_game_state(game_state_filename: str):
    file_path = os.path.join(const.TEST_CASE_DIR, game_state_filename)
    game_state = []
    with open(file_path, encoding='utf8') as input_file:
        for line in input_file.read().splitlines():
            row_tab = line.split(' ')
            game_state.append([int(x) for x in row_tab])
    return game_state
    # for row in game_state:
    #     print(row)

# if __name__ == '__main__':
#     input_game_state('initial_state.txt')