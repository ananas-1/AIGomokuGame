# player.py

from minmax import minimax
from alphaBeta import alphabeta

class HumanPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self, board):
        while True:
            try:
                coords = input("Enter your move (row col): ").split()
                row, col = int(coords[0]), int(coords[1])
                if board.is_valid_move(row, col):
                    return (row, col)
                else:
                    print("Invalid move. Cell is already occupied or out of range.")
            except (IndexError, ValueError):
                print("Invalid input. Please enter two integers.")

class MinimaxAIPlayer:
    def __init__(self, name, symbol, depth):
        self.name = name
        self.symbol = symbol
        self.depth = depth

    def get_move(self, board):
        _, move = minimax(board, self.depth, True, self.symbol, 'O' if self.symbol == 'X' else 'X')
        print(f"{self.name} chooses move: {move}")
        return move

class AlphaBetaAIPlayer:
    def __init__(self, name, symbol, depth):
        self.name = name
        self.symbol = symbol
        self.depth = depth

    def get_move(self, board):
        _, move = alphabeta(board, self.depth, float('-inf'), float('inf'), True, self.symbol, 'O' if self.symbol == 'X' else 'X')
        print(f"{self.name} chooses move: {move}")
        return move
