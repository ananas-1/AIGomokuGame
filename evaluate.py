import board as GomokuBoard

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
    open_ends = 0  # Number of open ends

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
            return 500  # Four with one open end
    elif consecutive == 3:
        if open_ends == 2:
            return 200  # Open three
        elif open_ends == 1:
            return 50  # Three with one open end
    elif consecutive == 2:
        if open_ends == 2:
            return 10  # Open two
        elif open_ends == 1:
            return 5  # Two with one open end
    elif consecutive == 1:
        if open_ends > 0:
            return 1  # Single stone with open end(s)

    return 0  # Default score