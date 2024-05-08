from utils import players_pawns, floor_euclidean_distance, input_game_state, Move
from abc import ABC, abstractmethod
from enum import Enum
import constants as const


class Strategy(ABC):

    @abstractmethod
    def evaluate(self, game_state: list[list[int]]) -> float:
        pass

    @abstractmethod
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        pass

    @abstractmethod
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        pass

class EarlyGameFormObstacle(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
        self.target_cell = (9,6) if maximizing_player else (6,9)
        self.obstacle_cells = const.OBSTACLE_CELLS_MAX_PLAYER if maximizing_player else const.OBSTACLE_CELLS_MIN_PLAYER
        self.max_player = maximizing_player
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        ''' We want to move our pawns towards middle of the board but also we would like to form some kind
            of obstacle on the main diagonal that will stop the opponent later.
        '''
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        pawns_in_obstacle_area = 0
        for pawn in pawns:
            dist_sum += floor_euclidean_distance(pawn, self.target_cell)
            pawns_in_obstacle_area += 1 if pawn in self.obstacle_cells else 0

        # pawns_in_obstacle_area = 0
        # for cell in self.obstacle_cells:
        #     if (self.max_player and game_state[cell[0]][cell[1]] == const.MAXIMIZING_PLAYER_MARK
        #         or not self.max_player and game_state[cell[0]][cell[1]] == const.MINIMIZING_PLAYER_MARK):
        #         pawns_in_obstacle_area += 1
        free_cells_obstacle_area = len(self.obstacle_cells) - pawns_in_obstacle_area
        
        if self.max_player:
            return -((2 * dist_sum) - free_cells_obstacle_area)
        return (2 * dist_sum) - free_cells_obstacle_area
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if floor_euclidean_distance(pawn, self.target_cell) > 2 and pawn not in self.obstacle_cells:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: floor_euclidean_distance(move.move_to, self.target_cell), reverse=False)

    # def __init__(self, maximizing_player: bool):
    #     self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
    #     self.penalty_square_size = const.EARLY_GAME_FORM_OBSTACLE_PENALTY_SQUARE_SIZE
    #     self.obstacle_cells = const.OBSTACLE_CELLS_MAX_PLAYER if maximizing_player else const.OBSTACLE_CELLS_MIN_PLAYER
    #     self.max_player = maximizing_player
    
    # def evaluate(self, game_state: list[list[int]]) -> float:
    #     pawns = players_pawns(game_state, self.max_player)
    #     base_corner = (15,0) if self.max_player else (0,15)
    #     penalty_square_pawns = 0
    #     pawns_in_obstacle_area = 0
    #     if self.max_player:
    #         for pawn in pawns:
    #             if pawn[0] > (base_corner[0] - self.penalty_square_size) and pawn[1] < (base_corner[1] + self.penalty_square_size):
    #                 penalty_square_pawns += 1
    #         for cell in self.obstacle_cells:
    #             if game_state[cell[0]][cell[1]] == const.MAXIMIZING_PLAYER_MARK:
    #                 pawns_in_obstacle_area += 1
    #         return (-1) * (len(self.obstacle_cells) - 1 + (2 * penalty_square_pawns) - pawns_in_obstacle_area)
    #         # return (1.0 - ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells)))) * 100.0
    #     for pawn in pawns:
    #         if pawn[0] < (base_corner[0] + self.penalty_square_size) and pawn[1] > (base_corner[1] - self.penalty_square_size):
    #             penalty_square_pawns += 1
    #     for cell in self.obstacle_cells:
    #         if game_state[cell[0]][cell[1]] == const.MINIMIZING_PLAYER_MARK:
    #             pawns_in_obstacle_area += 1
    #     return (len(self.obstacle_cells) + 1 + (2 * penalty_square_pawns) - pawns_in_obstacle_area)
    #     # return ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells))) * 100.0
    
    # def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
    #     if turn_number == self.max_turn_switch:
    #         return True
    #     players_mark = const.MAXIMIZING_PLAYER_MARK if self.max_player else const.MINIMIZING_PLAYER_MARK
    #     for cell in self.obstacle_cells:
    #         if game_state[cell[0]][cell[1]] != players_mark:
    #             return False
    #     return True
    
    # def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
    #     base_corner = (15,0) if self.max_player else (0,15)
    #     if self.max_player:
    #         return sorted(children, key=lambda move: 
    #             -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
    #                 2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else (
    #                     -1 if (move.move_from[0] <= (base_corner[0] - self.penalty_square_size) or move.move_from[1] >= (base_corner[1] + self.penalty_square_size))
    #                         and (move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size)) else (
    #                             1 if (move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size))
    #                                 and (move.move_to[0] <= (base_corner[0] - self.penalty_square_size) or move.move_to[1] >= (base_corner[1] + self.penalty_square_size)) else 0
    #                         )
    #                     )
    #                 ), reverse=True)
        
    #     return sorted(children, key=lambda move: 
    #         -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
    #             2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else (
    #                 -1 if (move.move_from[0] > (base_corner[0] + self.penalty_square_size) or move.move_from[1] < (base_corner[1] - self.penalty_square_size))
    #                     and (move.move_to[0] <= (base_corner[0] + self.penalty_square_size) and move.move_to[1] >= (base_corner[1] - self.penalty_square_size)) else (
    #                         1 if (move.move_from[0] <= (base_corner[0] + self.penalty_square_size) and move.move_from[1] >= (base_corner[1] - self.penalty_square_size))
    #                             and (move.move_to[0] > (base_corner[0] + self.penalty_square_size) or move.move_to[1] < (base_corner[1] - self.penalty_square_size)) else 0
    #                     )
    #                 )
    #             ), reverse=True)

