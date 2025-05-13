import numpy as np
import time
import pygame
import sys
from typing import Tuple, List, Optional
from board import GomokuBoard
from player import GomokuAI
from Controller import GomokuGame

def main():
    """Main function to run the Gomoku game."""
    print("Welcome to Gomoku!")
    print("Select game mode:")
    print("1. Human vs AI")
    print("2. AI vs AI")
    
    try:
        mode = int(input("Enter mode (1 or 2): "))
        board_size = int(input("Enter board size (15 recommended): "))
        use_gui = input("Use GUI? (y/n): ").lower() == 'y'
        
        game = GomokuGame(board_size, use_gui)
        
        if mode == 1:  # Human vs AI
            print("AI Algorithm options:")
            print("1. Minimax")
            print("2. Alpha-Beta Pruning")
            
            ai_algo_choice = int(input("Choose AI algorithm (1 or 2): "))
            ai_algorithm = "minimax" if ai_algo_choice == 1 else "alphabeta"
            
            ai_depth = int(input("Enter AI search depth (3 recommended): "))
            ai_player = int(input("AI plays as player (1 or 2): "))
            
            game.human_vs_ai(ai_algorithm, ai_depth, ai_player)
            
        elif mode == 2:  # AI vs AI
            print("AI1 (Player 1) Algorithm options:")
            print("1. Minimax")
            print("2. Alpha-Beta Pruning")
            
            ai1_algo_choice = int(input("Choose AI1 algorithm (1 or 2): "))
            ai1_algorithm = "minimax" if ai1_algo_choice == 1 else "alphabeta"
            ai1_depth = int(input("Enter AI1 search depth (3 recommended): "))
            
            print("AI2 (Player 2) Algorithm options:")
            print("1. Minimax")
            print("2. Alpha-Beta Pruning")
            
            ai2_algo_choice = int(input("Choose AI2 algorithm (1 or 2): "))
            ai2_algorithm = "minimax" if ai2_algo_choice == 1 else "alphabeta"
            ai2_depth = int(input("Enter AI2 search depth (3 recommended): "))
            
            max_moves = int(input("Enter maximum number of moves (100 recommended): "))
            
            game.ai_vs_ai(ai1_algorithm, ai2_algorithm, ai1_depth, ai2_depth, max_moves)
            
        else:
            print("Invalid mode selected.")
            
    except ValueError:
        print("Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()