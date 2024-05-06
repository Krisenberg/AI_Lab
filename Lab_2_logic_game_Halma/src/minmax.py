from math import inf
from halma import Halma, check_board_for_win, generate_valid_moves
from utils import players_pawns, floor_euclidean_distance, Move, make_move, reverse_move
# from constants import MAXIMIZING_PLAYER_CAMP, MINIMIZING_PLAYER_CAMP, MIN_PAWN_DIST_SUM, MAX_PAWN_DIST_SUM  

# def mockup_heuristic(game_state: list[list[int]], maximizing_player: bool) -> float:
#     goal_cell = (0,15) if maximizing_player else (15,0)
#     goal_camp = MINIMIZING_PLAYER_CAMP if maximizing_player else MAXIMIZING_PLAYER_CAMP
#     pawns = players_pawns(game_state, maximizing_player)
#     dist_sum = 0
#     for pawn in pawns:
#         dist_sum += floor_euclidean_distance(pawn, goal_cell)
#     if maximizing_player:
#         dist_percentage = (1.0 - ((dist_sum - MIN_PAWN_DIST_SUM)/(MAX_PAWN_DIST_SUM - MIN_PAWN_DIST_SUM))) * 100.0
#         return dist_percentage
#     dist_percentage = ((dist_sum - MIN_PAWN_DIST_SUM)/(MAX_PAWN_DIST_SUM - MIN_PAWN_DIST_SUM)) * 100.0
#     return dist_percentage

# def sort_children_on_distance(children: set[Move], maximizing_player: bool) -> list[Move]:
#     goal_cell = (0,15) if maximizing_player else (15,0)
#     return sorted(children, key=lambda move: abs(move.move_to[0] - goal_cell[0]) + abs(move.move_to[1] - goal_cell[1]))
    

def minimax(game: Halma, perform_pruning: bool = True, perform_sorting: bool = True):

    game_strategy = game.max_player_strategy if game.maximizing_player else game.min_player_strategy

    def minimax_rec(game_state: list[list[int]], depth_left: int, maximizing_player: bool, alpha: float,
                    beta: float, nodes_count: int):
        win_check = check_board_for_win(game_state)
        if win_check != 0:
            if win_check == 1:
                return None, inf, nodes_count
            return None, -inf, nodes_count
        if depth_left == 0:
            return None, game_strategy.evaluate_game_state(game_state), nodes_count
        
        turn_number = game.turn_number + (game.minmax_depth - depth_left)
        if game_strategy.switch_strategy_check(game_state, turn_number):
            return None, game_strategy.evaluate_game_state(game_state), nodes_count

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
        current_nodes_count = 0

        if maximizing_player:
            if perform_sorting:
                children_sorted = game_strategy.prepare_nodes_order(children, True)
            else:
                children_sorted = list(children)
            for move in (move for move in children_sorted if not prune_flag):
                make_move(game_state, move)
                _, eval, nodes = minimax_rec(game_state, depth_left - 1, False, alpha, beta, 0)
                reverse_move(game_state, move)
                current_nodes_count += 1
                nodes_count += nodes
                if best_move is None or eval > best_evaluation:
                    best_move = move
                    best_evaluation = eval
                alpha = max(alpha, eval)
                if perform_pruning and (beta <= alpha):
                    prune_flag = True
        else:
            if perform_sorting:
                children_sorted = game_strategy.prepare_nodes_order(children, False)
            else:
                children_sorted = list(children)
            for move in (move for move in children_sorted if not prune_flag):
                make_move(game_state, move)
                _, eval, nodes = minimax_rec(game_state, depth_left - 1, True, alpha, beta, 0)
                reverse_move(game_state, move)
                current_nodes_count += 1
                nodes_count += nodes
                if best_move is None or eval < best_evaluation:
                    best_move = move
                    best_evaluation = eval
                beta = min(beta, eval)
                if perform_pruning and (beta <= alpha):
                    prune_flag = True
        nodes_count += current_nodes_count
        return best_move, best_evaluation, nodes_count

    return minimax_rec(game.game_state, game.minmax_depth, game.maximizing_player, -inf, inf, 0)
