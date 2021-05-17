'''
unittest testing module
'''

import unittest
from abstract import *

class TestSquare(unittest.TestCase):
    
    def test_convert_position(self):
        self.assertEqual(convert_position("a1"), (0, 7))
    
    def test_convert_position_to_str(self):
        self.assertEqual(convert_position_to_str((0, 7)), "a1")
    
    def test_abstract_adt_getitem(self):
        abstract_adt = AbstractBoardADT()
        self.assertEqual(abstract_adt["a2"], 0)

    def testest_abstract_adt_add_piece(self):
        abstract_adt = AbstractBoardADT()
        abstract_adt.add_piece(AbstractPawn(abstract_adt, 1, 'a1'), "a2")
        self.assertEqual(str(abstract_adt["a2"]), "P")

    def testest_abstract_adt_remove_piece(self):
        abstract_adt = AbstractBoardADT()
        abstract_adt.add_piece(AbstractPawn(abstract_adt, 1, 'a1'), "a2")
        abstract_adt.remove_piece("a2")
        self.assertEqual(abstract_adt["a2"], 0)
    
    def test_possible_pawn_moves(self):
        abstract_adt = AbstractBoardADT()
        pawn = AbstractPawn(abstract_adt, 1, 'a2')
        self.assertEqual(pawn.possible_moves(), ['a3', 'a4'])
    
    def test_possible_king_moves(self):
        abstract_adt = AbstractBoardADT()
        king = AbstractKing(abstract_adt, 1, 'd1')
        self.assertEqual(king.possible_moves(), ['c2', 'c1', 'd2', 'e2', 'e1'])

    def test_possible_knight_moves(self):
        abstract_adt = AbstractBoardADT()
        knight = AbstractKnight(abstract_adt, 1, 'a2')
        self.assertEqual(knight.possible_moves(), ['b4', 'c3', 'c1'])

    def test_possible_bishop_moves(self):
        abstract_adt = AbstractBoardADT()
        bishop = AbstractBishop(abstract_adt, 1, 'a2')
        self.assertEqual(bishop.possible_moves(), ['b1', 'b3', 'c4', 'd5', 'e6', 'f7', 'g8'])

    def test_possible_rook_moves(self):
        abstract_adt = AbstractBoardADT()
        rook = AbstractRook(abstract_adt, 1, 'a2')
        self.assertEqual(rook.possible_moves(), ['b2','c2','d2',
                                                'e2','f2','g2','h2','a1',
                                                'a3','a4','a5','a6','a7','a8'])

    def test_possible_queen_moves(self):
        abstract_adt = AbstractBoardADT()
        queen = AbstractQueen(abstract_adt, 1, 'a2')
        self.assertEqual(queen.possible_moves(), ['b2','c2','d2',
                                                'e2','f2','g2','h2','a1',
                                                'a3','a4','a5','a6','a7','a8',
                                                'b1','b3','c4','d5','e6','f7','g8'])


if __name__ == "__main__":
    unittest.main()