# minimax.py

# from config import DEPTH_LIMIT

def evaluate(board, symbol):
    # Simplified evaluation: +1 for center control, +10 for potential lines
    # You can improve this with more heuristics later
    center = board.size // 2
    score = 0
    for r in range(board.size):
        for c in range(board.size):
            if board.board[r][c] == symbol:
                score += 1
                if r == center and c == center:
                    score += 2
    return score

def minimax(board, depth, maximizing, symbol, opponent_symbol):
    if depth == 0 or board.is_full() or board.check_win(symbol) or board.check_win(opponent_symbol):
        return evaluate(board, symbol), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.get_empty_cells():
            new_board = board.clone()
            new_board.place_move(move[0], move[1], symbol)
            eval, _ = minimax(new_board, depth - 1, False, symbol, opponent_symbol)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.get_empty_cells():
            new_board = board.clone()
            new_board.place_move(move[0], move[1], opponent_symbol)
            eval, _ = minimax(new_board, depth - 1, True, symbol, opponent_symbol)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move
