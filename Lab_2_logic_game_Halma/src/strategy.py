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
        self.target_cell = const.EARLY_GAME_FROM_OBSTACLE_TARGET_CELL_MAX if maximizing_player else const.EARLY_GAME_FROM_OBSTACLE_TARGET_CELL_MIN
        self.obstacle_cells = const.OBSTACLE_CELLS_MAX_PLAYER if maximizing_player else const.OBSTACLE_CELLS_MIN_PLAYER
        self.max_player = maximizing_player
        self.escape_square_size = const.EARLY_GAME_FORM_OBSTACLE_ESCAPE_SQUARE_SIZE
        self.min_pawns_outside_danger_zone = const.EARLY_GAME_FORM_OBSTACLE_MIN_AMOUT_OF_PAWNS_OUTSIDE_DANGER_ZONE
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        ''' We want to move our pawns towards middle of the board but also we would like to form some kind
            of obstacle on the main diagonal that will stop the opponent later.
        '''
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        pawns_in_obstacle_area = 0
        pawns_outside_danger_zone = 0
        for pawn in pawns:
            if self.max_player and (pawn[0] <= 15 - self.escape_square_size or pawn[1] >= self.escape_square_size):
                pawns_outside_danger_zone += 1
            if not self.max_player and (pawn[0] >= self.escape_square_size or pawn[1] <= 15 - self.escape_square_size):
                pawns_outside_danger_zone += 1
            dist_sum += floor_euclidean_distance(pawn, self.target_cell)
            pawns_in_obstacle_area += 1 if pawn in self.obstacle_cells else 0

        free_cells_obstacle_area = len(self.obstacle_cells) - pawns_in_obstacle_area
        if pawns_outside_danger_zone >= self.min_pawns_outside_danger_zone:
            eval = dist_sum + (2 * free_cells_obstacle_area)
        else:
            eval = (2 * dist_sum) + free_cells_obstacle_area
        return -eval if self.max_player else eval

    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        pawns_in_obstacle_area = 0
        for pawn in pawns:
            if floor_euclidean_distance(pawn, self.target_cell) > 2:
                return False
            elif pawn in self.obstacle_cells:
                pawns_in_obstacle_area += 1
        return True if pawns_in_obstacle_area == len(self.obstacle_cells) else False
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: floor_euclidean_distance(move.move_to, self.target_cell), reverse=False)


class EarlyGameConquerCenter(Strategy):

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.EARLY_GAME_TURN_LIMIT
        self.target_cell = const.EARLY_GAME_CONQUER_CENTER_TARGET_CELL_MAX if maximizing_player else const.EARLY_GAME_CONQUER_CENTER_TARGET_CELL_MIN
        self.max_player = maximizing_player
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        ''' We want to have as much our pawns around the target cell as possible.
        '''
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += floor_euclidean_distance(pawn, self.target_cell)
        return -(dist_sum) if self.max_player else dist_sum
    
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
        self.target_cell = (0,15) if maximizing_player else (15,0)
        self.diagonal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_DIAGONAL_OFFSET
        self.goal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET
        self.max_player = maximizing_player

    def __is_pawn_in_goal_area(self, pawn: tuple[int,int]):
        if self.max_player and (pawn[0] >= self.target_cell[0] + self.goal_offset or pawn[1] <= self.target_cell[1] - self.goal_offset):
            return False
        if not self.max_player and (pawn[0] <= self.target_cell[0] - self.goal_offset or pawn[1] >= self.target_cell[1] + self.goal_offset):
            return False
        return True

    def __calculate_distance(self, pawn: tuple[int,int]):
        diagonal_offset = abs(15 - (pawn[0] + pawn[1]))
        penalty = diagonal_offset if diagonal_offset <= self.diagonal_offset else (2 * diagonal_offset)
        distance_to_target = floor_euclidean_distance(pawn, self.target_cell)
        if self.__is_pawn_in_goal_area(pawn):
            return 0
        return distance_to_target + penalty

    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += self.__calculate_distance(pawn)
        return -dist_sum if self.max_player else dist_sum

    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            if self.__calculate_distance(pawn) != 0:
                return False
        return True

    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self.__calculate_distance(move.move_to) - self.__calculate_distance(move.move_from))
                      