class EarlyGameConquerCenter(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
        self.target_cell = (9,6) if maximizing_player else (6,9)
        self.max_player = maximizing_player
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        ''' We want to have as much our pawns around the target cell as possible.
        '''
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += floor_euclidean_distance(pawn, self.target_cell)
        return -dist_sum if self.max_player else dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if floor_euclidean_distance(pawn, self.target_cell) > 2:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: floor_euclidean_distance(move.move_to, self.target_cell), reverse=False)

class MiddleGameMoveDiagonal(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.MIDDLE_GAME_TURN_LIMIT
        self.target_cell = (4,11) if maximizing_player else (11,4)
        self.diagonal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_DIAGONAL_OFFSET
        self.goal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET
        self.max_player = maximizing_player
    
    def _calculate_distance(self, pawn: tuple[int,int]):
        diagonal_offset = abs(15 - (pawn[0] + pawn[1]))
        penalty = diagonal_offset if diagonal_offset <= self.diagonal_offset else (2 * diagonal_offset)
        return (floor_euclidean_distance(pawn, self.target_cell) + penalty)

    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns_max_player = players_pawns(game_state, True)
        pawns_min_player = players_pawns(game_state, False)
        dist_sum_max = 0
        dist_sum_min = 0
        
        for pawn in pawns_max_player:
            dist_sum_max += self._calculate_distance(pawn)
        for pawn in pawns_min_player:
            dist_sum_min += self._calculate_distance(pawn)
        
        # if self.max_player:
        #     return dist_sum_min - dist_sum_max
        # return dist_sum_max - dist_sum_min
        return dist_sum_min - dist_sum_max
        # pawns = players_pawns(game_state, self.max_player)
        # dist_sum = 0
        
        # for pawn in pawns:
        #     dist = self._calculate_distance(pawn)
        #     dist_sum += (-1.0) * dist if self.max_player else dist

        # return dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if self.max_player and (pawn[0] >= (self.target_cell[0] + self.goal_offset) or pawn[1] <= (self.target_cell[1] - self.goal_offset)):
                return False
            if not self.max_player and (pawn[0] <= (self.target_cell[0] - self.goal_offset) or pawn[1] >= (self.target_cell[1] + self.goal_offset)):
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self._calculate_distance(move.move_to) - self._calculate_distance(move.move_from))
                      
