from math import inf
from halma import Halma, check_board_for_win, generate_valid_moves
from utils import players_pawns, Move, make_move, reverse_move    

def minimax(game: Halma, perform_pruning: bool = True, perform_sorting: bool = True):

    game_strategy = game.max_player_strategy if game.maximizing_player else game.min_player_strategy

    def minimax_rec(game_state: list[list[int]], depth_left: int, maximizing_player: bool,
                    alpha: float, beta: float, nodes_count: int):
        win_check = check_board_for_win(game_state)
        if win_check != 0 or depth_left == 0:
            eval = inf if win_check == 1 else (-inf if win_check == 2 else game_strategy.evaluate_game_state(game_state))
            return None, eval, nodes_count
        
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

        children_list = game_strategy.prepare_nodes_order(children, maximizing_player) if perform_sorting else list(children)
        if depth_left == game.minmax_depth and game_strategy.is_currently_end_game_strategy():
            for move in children_list:
                make_move(game_state, move)
                win_check = check_board_for_win(game_state)
                reverse_move(game_state, move)
                current_nodes_count += 1
                if win_check != 0:
                    eval = inf if win_check == 1 else -inf
                    return move, eval, nodes_count
        for move in (move for move in children_list if not prune_flag):
            make_move(game_state, move)
            _, eval, nodes = minimax_rec(game_state, depth_left - 1, not maximizing_player, alpha, beta, 0)
            reverse_move(game_state, move)
            current_nodes_count += 1
            nodes_count += nodes
            update_condition_max = maximizing_player and (best_move is None or eval > best_evaluation)
            update_condition_min = not maximizing_player and (best_move is None or eval < best_evaluation)
            if update_condition_max or update_condition_min:
                best_move = move
                best_evaluation = eval
            if maximizing_player:
                alpha = max(alpha, eval)
            else:
                beta = min(beta, eval)
            if perform_pruning and (beta <= alpha):
                prune_flag = True
                
        nodes_count += current_nodes_count
        return best_move, best_evaluation, nodes_count

    return minimax_rec(game.game_state, game.minmax_depth, game.maximizing_player, -inf, inf, 0)
