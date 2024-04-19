# from dataclasses import dataclass

# @dataclass
# class Cell:
#     x: int
#     y: int

class Halma:
    def __init__(self, game_state: list[list[int]], player_who_starts: int = 1):
        self.game_state = game_state
        self.player_turn = player_who_starts
        self.board_size = 16
        self.turn_number = 1

    def players_pawns(self):
        pawn_positions:list[tuple[int,int]] = []
        for i in self.game_state:
            for j in self.game_state[i]:
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
                if (pawn_pos[0] + i in range (0, self.board_size + 1) and
                    pawn_pos[1] + j in range (0, self.board_size + 1) and
                    self.game_state[pawn_pos[0] + i][pawn_pos[1] + j] == 0):
                    step_moves.append((pawn_pos[0] + i, pawn_pos[1] + j))
        return step_moves
    
    def generate_possible_jumps(self, pawn_pos: tuple[int, int]):
        jump_moves = []
        i_offsets = [-1, 0, 1]
        j_offsets = [-1, 0, 1]
        for i in i_offsets:
            for j in j_offsets:
                if (pawn_pos[0] + i in range (0, self.board_size + 1) and
                    pawn_pos[1] + j in range (0, self.board_size + 1) and
                    pawn_pos[0] + (2 * i) in range (0, self.board_size + 1) and
                    pawn_pos[1] + (2 * j) in range (0, self.board_size + 1) and
                    self.game_state[pawn_pos[0] + i][pawn_pos[1] + j] != 0 and
                    self.game_state[pawn_pos[0] + (2 * i)][pawn_pos[1] + (2 * j)] == 0):
                    jump_moves.append((pawn_pos[0] + (2 * i), pawn_pos[1] + (2 * j)))
        return jump_moves
    
    def generate_jump_moves(self, pawn_pos: tuple[int,int], tabu_pos: set[tuple[int,int]]):
        possible_jumps = self.generate_possible_jumps(pawn_pos)
        
        moves = []
        for jump_pos in possible_jumps:
            if jump_pos not in tabu_pos:
                moves += [jump_pos] + self.generate_jump_moves(jump_pos, tabu_pos.add(jump_pos))
        return moves

    
    def generate_valid_moves(self, pawn_pos: tuple[int,int]):
        step_moves = self.generate_step_moves(pawn_pos)
        jump_moves = self.generate_jump_moves(pawn_pos, tabu_pos=set())
        return step_moves + jump_moves
        

# if __name__=='__main__':
#     print('Game state:')
#     line = input().split(' ')
#     print(line)
#     print(type(line))