class MiddleGameControlPawns(Strategy):
    '''Strategy to move towards the goal cell while trying not to allow opponent to jump
        and keeping own pawns close to each other
    '''

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.MIDDLE_GAME_TURN_LIMIT
        self.target_cell = (4,11) if maximizing_player else (11,4)
        self.max_player = maximizing_player
    
    def check_neighbours(self, pawn_pos: tuple[int,int], game_state: list[list[int]]):
        i_offsets = [-1, 0, 1]
        j_offsets = [-1, 0, 1]
        opponent_mark = 2 if self.max_player else 1
        player_mark = 1 if self.max_player else 2
        neighbour_opponents = 0
        neighbour_allies = 0
        for i in i_offsets:
            for j in j_offsets:
                if (pawn_pos[0] + i in range (len(game_state)) and pawn_pos[1] + j in range (len(game_state))):
                    if (game_state[pawn_pos[0] + i][pawn_pos[1] + j] == opponent_mark):
                        neighbour_opponents += 1
                    if (game_state[pawn_pos[0] + i][pawn_pos[1] + j] == player_mark):
                        neighbour_allies += 1
        return neighbour_opponents, neighbour_allies
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += floor_euclidean_distance(pawn, self.target_cell)
            neigh_opp, neigh_all = self.check_neighbours(pawn, game_state)
        return -(dist_sum + neigh_opp - neigh_all) if self.max_player else (dist_sum + neigh_opp - neigh_all)
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if floor_euclidean_distance(pawn, self.target_cell) > 2:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        return sorted(children, key=lambda move: floor_euclidean_distance(move.move_to, self.target_cell) - floor_euclidean_distance(move.move_from, self.target_cell), reverse=False)

class EndGameFillFromEnd(Strategy):

    def __init__(self, maximizing_player: bool):
        # self.goal_cells_weights = const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MAX_PLAYER if maximizing_player else const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MIN_PLAYER
        self.cell_weights_max = const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MAX_PLAYER
        self.cell_weights_min = const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MIN_PLAYER
        self.max_player = maximizing_player
        # self.target_cell = (0,15) if maximizing_player else (15,0)

    def _calculate_distance(self, pawn: tuple[int,int], max_player: bool) -> float:
        cell_weights = self.cell_weights_max if max_player else self.cell_weights_min
        target_cell = (0,15) if max_player else (15,0)
        # if pawn in cell_weights:
        #     dist = self.goal_cells_weights[pawn]
        # else:
        #     dist = floor_euclidean_distance(pawn, self.target_cell) + 4
        return cell_weights[pawn] if pawn in cell_weights else (floor_euclidean_distance(pawn, target_cell) + 4)
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        # pawns_in
        for pawn in pawns:
            dist_sum += self._calculate_distance(pawn, self.max_player)
        if self.max_player:
            return -dist_sum
        return dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return False
    
    def estimate_move_value(self, move: Move, max_player: bool) -> float:
        target_cell = (0,15) if max_player else (15,0)
        distance_delta = floor_euclidean_distance(move.move_to, target_cell) - floor_euclidean_distance(move.move_from, target_cell)
        base = const.MINIMIZING_PLAYER_CAMP if self.max_player else const.MAXIMIZING_PLAYER_CAMP
        cell_weights = self.cell_weights_max if max_player else self.cell_weights_min
        # pawn_in_base_bonus = 10 if move.move_to in base else 0
        pawn_in_base_bonus = (10 - cell_weights[move.move_to]) if move.move_to in cell_weights else 0
        return distance_delta - pawn_in_base_bonus
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self.estimate_move_value(move, max_player))
        # return sorted(children, key=lambda move: self._calculate_distance(move.move_to,) - self._calculate_distance(move.move_from))
    
class EndGameFillEveryOther(Strategy):

    def __init__(self, maximizing_player: bool):
        self.cell_weights_max = const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MAX_PLAYER
        self.cell_weights_min = const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MIN_PLAYER
        # self.goal_cells_weights = const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MAX_PLAYER if maximizing_player else const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MIN_PLAYER
        self.max_player = maximizing_player
        # self.target_cell = (0,15) if maximizing_player else (15,0)

    def _calculate_distance(self, pawn: tuple[int,int], max_player: bool) -> float:
        cell_weights = self.cell_weights_max if max_player else self.cell_weights_min
        target_cell = (0,15) if max_player else (15,0)
        return cell_weights[pawn] if pawn in cell_weights else (floor_euclidean_distance(pawn, target_cell) + 4)
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += self._calculate_distance(pawn, self.max_player)
        if self.max_player:
            return -dist_sum
        return dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return False
    
    def estimate_move_value(self, move: Move, max_player: bool) -> float:
        target_cell = (0,15) if max_player else (15,0)
        cell_weights = self.cell_weights_max if max_player else self.cell_weights_min
        distance_delta = floor_euclidean_distance(move.move_to, target_cell) - floor_euclidean_distance(move.move_from, target_cell)
        pawn_in_base_bonus = (10 - cell_weights[move.move_to]) if move.move_to in cell_weights else 0
        return distance_delta - pawn_in_base_bonus
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self.estimate_move_value(move, max_player))
    
    # def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
    #     return sorted(children, key=lambda move: self._calculate_distance(move.move_to) - self._calculate_distance(move.move_from))
        
        

