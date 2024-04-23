
class Halma:
    def __init__(self, game_state: list[list[int]], player_who_starts: int = 1):
        self.game_state = game_state
        self.player_turn = player_who_starts
        self.board_size = 16
        self.turn_number = 1

    def players_pawns(self):
        pawn_positions:list[tuple[int,int]] = []
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.game_state[i][j]==self.player_turn:
                    pawn_positions.append((i,j))
        return pawn_positions
    
    def generate_step_moves(self, pawn_pos: tuple[int,int]):
        """
            Function to generate valid step moves for the pawn. Step move is a move
            onto the neighbour cell without jumping, for example: (3,4) -> (3,5).
        """
        step_moves = []
        i_offsets = [-1, 0, 1]
        j_offsets = [-1, 0, 1]
        for i in i_offsets:
            for j in j_offsets:
                if (pawn_pos[0] + i in range (0, self.board_size) and
                    pawn_pos[1] + j in range (0, self.board_size) and
                    self.game_state[pawn_pos[0] + i][pawn_pos[1] + j] == 0):
                    step_moves.append((pawn_pos[0] + i, pawn_pos[1] + j))
        return step_moves
    
    def generate_possible_jumps(self, pawn_pos: tuple[int, int]):
        """
            Function to generate possible jumps for the pawn from a certain position.
            It checks all 8 directions - if the first cell in that direction is empty
            and the second one is free, then this second cell as the ending (landing)
            one is considered a valid jump opportunity.
        """
        jump_moves = []
        i_offsets = [-1, 0, 1]
        j_offsets = [-1, 0, 1]
        for i in i_offsets:
            for j in j_offsets:
                if (pawn_pos[0] + i in range (0, self.board_size) and
                    pawn_pos[1] + j in range (0, self.board_size) and
                    pawn_pos[0] + (2 * i) in range (0, self.board_size) and
                    pawn_pos[1] + (2 * j) in range (0, self.board_size) and
                    self.game_state[pawn_pos[0] + i][pawn_pos[1] + j] != 0 and
                    self.game_state[pawn_pos[0] + (2 * i)][pawn_pos[1] + (2 * j)] == 0):
                    jump_moves.append((pawn_pos[0] + (2 * i), pawn_pos[1] + (2 * j)))
        return jump_moves
    
    def generate_jump_moves(self, pawn_pos: tuple[int,int], tabu_pos: set[tuple[int,int]]):
        """
            This function takes all possible jumps from a specific position and recursively
            checks if it's possible to continue such a jump (to perform multi-jump). It returns
            all positions of the cells that are achievable by jumping from the original pawn position.
        """
        possible_jumps = self.generate_possible_jumps(pawn_pos)
        
        moves = []
        tabu_pos.add(pawn_pos)
        for jump_pos in possible_jumps:
            if jump_pos not in tabu_pos:
                moves += [jump_pos] + self.generate_jump_moves(jump_pos, tabu_pos)
        return moves

    
    def generate_valid_moves(self, pawn_pos: tuple[int,int]):
        step_moves = self.generate_step_moves(pawn_pos)
        jump_moves = self.generate_jump_moves(pawn_pos, tabu_pos=set())
        return step_moves + jump_moves

    @staticmethod
    def check_corner_for_win(game_state: list[list[int]], bottom_corner: bool):
        corner_cells_offsets = {
            0 : [0, 1, 2, 3, 4],
            1 : [0, 1, 2, 3, 4],
            2 : [0, 1, 2, 3],
            3 : [0, 1, 2],
            4 : [0, 1]
        }
        base_cell = (15,0) if bottom_corner else [0,15]
        cell_mark = game_state[base_cell[0]][base_cell[1]]
        for row_offset, col_offsets in corner_cells_offsets.items():
            for col_offset in col_offsets:
                if bottom_corner:
                    nex_cell_i = base_cell[0] - row_offset
                    nex_cell_j = base_cell[1] + col_offset
                else:
                    nex_cell_i = base_cell[0] + row_offset
                    nex_cell_j = base_cell[1] - col_offset
                if game_state[nex_cell_i][nex_cell_j] != cell_mark:
                    return 0
        return cell_mark

    @staticmethod
    def check_board_for_win(game_state: list[list[int]]):
        bottom_corner_check = Halma.check_corner_for_win(game_state, True)
        top_corner_check = Halma.check_corner_for_win(game_state, False)
        if bottom_corner_check == 0 and top_corner_check == 0:
            return 0
        if bottom_corner_check != 0:
            return bottom_corner_check
        return top_corner_check
        

# if __name__=='__main__':
#     print('Game state:')
#     line = input().split(' ')
#     print(line)
#     print(type(line))