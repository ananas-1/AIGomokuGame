# minimax.py
from evaluate import evaluate_pattern
from typing import Tuple, Optional
import numpy as np
import board as GomokuBoard



def evaluate_board(board: 'GomokuBoard', player: int) -> int:
    """
    Evaluate the board from the perspective of `player`.

    Returns:
        An integer score: higher is better for `player`
    """
    opponent = 3 - player
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for r in range(board.size):
        for c in range(board.size):
            if board.board[r][c] == player:
                for dr, dc in directions:
                    score += evaluate_pattern(board, r, c, dr, dc, player)
            elif board.board[r][c] == opponent:
                for dr, dc in directions:
                    score -= evaluate_pattern(board, r, c, dr, dc, opponent)

    return score



def minimax(board: 'GomokuBoard', depth: int, maximizing: bool, player: int) -> Tuple[int, Optional[Tuple[int, int]]]:
    """
    Minimax search

    Args:
        board: GomokuBoard instance
        depth: How deep to search
        maximizing: Whether it's the maximizing player's turn
        player: The AI's player number (1 or 2)

    Returns:
        A tuple of (score, best_move)
    """
    opponent = 3 - player

    if depth == 0 or board.game_over:
        return evaluate_board(board, player), None

    best_move = None
    moves = board.get_neighbor_moves(distance=1)

    if maximizing:
        max_eval = float('-inf')
        for move in moves:
            r, c = move
            new_board = copy_board(board)
            new_board.make_move(r, c)
            eval_score, _ = minimax(new_board, depth - 1, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            r, c = move
            new_board = copy_board(board)
            new_board.make_move(r, c)
            eval_score, _ = minimax(new_board, depth - 1, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def copy_board(original_board: 'GomokuBoard') -> 'GomokuBoard':
    """Create a copy of the board to simulate a move."""
    from copy import deepcopy
    clone = GomokuBoard(original_board.size)
    clone.board = np.copy(original_board.board)
    clone.current_player = original_board.current_player
    clone.last_move = original_board.last_move
    clone.winner = original_board.winner
    clone.game_over = original_board.game_over
    return clone