class PlayerStrategy(Enum):
    """ Enum representing possible strategies

    Options
    -------
    - EARLY_GAME_FORM_OBSTACLE = 1 -> take pawns from behind of the base and form the obstacle out of them (to block opponent in the future)
    - EARLY_GAME_CONQUER_CENTER = 2 -> move pawns to the specific area in the middle of the board as fast as possible
    - MIDDLE_GAME_MOVE_DIAGONAL = 3 -> move pawns along the defined diagonal to lead them directly into the opponent's base camp
    - MIDDLE_GAME_CONTROL_PAWNS = 4 -> control every pawn not to go away from other ones (not to limit the jump possibilities)
    - END_GAME_FILL_FROM_END = 5 -> in the end game try to fill the camp from the end (from the furthest cell up to the borders)
    - END_GAME_FILL_EVERY_OTHER = 6 -> in the end game fill the camp starting by filling every other row (to fill the rest cells by jumping then)
    """
    EARLY_GAME_FORM_OBSTACLE = 1
    EARLY_GAME_CONQUER_CENTER = 2
    MIDDLE_GAME_MOVE_DIAGONAL = 3
    MIDDLE_GAME_CONTROL_PAWNS = 4
    END_GAME_FILL_FROM_END = 5
    END_GAME_FILL_EVERY_OTHER = 6


class GameStrategy:
    map_strategy_name_to_class = {
        PlayerStrategy.EARLY_GAME_FORM_OBSTACLE : EarlyGameFormObstacle,
        PlayerStrategy.EARLY_GAME_CONQUER_CENTER : EarlyGameConquerCenter,
        PlayerStrategy.MIDDLE_GAME_MOVE_DIAGONAL : MiddleGameMoveDiagonal,
        PlayerStrategy.END_GAME_FILL_FROM_END : EndGameFillFromEnd,
        PlayerStrategy.END_GAME_FILL_EVERY_OTHER : EndGameFillEveryOther
    }

    def __init__(self, maximizing_player: bool, early_strategy: PlayerStrategy, mid_strategy: PlayerStrategy, end_strategy: PlayerStrategy):
        self.strategies = [
            self.map_strategy_name_to_class[early_strategy](maximizing_player),
            self.map_strategy_name_to_class[mid_strategy](maximizing_player),
            self.map_strategy_name_to_class[end_strategy](maximizing_player)
        ]
        self.maximizing_player = maximizing_player
        self.current_strategy = 0
        self.tabu_set_from = set()
    
    def evaluate_game_state(self, game_state: list[list[int]]) -> float:
        return self.strategies[self.current_strategy].evaluate(game_state)
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return self.strategies[self.current_strategy].switch_strategy_check(game_state, turn_number)
    
    def switch_strategy(self) -> None:
        if isinstance(self.strategies[self.current_strategy], EarlyGameFormObstacle):
            self.tabu_set_from = const.OBSTACLE_CELLS_MAX_PLAYER if self.maximizing_player else const.OBSTACLE_CELLS_MIN_PLAYER
        self.current_strategy = 1 if self.current_strategy == 0 else 2
        if self.current_strategy == 2:
            self.tabu_set_from = set()

    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        valid_moves = {move for move in children if move.move_from not in self.tabu_set_from}
        return self.strategies[self.current_strategy].prepare_nodes_order(valid_moves, max_player)

    def is_currently_end_game_strategy(self) -> bool:
        return self.current_strategy == 2

# def calc_dist(pawn, goal):
#     return abs(pawn[0] - goal[0]) + abs(pawn[1] - goal[1])

if __name__ == '__main__':
    input_game_state = input_game_state('initial_state.txt')
    pawns = players_pawns(input_game_state, True)
    max_sum_max = 0
    max_sum_min = 0
    for pawn in pawns:
        max_sum_max += floor_euclidean_distance(pawn, (0,15))
        max_sum_min += floor_euclidean_distance(pawn, (15,0))
    pawns = players_pawns(input_game_state, False)
    min_sum_max = 0
    min_sum_min = 0
    for pawn in pawns:
        min_sum_max += floor_euclidean_distance(pawn, (15,0))
        min_sum_min += floor_euclidean_distance(pawn, (0,15))
    print(f'Dist max sum for max: {max_sum_max}, min sum for max: {max_sum_min}')
    print(f'Dist max sum for min: {min_sum_max}, min sum for min: {min_sum_min}')
    
