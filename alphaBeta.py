# alphabeta.py

# from config import DEPTH_LIMIT
from minmax import evaluate  # Use the same evaluation function

def alphabeta(board, depth, alpha, beta, maximizing, symbol, opponent_symbol):
    if depth == 0 or board.is_full() or board.check_win(symbol) or board.check_win(opponent_symbol):
        return evaluate(board, symbol), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.get_empty_cells():
            new_board = board.clone()
            new_board.place_move(move[0], move[1], symbol)
            eval, _ = alphabeta(new_board, depth - 1, alpha, beta, False, symbol, opponent_symbol)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.get_empty_cells():
            new_board = board.clone()
            new_board.place_move(move[0], move[1], opponent_symbol)
            eval, _ = alphabeta(new_board, depth - 1, alpha, beta, True, symbol, opponent_symbol)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_move
