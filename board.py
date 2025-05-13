from typing import List, Tuple
import numpy as np


class GomokuBoard:
    """Represents the Gomoku game board and game state."""

    def __init__(self, size: int = 15):
        """
        Initialize the Gomoku board with the specified size.

        Args:
            size: The size of the board (size x size)
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # 0: empty, 1: player 1, 2: player 2
        self.current_player = 1  # Player 1 starts
        self.last_move = None
        self.winner = None
        self.game_over = False

    def reset(self):
        """Reset the game board to its initial state."""
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = 1
        self.last_move = None
        self.winner = None
        self.game_over = False

    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid (within bounds and on an empty cell).

        Args:
            row: Row index of the move
            col: Column index of the move

        Returns:
            True if the move is valid, False otherwise
        """
        return (0 <= row < self.size and
                0 <= col < self.size and
                self.board[row][col] == 0)

    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board for the current player.

        Args:
            row: Row index of the move
            col: Column index of the move

        Returns:
            True if the move was successful, False otherwise
        """
        if self.game_over or not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.current_player
        self.last_move = (row, col)

        # Check if the current player has won
        if self.check_win(row, col):
            self.winner = self.current_player
            self.game_over = True
        # Check if the board is full (draw)
        elif np.count_nonzero(self.board) == self.size * self.size:
            self.winner = 0
            self.game_over = True
        else:
            # Switch player
            self.current_player = 3 - self.current_player  # Toggle between 1 and 2

        return True

    def check_win(self, row: int, col: int) -> bool:
        """
        Check if the current player has won after making a move at (row, col).

        Args:
            row: Row index of the last move
            col: Column index of the last move

        Returns:
            True if the current player has won, False otherwise
        """
        player = self.board[row][col]
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonal \
            [(1, -1), (-1, 1)]  # Diagonal /
        ]

        for dir_pair in directions:
            count = 1  # Count the current stone

            # Check both directions
            for dr, dc in dir_pair:
                r, c = row, col

                # Count consecutive stones in this direction
                for _ in range(4):  # We need 5 in a row, already counted 1
                    r, c = r + dr, c + dc
                    if (0 <= r < self.size and
                            0 <= c < self.size and
                            self.board[r][c] == player):
                        count += 1
                    else:
                        break

            if count >= 5:
                return True

        return False

    def get_available_moves(self) -> List[Tuple[int, int]]:
        """
        Get all available (empty) cells on the board.

        Returns:
            List of (row, col) tuples representing available moves
        """
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.board[r][c] == 0]

    def get_neighbor_moves(self, distance: int = 1) -> List[Tuple[int, int]]:
        """
        Get available cells that are neighbors to existing stones.

        Args:
            distance: Maximum Manhattan distance to consider as neighbor

        Returns:
            List of (row, col) tuples representing available neighbor moves
        """
        # If board is empty, return center
        if np.count_nonzero(self.board) == 0:
            center = self.size // 2
            return [(center, center)]

        neighbors = set()
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] != 0:  # If there's a stone here
                    # Check neighbors within specified distance
                    for dr in range(-distance, distance + 1):
                        for dc in range(-distance, distance + 1):
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < self.size and
                                    0 <= nc < self.size and
                                    self.board[nr][nc] == 0):
                                neighbors.add((nr, nc))

        return list(neighbors) if neighbors else self.get_available_moves()

    def print_board(self):
        """Print the current state of the board to the console."""
        symbols = {0: '.', 1: 'X', 2: 'O'}

        print("   " + " ".join(f"{i:2d}" for i in range(self.size)))
        print("  +" + "---" * self.size + "+")

        for r in range(self.size):
            print(f"{r:2d}|", end=" ")
            for c in range(self.size):
                print(symbols[self.board[r][c]], end="  ")
            print("|")

        print("  +" + "---" * self.size + "+")