class MiddleGameControlPawns(Strategy):
    '''Strategy to move towards the goal cell while trying not to allow opponent to jump
        and keeping own pawns close to each other
    '''

    def __init__(self, maximizing_player: bool):
        self.max_turn_switch = const.MIDDLE_GAME_TURN_LIMIT
        self.target_cell = (0,15) if maximizing_player else (15,0)
        self.goal_offset = const.MIDDLE_GAME_MOVE_DIAGONAL_GOAL_OFFSET
        self.max_player = maximizing_player

    def __is_pawn_in_goal_area(self, pawn: tuple[int,int]):
        if self.max_player and (pawn[0] >= self.target_cell[0] + self.goal_offset or pawn[1] <= self.target_cell[1] - self.goal_offset):
            return False
        if not self.max_player and (pawn[0] <= self.target_cell[0] - self.goal_offset or pawn[1] >= self.target_cell[1] + self.goal_offset):
            return False
        return True

    def check_neighbours(self, pawn_pos: tuple[int,int], game_state: list[list[int]]):
        i_offsets = [-1, 0, 1]
        j_offsets = [-1, 0, 1]
        opponent_mark = 2 if self.max_player else 1
        player_mark = 1 if self.max_player else 2
        neighbour_opponents = 0
        neighbour_allies = 0
        for i in i_offsets:
            for j in j_offsets:
                if (i != 0 or j != 0) and (pawn_pos[0] + i in range (len(game_state)) and pawn_pos[1] + j in range (len(game_state))):
                    if (game_state[pawn_pos[0] + i][pawn_pos[1] + j] == opponent_mark):
                        in_board = pawn_pos[0] - i in range (len(game_state)) and pawn_pos[1] - j in range (len(game_state))
                        if in_board and (game_state[pawn_pos[0] - i][pawn_pos[1] - j] == 0):
                            neighbour_opponents += 1
                    if (game_state[pawn_pos[0] + i][pawn_pos[1] + j] == player_mark):
                        in_board = pawn_pos[0] - i in range (len(game_state)) and pawn_pos[1] - j in range (len(game_state))
                        if in_board and (game_state[pawn_pos[0] - i][pawn_pos[1] - j] == 0):
                            neighbour_allies += 1
        return neighbour_opponents, neighbour_allies
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        neigh_opponents_sum = 0
        neigh_allies_sum = 0
        for pawn in pawns:
            dist = 0 if self.__is_pawn_in_goal_area(pawn) else floor_euclidean_distance(pawn, self.target_cell)
            dist_sum += dist
            neigh_opp, neigh_all = self.check_neighbours(pawn, game_state)
            neigh_opponents_sum += neigh_opp
            neigh_allies_sum += neigh_all
        value = dist_sum + neigh_opponents_sum - neigh_allies_sum
        return -value if self.max_player else value
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        if turn_number == self.max_turn_switch:
            return True
        pawns = players_pawns(game_state, self.max_player)
        for pawn in pawns:
            dist = 0 if self.__is_pawn_in_goal_area(pawn) else floor_euclidean_distance(pawn, self.target_cell)
            if dist != 0:
                return False
        return True
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        def __calc_dist_delta(move: Move):
            dist_to = 0 if self.__is_pawn_in_goal_area(move.move_to) else floor_euclidean_distance(move.move_to, self.target_cell)
            dist_from = 0 if self.__is_pawn_in_goal_area(move.move_from) else floor_euclidean_distance(move.move_from, self.target_cell)
            return dist_to - dist_from
        return sorted(children, key=lambda move: __calc_dist_delta(move))


class EndGameFillFromEnd(Strategy):

    def __init__(self, maximizing_player: bool):
        self.goal_cells_weights = const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MAX_PLAYER if maximizing_player else const.END_GAME_FILL_FROM_END_CELLS_WEIGHTS_MIN_PLAYER
        self.target_cell = (0,15) if maximizing_player else (15,0)
        self.outside_goal_area_penalty = const.END_GAME_FILL_FROM_END_OUTSIDE_AREA_PENALTY
        self.max_player = maximizing_player

    def __calculate_distance(self, pawn: tuple[int,int], max_player: bool) -> float:
        return self.goal_cells_weights[pawn] if pawn in self.goal_cells_weights else (floor_euclidean_distance(pawn, self.target_cell) + self.outside_goal_area_penalty)
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += self.__calculate_distance(pawn, self.max_player)
        return -dist_sum if self.max_player else dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return False
    
    def estimate_move_value(self, move: Move, max_player: bool) -> float:
        distance_delta = floor_euclidean_distance(move.move_to, self.target_cell) - floor_euclidean_distance(move.move_from, self.target_cell)
        pawn_in_base_bonus = (self.outside_goal_area_penalty - self.goal_cells_weights[move.move_to]) if move.move_to in self.goal_cells_weights else 0
        return distance_delta - pawn_in_base_bonus
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self.estimate_move_value(move, max_player))
    

class EndGameFillEveryOther(Strategy):

    def __init__(self, maximizing_player: bool):
        self.goal_cells_weights = const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MAX_PLAYER if maximizing_player else const.END_GAME_FILL_EVERY_OTHER_CELLS_WEIGHTS_MIN_PLAYER
        self.max_player = maximizing_player
        self.target_cell = (0,15) if maximizing_player else (15,0)
        self.penalty = const.END_GAME_FILL_EVERY_OTHER_PENALTY

    def _calculate_distance(self, pawn: tuple[int,int], max_player: bool) -> float:
        return self.goal_cells_weights[pawn] if pawn in self.goal_cells_weights else (floor_euclidean_distance(pawn, self.target_cell) + self.penalty)
    
    def evaluate(self, game_state: list[list[int]]) -> float:
        pawns = players_pawns(game_state, self.max_player)
        dist_sum = 0
        for pawn in pawns:
            dist_sum += self._calculate_distance(pawn, self.max_player)
        return -dist_sum if self.max_player else dist_sum
    
    def switch_strategy_check(self, game_state: list[list[int]], turn_number: int) -> bool:
        return False
    
    def estimate_move_value(self, move: Move, max_player: bool) -> float:
        distance_delta = floor_euclidean_distance(move.move_to, self.target_cell) - floor_euclidean_distance(move.move_from, self.target_cell)
        pawn_in_base_bonus = (self.penalty - self.goal_cells_weights[move.move_to]) if move.move_to in self.goal_cells_weights else 0
        return distance_delta - pawn_in_base_bonus
    
    def prepare_nodes_order(self, children: set[Move], max_player: bool) -> list[Move]:
        return sorted(children, key=lambda move: self.estimate_move_value(move, max_player))      


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
        PlayerStrategy.MIDDLE_GAME_CONTROL_PAWNS : MiddleGameControlPawns,
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
    
