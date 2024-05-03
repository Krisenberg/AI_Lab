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
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        pass

class EarlyGameFormObstacle(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
        self.penalty_square_size = const.EARLY_GAME_FORM_OBSTACLE_PENALTY_SQUARE_SIZE
        obstacle_cells_min_player = { (4,10), (5,10), (3,11), (4,11), (5,11), (4,12) }
        obstacle_cells_max_player = { (11,3), (10,4), (11,4), (12,4), (10,5), (11,5) }

        self.obstacle_cells = obstacle_cells_max_player if maximizing_player else obstacle_cells_min_player
        self.max_player = maximizing_player
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        base_corner = (15,0) if self.max_player else (0,15)
        penalty_square_pawns = 0
        pawns_in_obstacle_area = 0
        if self.max_player:
            for pawn in pawns:
                if pawn[0] > (base_corner[0] - self.penalty_square_size) and pawn[1] < (base_corner[1] + self.penalty_square_size):
                    penalty_square_pawns += 1
            for cell in self.obstacle_cells:
                if game_state[cell[0]][cell[1]] == const.MAXIMIZING_PLAYER_MARK:
                    pawns_in_obstacle_area += 1
            return (1.0 - ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells)))) * 100.0
        for pawn in pawns:
            if pawn[0] < (base_corner[0] + self.penalty_square_size) and pawn[1] > (base_corner[1] - self.penalty_square_size):
                penalty_square_pawns += 1
        for cell in self.obstacle_cells:
            if game_state[cell[0]][cell[1]] == const.MINIMIZING_PLAYER_MARK:
                pawns_in_obstacle_area += 1
        return ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells))) * 100.0
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        players_mark = const.MAXIMIZING_PLAYER_MARK if self.max_player else const.MINIMIZING_PLAYER_MARK
        for cell in self.obstacle_cells:
            if game_state[cell[0]][cell[1]] != players_mark:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        base_corner = (15,0) if self.max_player else (0,15)
        if self.max_player:
            return sorted(children, key=lambda move: 
                -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
                    -1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
                        and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
                        1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
                            and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
                            2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
                        )
                    )
                ), reverse=True
            )
        return sorted(children, key=lambda move: 
            -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
                -1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
                    and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
                    1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
                        and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
                        2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
                    )
                )
            ), reverse=True
        )

