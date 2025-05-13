import numpy as np
import time
import pygame
import sys
from typing import Tuple, List, Optional
from board import GomokuBoard

class GomokuAI:
    """AI player for Gomoku using Minimax and Alpha-Beta pruning algorithms."""
    
    def __init__(self, player_number: int, algorithm: str = "minimax", max_depth: int = 3):
        """
        Initialize the AI player.
        
        Args:
            player_number: 1 for the first player, 2 for the second player
            algorithm: "minimax" or "alphabeta" - the search algorithm to use
            max_depth: Maximum search depth for the algorithm
        """
        self.player = player_number
        self.opponent = 3 - player_number  # 1 if player is 2, 2 if player is 1
        self.algorithm = algorithm.lower()
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def get_move(self, board: GomokuBoard) -> Tuple[int, int]:
        """
        Determine the best move for the AI player.
        
        Args:
            board: The current game board
            
        Returns:
            A tuple (row, col) representing the AI's chosen move
        """
        self.nodes_evaluated = 0
        start_time = time.time()
        
        # Get potential moves (neighbors of existing stones)
        possible_moves = board.get_neighbor_moves(2)
        
        if not possible_moves:
            center = board.size // 2
            return (center, center)
        
        best_score = float('-inf')
        best_move = possible_moves[0]
        
        # Apply chosen algorithm to find the best move
        if self.algorithm == "minimax":
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.player
                    
                    # Evaluate this move
                    score = self.minimax(board, self.max_depth, False)
                    
                    # Undo the move
                    board.board[row][col] = 0
                    
                    # Update best move if needed
                    if score > best_score:
                        best_score = score
                        best_move = move
        
        elif self.algorithm == "alphabeta":
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.player
                    
                    # Evaluate this move with alpha-beta pruning
                    score = self.alpha_beta(board, self.max_depth, float('-inf'), float('inf'), False)
                    
                    # Undo the move
                    board.board[row][col] = 0
                    
                    # Update best move if needed
                    if score > best_score:
                        best_score = score
                        best_move = move
        
        elapsed_time = time.time() - start_time
        print(f"AI {self.algorithm} (player {self.player}) chose move {best_move}")
        print(f"Nodes evaluated: {self.nodes_evaluated}, Time: {elapsed_time:.2f}s")
        
        return best_move

    def minimax(self, board: GomokuBoard, depth: int, is_maximizing: bool) -> float:
        """
        Minimax algorithm implementation.
        
        Args:
            board: The current game board
            depth: Current search depth
            is_maximizing: True if maximizing player's turn, False otherwise
            
        Returns:
            The score of the best move
        """
        self.nodes_evaluated += 1
        
        # Check terminal states
        if self.is_terminal(board) or depth == 0:
            return self.evaluate(board)
        
        # Get potential moves
        possible_moves = board.get_neighbor_moves(2)
        
        if is_maximizing:
            max_score = float('-inf')
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.player
                    score = self.minimax(board, depth - 1, False)
                    board.board[row][col] = 0  # Undo the move
                    max_score = max(max_score, score)
            return max_score
        else:
            min_score = float('inf')
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.opponent
                    score = self.minimax(board, depth - 1, True)
                    board.board[row][col] = 0  # Undo the move
                    min_score = min(min_score, score)
            return min_score

    
    def alpha_beta(self, board: GomokuBoard, depth: int, alpha: float, beta: float, 
                   is_maximizing: bool) -> float:
        """
        Alpha-Beta pruning algorithm implementation.
        
        Args:
            board: The current game board
            depth: Current search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player's turn, False otherwise
            
        Returns:
            The score of the best move
        """
        self.nodes_evaluated += 1
        
        # Check terminal states
        if self.is_terminal(board) or depth == 0:
            return self.evaluate(board)
        
        # Get potential moves
        possible_moves = board.get_neighbor_moves(2)
        
        if is_maximizing:
            value = float('-inf')
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.player
                    value = max(value, self.alpha_beta(board, depth - 1, alpha, beta, False))
                    board.board[row][col] = 0  # Undo the move
                    
                    # Pruning
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break  # Beta cutoff
            return value
        else:
            value = float('inf')
            for move in possible_moves:
                row, col = move
                # Try this move
                if board.is_valid_move(row, col):
                    board.board[row][col] = self.opponent
                    value = min(value, self.alpha_beta(board, depth - 1, alpha, beta, True))
                    board.board[row][col] = 0  # Undo the move
                    
                    # Pruning
                    beta = min(beta, value)
                    if beta <= alpha:
                        break  # Alpha cutoff
            return value
    
    def is_terminal(self, board: GomokuBoard) -> bool:
        """
        Check if the current board state is terminal (game over).
        
        Args:
            board: The current game board
            
        Returns:
            True if the game is over, False otherwise
        """
        # Check for win conditions based on the last move
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != 0:
                    player = board.board[r][c]
                    # Check horizontal, vertical, and diagonal wins
                    directions = [
                        [(0, 1), (0, -1)],   # Horizontal
                        [(1, 0), (-1, 0)],   # Vertical
                        [(1, 1), (-1, -1)],  # Diagonal \
                        [(1, -1), (-1, 1)]   # Diagonal /
                    ]
                    
                    for dir_pair in directions:
                        count = 1  # Count the current stone
                        
                        # Check both directions
                        for dr, dc in dir_pair:
                            r1, c1 = r, c
                            
                            # Count consecutive stones in this direction
                            for _ in range(4):  # We need 5 in a row, already counted 1
                                r1, c1 = r1 + dr, c1 + dc
                                if (0 <= r1 < board.size and 
                                    0 <= c1 < board.size and 
                                    board.board[r1][c1] == player):
                                    count += 1
                                else:
                                    break
                        
                        if count >= 5:
                            return True
                    
        # Check if the board is full
        return np.count_nonzero(board.board) == board.size * board.size
    
    def evaluate(self, board: GomokuBoard) -> float:
        """
        Evaluate the current board state for the AI player.
        
        This function assigns a score to the current board state based on various patterns.
        Positive scores favor the AI player, negative scores favor the opponent.
        
        Args:
            board: The current game board
            
        Returns:
            A score representing how favorable the board is for the AI player
        """
        score = 0
        
        # Check if game is over
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != 0:
                    player = board.board[r][c]
                    # Check horizontal, vertical, and diagonal wins
                    directions = [
                        [(0, 1)],   # Horizontal
                        [(1, 0)],   # Vertical
                        [(1, 1)],   # Diagonal \
                        [(1, -1)]   # Diagonal /
                    ]
                    
                    for direction in directions:
                        for dr, dc in direction:
                            # Pattern scores
                            pattern_score = self.evaluate_pattern(board, r, c, dr, dc, player)
                            
                            # Add to total score (positive for AI, negative for opponent)
                            if player == self.player:
                                score += pattern_score
                            else:
                                score -= pattern_score
        
        return score
    
    def evaluate_pattern(self, board: GomokuBoard, r: int, c: int, dr: int, dc: int, player: int) -> int:
        """
        Evaluate a pattern in a specific direction from a position.
        
        Args:
            board: The current game board
            r, c: Starting position
            dr, dc: Direction
            player: Player to check for (1 or 2)
            
        Returns:
            Score for the pattern
        """
        consecutive = 1  # Count the starting stone
        open_ends = 0    # Number of open ends
        
        # Check forward direction
        r1, c1 = r + dr, c + dc
        while (0 <= r1 < board.size and 
               0 <= c1 < board.size and 
               board.board[r1][c1] == player):
            consecutive += 1
            r1, c1 = r1 + dr, c1 + dc
        
        # Check if this end is open
        if (0 <= r1 < board.size and 
            0 <= c1 < board.size and 
            board.board[r1][c1] == 0):
            open_ends += 1
        
        # Check backward direction
        r1, c1 = r - dr, c - dc
        while (0 <= r1 < board.size and 
               0 <= c1 < board.size and 
               board.board[r1][c1] == player):
            consecutive += 1
            r1, c1 = r1 - dr, c1 - dc
        
        # Check if this end is open
        if (0 <= r1 < board.size and 
            0 <= c1 < board.size and 
            board.board[r1][c1] == 0):
            open_ends += 1
        
        # Assign scores based on pattern
        if consecutive >= 5:
            return 10000  # Win condition
        elif consecutive == 4:
            if open_ends == 2:
                return 5000  # Open four (will lead to win)
            elif open_ends == 1:
                return 500   # Four with one open end
        elif consecutive == 3:
            if open_ends == 2:
                return 200   # Open three
            elif open_ends == 1:
                return 50    # Three with one open end
        elif consecutive == 2:
            if open_ends == 2:
                return 10    # Open two
            elif open_ends == 1:
                return 5     # Two with one open end
        elif consecutive == 1:
            if open_ends > 0:
                return 1     # Single stone with open end(s)
        
        return 0  # Default score

