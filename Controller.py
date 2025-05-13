from typing import Tuple
import pygame
from board import GomokuBoard
# from ai_minimax import AI_Minimax
# from ai_alphabeta import AI_Alphabeta


class GomokuGame:

    def __init__(self, board_size: int = 15, gui_enabled: bool = True):
        """
        Initialize the Gomoku game.

        Args:
            board_size: Size of the game board (board_size x board_size)
            gui_enabled: Whether to show the GUI or run in console mode
        """
        self.board = GomokuBoard(board_size)
        self.gui_enabled = gui_enabled

        # Initialize GUI if enabled
        if gui_enabled:
            # Initialize pygame
            pygame.init()

            # Constants
            self.CELL_SIZE = 40
            self.MARGIN = 50
            self.WIDTH = self.CELL_SIZE * board_size + 2 * self.MARGIN
            self.HEIGHT = self.CELL_SIZE * board_size + 2 * self.MARGIN

            # Colors
            self.BLACK = (0, 0, 0)
            self.WHITE = (255, 255, 255)
            self.BROWN = (205, 133, 63)
            self.RED = (255, 0, 0)
            self.BLUE = (0, 0, 255)

            # Create screen
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Gomoku")

            # Font
            self.font = pygame.font.SysFont('Arial', 20)

    def draw_board(self):
        self.screen.fill(self.BROWN)

        # Draw grid lines
        for i in range(self.board.size + 1):
            # Horizontal lines
            pygame.draw.line(
                self.screen, self.BLACK,
                (self.MARGIN, self.MARGIN + i * self.CELL_SIZE),
                (self.WIDTH - self.MARGIN, self.MARGIN + i * self.CELL_SIZE)
            )
            # Vertical lines
            pygame.draw.line(
                self.screen, self.BLACK,
                (self.MARGIN + i * self.CELL_SIZE, self.MARGIN),
                (self.MARGIN + i * self.CELL_SIZE, self.HEIGHT - self.MARGIN)
            )

        # Draw stones
        for r in range(self.board.size):
            for c in range(self.board.size):
                if self.board.board[r][c] == 1:
                    pygame.draw.circle(
                        self.screen, self.BLACK,
                        (self.MARGIN + c * self.CELL_SIZE, self.MARGIN + r * self.CELL_SIZE),
                        self.CELL_SIZE // 2 - 2
                    )
                elif self.board.board[r][c] == 2:
                    pygame.draw.circle(
                        self.screen, self.WHITE,
                        (self.MARGIN + c * self.CELL_SIZE, self.MARGIN + r * self.CELL_SIZE),
                        self.CELL_SIZE // 2 - 2
                    )

        # Highlight last move
        if self.board.last_move:
            r, c = self.board.last_move
            pygame.draw.circle(
                self.screen, self.RED,
                (self.MARGIN + c * self.CELL_SIZE, self.MARGIN + r * self.CELL_SIZE),
                self.CELL_SIZE // 2 - 6, 2
            )

        # Display game status
        status_text = f"Player {self.board.current_player}'s turn"
        if self.board.game_over:
            if self.board.winner:
                status_text = f"Player {self.board.winner} wins!"
            else:
                status_text = "Draw!"

        text_surface = self.font.render(status_text, True, self.BLACK)
        self.screen.blit(text_surface, (10, 10))

        pygame.display.flip()

    def get_cell_from_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """
        Convert screen position to board cell coordinates.

        Args:
            pos: (x, y) screen position

        Returns:
            (row, col) board cell coordinates
        """
        x, y = pos

        # Check if click is outside the board
        if (x < self.MARGIN - self.CELL_SIZE // 2 or
                x > self.WIDTH - self.MARGIN + self.CELL_SIZE // 2 or
                y < self.MARGIN - self.CELL_SIZE // 2 or
                y > self.HEIGHT - self.MARGIN + self.CELL_SIZE // 2):
            return None

        col = round((x - self.MARGIN) / self.CELL_SIZE)
        row = round((y - self.MARGIN) / self.CELL_SIZE)

        # Ensure coordinates are within board boundaries
        if 0 <= row < self.board.size and 0 <= col < self.board.size:
            return (row, col)

        return None

    def human_vs_ai(self, ai_algorithm: str = "minimax", ai_depth: int = 3, ai_player: int = 2):
        """
        Play a Human vs AI game.

        Args:
            ai_algorithm: "minimax" or "alphabeta"
            ai_depth: AI search depth
            ai_player: Which player the AI controls (1 or 2)
        """
        ai = GomokuAI(ai_player, ai_algorithm, ai_depth)

        # If AI is player 1, make initial move
        if ai_player == 1 and not self.board.game_over:
            row, col = ai.get_move(self.board)
            self.board.make_move(row, col)

        if self.gui_enabled:
            self.draw_board()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN and not self.board.game_over:
                        if self.board.current_player != ai_player:  # Human's turn
                            pos = pygame.mouse.get_pos()
                            cell = self.get_cell_from_pos(pos)

                            if cell and self.board.is_valid_move(*cell):
                                row, col = cell
                                self.board.make_move(row, col)
                                self.draw_board()

                                # If game not over, AI makes its move
                                if not self.board.game_over:
                                    pygame.display.flip()  # Update display before AI thinks
                                    row, col = ai.get_move(self.board)
                                    self.board.make_move(row, col)
                                    self.draw_board()

                pygame.time.wait(100)  # Small delay to reduce CPU usage

            pygame.quit()
        else:
            # Console-based play
            while not self.board.game_over:
                self.board.print_board()

                if self.board.current_player != ai_player:  # Human's turn
                    while True:
                        try:
                            row = int(input(f"Player {self.board.current_player}, enter row: "))
                            col = int(input(f"Player {self.board.current_player}, enter column: "))

                            if self.board.is_valid_move(row, col):
                                self.board.make_move(row, col)
                                break
                            else:
                                print("Invalid move, try again.")
                        except ValueError:
                            print("Please enter valid numbers.")
                else:  # AI's turn
                    print(f"AI (Player {ai_player}) is thinking...")
                    row, col = ai.get_move(self.board)
                    self.board.make_move(row, col)
                    print(f"AI played at ({row}, {col})")

            # Game over
            self.board.print_board()
            if self.board.winner:
                print(f"Player {self.board.winner} wins!")
            else:
                print("Draw!")

    def ai_vs_ai(self, ai1_algorithm: str = "minimax", ai2_algorithm: str = "alphabeta",
                 ai1_depth: int = 3, ai2_depth: int = 3, max_moves: int = 100):
        """
        Play an AI vs AI game.

        Args:
            ai1_algorithm: Algorithm for player 1 ("minimax" or "alphabeta")
            ai2_algorithm: Algorithm for player 2 ("minimax" or "alphabeta")
            ai1_depth: Search depth for player 1
            ai2_depth: Search depth for player 2
            max_moves: Maximum number of moves to prevent infinite games
        """
        ai1 = GomokuAI(1, ai1_algorithm, ai1_depth)
        ai2 = GomokuAI(2, ai2_algorithm, ai2_depth)

        move_count = 0

        print(f"AI1: {ai1_algorithm} (depth {ai1_depth}) vs AI2: {ai2_algorithm} (depth {ai2_depth})")

        if self.gui_enabled:
            self.draw_board()
            running = True

            while running and not self.board.game_over and move_count < max_moves:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        return

                # Current AI makes a move
                current_ai = ai1 if self.board.current_player == 1 else ai2
                print(f"AI Player {self.board.current_player} ({current_ai.algorithm}) is thinking...")

                pygame.display.flip()  # Update display before AI thinks
                row, col = current_ai.get_move(self.board)
                self.board.make_move(row, col)
                move_count += 1

                self.draw_board()
                pygame.time.wait(500)  # Pause for visualization

            # Game over
            if move_count >= max_moves:
                print("Game reached maximum move limit.")

            if self.board.winner:
                algorithm = ai1_algorithm if self.board.winner == 1 else ai2_algorithm
                print(f"Player {self.board.winner} ({algorithm}) wins!")
            elif self.board.game_over:
                print("Draw!")

            pygame.quit()
        else:
            # Console-based play
            while not self.board.game_over and move_count < max_moves:
                self.board.print_board()

                # Current AI makes a move
                current_ai = ai1 if self.board.current_player == 1 else ai2
                print(f"AI Player {self.board.current_player} ({current_ai.algorithm}) is thinking...")

                row, col = current_ai.get_move(self.board)
                self.board.make_move(row, col)
                move_count += 1

                print(f"AI Player {3 - self.board.current_player} played at ({row}, {col})")

            # Game over
            self.board.print_board()

            if move_count >= max_moves:
                print("Game reached maximum move limit.")

            if self.board.winner:
                algorithm = ai1_algorithm if self.board.winner == 1 else ai2_algorithm
                print(f"Player {self.board.winner} ({algorithm}) wins!")
            elif self.board.game_over:
                print("Draw!")