class EarlyGameConquerCenter(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
        self.target_cell = (8,7) if maximizing_player else (7,8)
        self.max_player = maximizing_player
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0

        for pawn in pawns:
            dist_sum += (-1.0) * floor_euclidean_distance(pawn, self.target_cell) if self.max_player else floor_euclidean_distance(pawn, self.target_cell)
        return dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if floor_euclidean_distance(pawn, self.target_cell) > 2:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        return sorted(children, key=lambda move: floor_euclidean_distance(move.move_to, self.target_cell), reverse=True)

class MiddleGameMoveDiagonal(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.MIDDLE_GAME_TURN_LIMIT
        self.target_cell = (0,15) if maximizing_player else (15,0)
        self.goal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET
        self.max_player = maximizing_player
    
    def _calculate_distance(self, pawn: tuple[int,int]):
        diagonal_offset = abs(15 - (pawn[0] + pawn[1]))
        penalty = diagonal_offset if diagonal_offset <= 4 else (2 * diagonal_offset)
        return floor_euclidean_distance(pawn, self.target_cell) + penalty

    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        
        for pawn in pawns:
            dist = self._calculate_distance(pawn)
            dist_sum += (-1.0) * dist if self.max_player else dist

        return dist_sum
    
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
    
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        return sorted(children, key=lambda move: self._calculate_distance(move.move_to) - self._calculate_distance(move.move_from))
                      
# class EarlyGameFormObstacle(Strategy):

#     def __init__(self, maximizing_player: bool):
#         self.max_turn_switch = const.EARLY_GAME_FORM_OBSTACLE_MAX_TURN
#         self.penalty_square_size = const.EARLY_GAME_FORM_OBSTACLE_PENALTY_SQUARE_SIZE
#         obstacle_cells_min_player = { (4,10), (5,10), (3,11), (4,11), (5,11), (4,12) }
#         obstacle_cells_max_player = { (11,3), (10,4), (11,4), (12,4), (10,5), (11,5) }

#         self.obstacle_cells = obstacle_cells_max_player if maximizing_player else obstacle_cells_min_player
#         self.max_player = maximizing_player
    
#     def evaluate(self, game_state: list[list[int]]) -> float:
#         pawns = players_pawns(game_state, self.max_player)
#         base_corner = (15,0) if self.max_player else (0,15)
#         penalty_square_pawns = 0
#         pawns_in_obstacle_area = 0
#         if self.max_player:
#             for pawn in pawns:
#                 if pawn[0] > (base_corner[0] - self.penalty_square_size) and pawn[1] < (base_corner[1] + self.penalty_square_size):
#                     penalty_square_pawns += 1
#             for cell in self.obstacle_cells:
#                 if game_state[cell[0]][cell[1]] == const.MAXIMIZING_PLAYER_MARK:
#                     pawns_in_obstacle_area += 1
#             return (1.0 - ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells)))) * 100.0
#         for pawn in pawns:
#             if pawn[0] < (base_corner[0] + self.penalty_square_size) and pawn[1] > (base_corner[1] - self.penalty_square_size):
#                 penalty_square_pawns += 1
#         for cell in self.obstacle_cells:
#             if game_state[cell[0]][cell[1]] == const.MINIMIZING_PLAYER_MARK:
#                 pawns_in_obstacle_area += 1
#         return ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells))) * 100.0
    
#     def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
#         if turn_number == self.max_turn_switch:
#             return True
#         players_mark = const.MAXIMIZING_PLAYER_MARK if self.max_player else const.MINIMIZING_PLAYER_MARK
#         for cell in self.obstacle_cells:
#             if game_state[cell[0]][cell[1]] != players_mark:
#                 return False
#         return True
    
#     def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
#         base_corner = (15,0) if self.max_player else (0,15)
#         if self.max_player:
#             return sorted(children, key=lambda move: 
#                 -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
#                     -1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
#                         and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
#                         1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
#                             and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
#                             2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
#                         )
#                     )
#                 ), reverse=True
#             )
#         return sorted(children, key=lambda move: 
#             -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
#                 -1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
#                     and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
#                     1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
#                         and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
#                         2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
#                     )
#                 )
#             ), reverse=True
#         )

class EndGameFillFromEnd(Strategy):

    def __init__(self, maximizing_player: bool):
        self.goal_cells_weights = const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MAX_PLAYER if maximizing_player else const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MIN_PLAYER
        self.max_player = maximizing_player
        self.target_cell = (0,15) if maximizing_player else (15,0)

    def _calculate_distance(self, pawn: tuple[int,int]) -> float:
        if pawn in self.goal_cells_weights:
            dist = self.goal_cells_weights[pawn]
        else:
            dist = (2.0 * floor_euclidean_distance(pawn, self.target_cell) + 4)
        return dist
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)

        dist_sum = 0
        for pawn in pawns:
            dist = self._calculate_distance(pawn)
            dist_sum += (-1.0) * dist if self.max_player else dist
        return dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return False
    
    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        return sorted(children, key=lambda move: self._calculate_distance(move.move_to) - self._calculate_distance(move.move_from))
    
# class EarlyGameFormObstacle(Strategy):

#     def __init__(self, maximizing_player: bool):
#         self.max_turn_switch = const.EARLY_GAME_FORM_OBSTACLE_MAX_TURN
#         self.penalty_square_size = const.EARLY_GAME_FORM_OBSTACLE_PENALTY_SQUARE_SIZE
#         obstacle_cells_min_player = { (4,10), (5,10), (3,11), (4,11), (5,11), (4,12) }
#         obstacle_cells_max_player = { (11,3), (10,4), (11,4), (12,4), (10,5), (11,5) }

#         self.obstacle_cells = obstacle_cells_max_player if maximizing_player else obstacle_cells_min_player
#         self.max_player = maximizing_player
    
#     def evaluate(self, game_state: list[list[int]]) -> float:
#         pawns = players_pawns(game_state, self.max_player)
#         base_corner = (15,0) if self.max_player else (0,15)
#         penalty_square_pawns = 0
#         pawns_in_obstacle_area = 0
#         if self.max_player:
#             for pawn in pawns:
#                 if pawn[0] > (base_corner[0] - self.penalty_square_size) and pawn[1] < (base_corner[1] + self.penalty_square_size):
#                     penalty_square_pawns += 1
#             for cell in self.obstacle_cells:
#                 if game_state[cell[0]][cell[1]] == const.MAXIMIZING_PLAYER_MARK:
#                     pawns_in_obstacle_area += 1
#             return (1.0 - ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells)))) * 100.0
#         for pawn in pawns:
#             if pawn[0] < (base_corner[0] + self.penalty_square_size) and pawn[1] > (base_corner[1] - self.penalty_square_size):
#                 penalty_square_pawns += 1
#         for cell in self.obstacle_cells:
#             if game_state[cell[0]][cell[1]] == const.MINIMIZING_PLAYER_MARK:
#                 pawns_in_obstacle_area += 1
#         return ((penalty_square_pawns + (len(self.obstacle_cells) - pawns_in_obstacle_area))/(self.penalty_square_size**2 + len(self.obstacle_cells))) * 100.0
    
#     def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
#         if turn_number == self.max_turn_switch:
#             return True
#         players_mark = const.MAXIMIZING_PLAYER_MARK if self.max_player else const.MINIMIZING_PLAYER_MARK
#         for cell in self.obstacle_cells:
#             if game_state[cell[0]][cell[1]] != players_mark:
#                 return False
#         return True
    
#     def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
#         base_corner = (15,0) if self.max_player else (0,15)
#         if self.max_player:
#             return sorted(children, key=lambda move: 
#                 -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
#                     -1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
#                         and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
#                         1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
#                             and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
#                             2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
#                         )
#                     )
#                 ), reverse=True
#             )
#         return sorted(children, key=lambda move: 
#             -2 if move.move_from in self.obstacle_cells and move.move_to not in self.obstacle_cells else (
#                 -1 if move.move_from[0] > (base_corner[0] - self.penalty_square_size) and move.move_from[1] < (base_corner[1] + self.penalty_square_size)
#                     and move.move_to[0] <= (base_corner[0] - self.penalty_square_size) and move.move_to[1] >= (base_corner[1] + self.penalty_square_size) else (
#                     1 if move.move_from[0] <= (base_corner[0] - self.penalty_square_size) and move.move_from[1] >= (base_corner[1] + self.penalty_square_size)
#                         and move.move_to[0] > (base_corner[0] - self.penalty_square_size) and move.move_to[1] < (base_corner[1] + self.penalty_square_size) else (
#                         2 if move.move_from not in self.obstacle_cells and move.move_to in self.obstacle_cells else 0
#                     )
#                 )
#             ), reverse=True
#         )
        
        

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
        PlayerStrategy.END_GAME_FILL_FROM_END : EndGameFillFromEnd
    }

    def __init__(self, maximizing_player: bool, early_strategy: PlayerStrategy, mid_strategy: PlayerStrategy, end_strategy: PlayerStrategy):
        # self.early_game_strategy = self.map_strategy_name_to_class[early_strategy](maximizing_player)
        # self.middle_game_strategy = mid_strategy
        # self.end_game_strategy = end_strategy
        self.strategies = [
            self.map_strategy_name_to_class[early_strategy](maximizing_player),
            self.map_strategy_name_to_class[mid_strategy](maximizing_player),
            self.map_strategy_name_to_class[end_strategy](maximizing_player)
        ]
        self.current_strategy = 0
    
    def evaluate_game_state(self, game_state: list[list[int]]) -> float:
        return self.strategies[self.current_strategy].evaluate(game_state)
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return self.strategies[self.current_strategy].switch_strategy_check(game_state, turn_number)
    
    def switch_strategy(self) -> None:
        self.current_strategy = 1 if self.current_strategy == 0 else 2

    def prepare_nodes_order(self, children: set[Move]) -> list[Move]:
        return self.strategies[self.current_strategy].prepare_nodes_order(children)

def calc_dist(pawn, goal):
    return abs(pawn[0] - goal[0]) + abs(pawn[1] - goal[1])

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
    
