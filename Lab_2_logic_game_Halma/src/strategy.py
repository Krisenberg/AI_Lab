import cli
from halma import players_pawns

def calc_dist(pawn, goal):
    return abs(pawn[0] - goal[0]) + abs(pawn[1] - goal[1])

if __name__ == '__main__':
    input_game_state = cli.input_game_state('initial_state.txt')
    pawns = players_pawns(input_game_state, True)
    max_sum_max = 0
    max_sum_min = 0
    for pawn in pawns:
        max_sum_max += calc_dist(pawn, (0,15))
        max_sum_min += calc_dist(pawn, (15,0))
    pawns = players_pawns(input_game_state, False)
    min_sum_max = 0
    min_sum_min = 0
    for pawn in pawns:
        min_sum_max += calc_dist(pawn, (15,0))
        min_sum_min += calc_dist(pawn, (0,15))
    print(f'Dist max sum for max: {max_sum_max}, min sum for max: {max_sum_min}')
    print(f'Dist max sum for min: {min_sum_max}, min sum for min: {min_sum_min}')
    
