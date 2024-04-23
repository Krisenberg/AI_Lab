from halma import Halma

def minmax(game_state: list[list[int]], players_perspective: int, max_depth: int):
    win_check = Halma.check_board_for_win(game_state)
    if win_check != 0:
        return (win_check - 1) * 100
    if max_depth == 0:
        pass # return heuristic function value
    # ! TO-DO:
    #   1. take all the player's pawns
    #   2. generate next valid moves for each pawn
    #   3. create a dictionary 'children' where the key is the next valid game_state
    #       and the value is initially -1
    #   4. recursively evaluate each child using minmax function
    #   5. select min or max value out of all values based on the player's perspective

