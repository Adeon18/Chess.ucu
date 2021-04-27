"""
!!!!!!!!!
This is an oversimplified example, as we did no learn a lot about desition trees yet
and we are still thinking about the best implementation of a chess board and ADT's.
"""
from arrays import Array2D


class Board:
    """
    A representation of a chess board using a 2D list
    """
    def __init__(self):
        self.chess_board = Array2D(8, 8)
        self.position_history = {}
    
    def possible_moves(self):
        """
        Give all of the possible moves on the board
        """
        pass


class Piece:
    """
    A parent class for a chess piece - very raw for now
    """
    def __init__(self):
        self.current_position = ()
        self.move_history = dict()

    def move(self, from_cell, to_cell):
        """
        Move between cells
        """
        pass
