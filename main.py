# main.py

from board import Board
from player import HumanPlayer, MinimaxAIPlayer, AlphaBetaAIPlayer


def choose_mode():
    print("Welcome to Gomoku AI Game Solver!")
    print("Choose a game mode:")
    print("1. Human vs AI (Minimax)")
    print("2. AI vs AI (Minimax vs Alpha-Beta)")
    choice = input("Enter 1 or 2: ")
    while choice not in ["1", "2"]:
        choice = input("Invalid choice. Please enter 1 or 2: ")
    return int(choice)


def play_game(player1, player2):
    board = Board(BOARD_SIZE)
    current_player = player1

    while not board.is_full():
        board.display()
        print(f"{current_player.name}'s turn ({current_player.symbol})")
        move = current_player.get_move(board)
        if board.place_move(move[0], move[1], current_player.symbol):
            if board.check_win(current_player.symbol):
                board.display()
                print(f"\n🎉 {current_player.name} ({current_player.symbol}) wins!")
                return
            # Switch turns
            current_player = player1 if current_player == player2 else player2
        else:
            print("Invalid move. Try again.")

    board.display()
    print("It's a draw!")


def main():
    mode = choose_mode()

    if mode == 1:
        player1 = HumanPlayer("Human", "X")
        player2 = MinimaxAIPlayer("AI-Minimax", "O", DEPTH_LIMIT)
    else:
        player1 = MinimaxAIPlayer("AI-Minimax", "X", DEPTH_LIMIT)
        player2 = AlphaBetaAIPlayer("AI-AlphaBeta", "O", DEPTH_LIMIT)

    play_game(player1, player2)


if __name__ == "__main__":
    main()
