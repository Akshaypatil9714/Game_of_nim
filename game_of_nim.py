from games import *
import random

class GameOfNim(Game):
    def __init__(self, board):
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=self.get_valid_moves(board))

    def get_valid_moves(self, board):
        valid_moves = []
        for row, count in enumerate(board):
            for num in range(1, count+1):
                valid_moves.append((row, num))
        return valid_moves

    
    def result(self, state, move):
        if move not in state.moves:
            return state   # Illegal move has no effect
        board = state.board.copy()
        row, num = move
        board[row] -= num
        #moves = list(state.moves)
        #moves.remove(move)
        moves = [(r, c) for r, c in state.moves if r != row or c < num]
        return GameState(to_move=('MIN' if state.to_move == 'MAX' else 'MAX'),
                     utility=self.compute_utility(board, state.to_move, moves),
                     board=board, moves=self.get_valid_moves(board))

    
    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves
    
    def utility(self, state, player):
        if state.utility != 0:
            return state.utility if player == 'MAX' else -state.utility
        else:
            return 0

    
    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    
    def compute_utility(self, board, player, moves):
        """If 'MAX' wins with this move, return 1; if 'MIN' wins return -1; else return 0."""
        if self.terminal_test(GameState(board=board, to_move='MAX', utility=0, moves=moves)):
            return +1 if player == 'MAX' else -1
        else:
            return 0

                    
    def play_game(self, *players):
        state = self.initial
        mapping = {'MAX': 0, 'MIN': 1}
        while True:
            player = mapping[state.to_move]
            print("Current player:", state.to_move)
            if self.terminal_test(state):
                return self.utility(state, self.to_move(self.initial))
            move = players[player](self, state)
            state = self.result(state, move)
            print("Move:", move)
            print("Resulting state:")
            print("board:", state.board)
            
        
if __name__ == "__main__":
    #nim = GameOfNim(board=[0, 5, 3, 1]) # Creating the game instance
    nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [0, 5, 3, 1]
    print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2,1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1,3) ))
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first
    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")
