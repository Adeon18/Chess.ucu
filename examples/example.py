"""
Some Array2D usage examples - I know that this is bad, but we don't have a strict plan yet
"""
import random
from arrays import Array2D

board = Array2D(8, 8)
pieces = ["P", "B", "K", "R", "Q", "K", "_"]

for i in range(8):
    for j in range(8):
        if i == 1 or i == 6:
            board[i, j] = "P"
        else:
            board[i, j] = "_"

board[0, 0], board[0, 7], board[7, 0], board[7, 7] = "R", "R", "R", "R"
board[0, 1], board[0, 6], board[7, 1], board[7, 6] = "H", "H", "H", "H"
board[0, 2], board[0, 5], board[7, 2], board[7, 5] = "B", "B", "B", "B"
board[0, 3], board[0, 4], board[7, 3], board[7, 4] = "Q", "K", "Q", "K"

print(board)