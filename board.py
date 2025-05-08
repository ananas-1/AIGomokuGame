# board.py

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def display(self):
        print("\n  " + " ".join(f"{i:2}" for i in range(self.size)))
        for idx, row in enumerate(self.board):
            print(f"{idx:2} " + "  ".join(row))
        print()

    def place_move(self, row, col, symbol):
        if self.is_valid_move(row, col):
            self.board[row][col] = symbol
            return True
        return False

    def is_valid_move(self, row, col):
        return (0 <= row < self.size and
                0 <= col < self.size and
                self.board[row][col] == '.')

    def is_full(self):
        return all(cell != '.' for row in self.board for cell in row)

    def check_win(self, symbol):
        for row in range(self.size):
            for col in range(self.size):
                if self.check_five(row, col, symbol):
                    return True
        return False

    def check_five(self, row, col, symbol):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(5):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                    count += 1
                else:
                    break
            if count == 5:
                return True
        return False

    def get_empty_cells(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == '.']

    def clone(self):
        new_board = Board(self.size)
        new_board.board = [row[:] for row in self.board]
        return new_board
