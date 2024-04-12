
class Halma:
    def __init__(self, game_state: list[list[int]], player_who_starts: int = 1):
        self.game_state = game_state
        self.player_turn = player_who_starts
        self.turn_number = 1
    
    # def generate_valid_moves(self):


# if __name__=='__main__':
#     print('Game state:')
#     line = input().split(' ')
#     print(line)
#     print(type(line))