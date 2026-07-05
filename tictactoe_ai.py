"""
Tic-Tac-Toe: Human vs. Unbeatable AI
=====================================


Board positions are numbered 1-9 like a phone keypad:

     1 | 2 | 3
    -----------
     4 | 5 | 6
    -----------
     7 | 8 | 9

Run this file directly to play:
"""

import math
import random
import time

HUMAN = "X"
AI = "O"
EMPTY = " "

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
]


# Board helpers

def new_board():
    return [EMPTY] * 9


def print_board(board):
    def cell(i):
        return board[i] if board[i] != EMPTY else str(i + 1)

    rows = []
    for r in range(0, 9, 3):
        rows.append(f" {cell(r)} | {cell(r+1)} | {cell(r+2)} ")
    print("\n-----------\n".join(rows))
    print()


def winner(board):
    """Return 'X', 'O', 'Draw', or None (game still going)."""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "Draw"
    return None


def available_moves(board):
    return [i for i, v in enumerate(board) if v == EMPTY]


# Minimax with Alpha-Beta Pruning

def minimax_ab(board, is_maximizing, alpha, beta, depth=0, stats=None):
    if stats is not None:
        stats["nodes"] += 1

    result = winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if result == "Draw":
        return 0

    if is_maximizing:
        value = -math.inf
        for move in available_moves(board):
            board[move] = AI
            value = max(value, minimax_ab(board, False, alpha, beta, depth + 1, stats))
            board[move] = EMPTY
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cutoff — prune remaining branches
        return value
    else:
        value = math.inf
        for move in available_moves(board):
            board[move] = HUMAN
            value = min(value, minimax_ab(board, True, alpha, beta, depth + 1, stats))
            board[move] = EMPTY
            beta = min(beta, value)
            if beta <= alpha:
                break  # alpha cutoff — prune remaining branches
        return value


def best_move(board, stats=None):
    best_score = -math.inf
    best_moves = []
    for move in available_moves(board):
        board[move] = AI
        score = minimax_ab(board, False, -math.inf, math.inf, 0, stats)
        board[move] = EMPTY
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
    return random.choice(best_moves)  # randomize among equally-good moves


# Game loop

def choose_first_player():
    print("Who goes first?")
    print("  1) You (X)")
    print("  2) AI (O)")
    choice = input("Enter 1 or 2 [default 1]: ").strip()
    return HUMAN if choice != "2" else AI


def human_move(board):
    while True:
        raw = input("Your move (1-9): ").strip()
        if not raw.isdigit() or not (1 <= int(raw) <= 9):
            print("Please enter a number from 1 to 9.")
            continue
        idx = int(raw) - 1
        if board[idx] != EMPTY:
            print("That square is already taken. Try again.")
            continue
        return idx


def play_game():
    print("=" * 40)
    print("   TIC-TAC-TOE vs. Unbeatable AI")
    print("=" * 40)

    turn = choose_first_player()

    board = new_board()
    print("\nBoard positions:\n")
    print_board(list("123456789"))

    while True:
        print_board(board)

        if winner(board):
            break

        if turn == HUMAN:
            move = human_move(board)
            board[move] = HUMAN
        else:
            print("AI is thinking...")
            stats = {"nodes": 0}
            start = time.time()
            move = best_move(board, stats)
            elapsed = time.time() - start
            board[move] = AI
            print(f"AI plays {move + 1}  (evaluated {stats['nodes']} nodes in {elapsed:.3f}s)")

        turn = AI if turn == HUMAN else HUMAN

    print_board(board)
    result = winner(board)
    if result == "Draw":
        print("It's a draw! (Perfect play from both sides.)")
    elif result == AI:
        print("The AI wins! Better luck next time.")
    else:
        print("Congratulations, you won! (This shouldn't be possible against a "
              "correctly-implemented Minimax AI — nice bug hunting!)")


if __name__ == "__main__":
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
