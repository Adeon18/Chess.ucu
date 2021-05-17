'''
a module representing BoardADT and abstract pieces for bot
'''
from pprint import pprint
from copy import deepcopy
from settings import LETTERS

letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
letters2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
old_boards = []

def convert_position(string):
    '''
    convert position in chess notation to standart list indexes
    '''
    x, y = string[0], string[1]
    x = letters[x]
    y = 8 - int(y)
    return x, y


def convert_position_to_str(pos):
    '''
    convert standart list indexes to the chess notation
    '''
    x, y = pos[0], pos[1]
    x = letters2[x]
    y = 8-y
    res = str(x) + str(y)
    return res


class AbstractBoardADT:
    '''
    board data type which contains all the information about the chess game
    '''
    def __init__(self, copy=None):
        '''
        initialise an empty board
        '''
        self.content = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.moves = 0
        if copy:
            self.init_from_copy(copy)


    def init_from_copy(self, copy):
        # print("here")
        self.moves, content = copy
        for row in content:
            for piece in row:
                try:
                    old_type = str(type(piece)).split(".")[1].split("\'")[0]
                    # print(piece.pos, piece.color)
                    # print("Abstract" + old_type + "(self, piece.color, piece.pos)")
                    copied_piece = eval("Abstract" + old_type + "(self, piece.color, piece.pos)")
                except IndexError:
                    pass
        # print("Copied to an abstract board:")
        # pprint(self.content)

    def __getitem__(self, pos):
        '''
        get item from ADT
        pos must be in chess notation: "a1" - "h8"
        '''
        x, y = convert_position(pos)
        return self.content[y][x]

    def add_piece(self, piece, position):
        '''
        add a piece to the board
        piece instance must be Piece
        '''
        x, y = convert_position(position)
        self.content[y][x] = piece

    def remove_piece(self, position):
        '''
        remove piece from chess board by it's position
        '''
        x, y = convert_position(position)
        self.content[y][x] = 0
    
    def __str__(self):
        '''
        return a chess board with pieces being represented as letters
        capital letter means white piece, lower case - black piece
        '''
        result = ""
        for i in self.content:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result

    def possible_computer_moves(self):
        possible_computer_moves = []
        for row in self.content:
            for piece in row:
                if str(piece) == str(piece).lower():
                    try:
                        # print(f"{piece} can make following moves: {piece.possible_moves()}")
                        for move in piece.possible_moves():
                            # print(f"{piece} at {piece.pos} can move to {move}")
                            possible_computer_moves.append((piece.pos, move))
                    except AttributeError:
                        pass
        # print(f"All possible moves for computer: {possible_computer_moves}")
        return possible_computer_moves

    def revert_last_move(self):
        global old_boards
        # print("Reverting the following board:")
        # print(self)
        self.content, self.moves = old_boards[-1]
        # print("Reverted:")
        # print(self)
        for n_row, row in enumerate(self.content):
            for n_piece, piece in enumerate(row):
                try:
                    piece.pos = LETTERS[n_piece] + str(8 - n_row)
                except AttributeError:
                    pass
        old_boards = old_boards[:-1]
        # print(self.content[0][1].pos)

    def is_game_over(self):
        k_in, K_in = False, False
        for row in self.content:
            for piece in row:
                if str(piece) == "k":
                    k_in = True
                elif str(piece) == "K":
                    K_in = True
        if not all((k_in, K_in)):
            return True
        return False


class AbstractPiece:
    '''
    parent class for all pieces
    '''
    def __init__(self, board, tipe, color, pos):
        '''
        initialise a piece with its type, one of the following
        'p' for pawn
        'r' for rook
        'q' for queen
        'k' for king
        'n' for knight
        'b' for bishop
        white pieces get their tipe as capital letter, black as lower case letter
        '''
        self.game_board = board
        # self.position = position

        self.tipe = tipe
        self.pos = pos
        self.color = color
        self.game_board.add_piece(self, self.pos)
    
    def __repr__(self):
        return self.tipe
    
    def move(self, next_pos):
        """
        Move the figure to the next position
        """

        # print("Updating the old_boards with the content:")
        # pprint(self.game_board.content)

        global old_boards
        old_boards.append((deepcopy(self.game_board.content), deepcopy(self.game_board.moves)))

        # print("Updated.")
        # print(old_boards[-1][0])

        # print(repr(self.game_board))

        if next_pos:
            # Get the next pos
            next_pos = convert_position_to_str(next_pos)
            # print(next_pos)

            # print(isinstance(self, AbstractKing))
            if isinstance(self, AbstractRook):
                self.castle = False

                self.game_board.add_piece(self, next_pos)
                self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
            
            elif isinstance(self, AbstractKing):

                self.left_castle = False
                self.right_castle = False
                y = convert_position(self.pos)[1]

                if abs(convert_position(self.pos)[0] - convert_position(next_pos)[0]) == 2:
                    self.game_board.add_piece(self, next_pos)
                    # print(convert_position(next_pos)[0])
                    if convert_position(next_pos)[0] <= 4:
                        self.game_board.content[y][0].move((3, y))
                    else:
                        self.game_board.content[y][7].move((5, y))
                    self.game_board.remove_piece(self.pos)

                else: 
                    self.game_board.add_piece(self, next_pos)
                    self.game_board.remove_piece(self.pos)
                    self.game_board.moves += 1
            
            elif isinstance(self, AbstractPawn):
                # print(self.color, next_pos[1])
                if int(next_pos[1]) == 8 or int(next_pos[1]) == 1:
                    self.game_board.add_piece(AbstractQueen(self.game_board, self.color, next_pos), next_pos)
                    self.game_board.remove_piece(self.pos)

                    # self.kill()
                    
                else:
                    self.game_board.add_piece(self, next_pos)
                    self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
            else:
                self.game_board.add_piece(self, next_pos)
                self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
                    
            # Update the board

            self.pos = next_pos
            # print(self.game_board)
            # Deselect and change turns


class AbstractPawn(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'P', color, pos)
        if color == 0:
            super().__init__(board, 'p', color, pos)

        self.double_move = True
        
        self.en_passant = False
    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []
        
        if self.color == 1:
            mod = 1
        if self.color == 0:
            mod = -1

        x, y = convert_position(self.pos)
        try:
            pos = self.pos[0] + str(int(self.pos[1]) + mod)
            if self.game_board[pos] == 0:
                possible_moves.append(pos)
        except (IndexError, KeyError, AttributeError):
            pass

        if self.double_move:
            try:
                if (int(self.pos[1]) == 7 and self.color == 0) or (int(self.pos[1]) == 2 and self.color == 1):
                    pos = self.pos[0] + str(int(self.pos[1]) + 2*mod)
                    if self.game_board[pos] == 0:
                        possible_moves.append(pos)
            except (IndexError, KeyError, AttributeError):
                pass
        
        try:
            pos = letters2[letters[self.pos[0]]-1] + str(int(self.pos[1]) + mod)
            if self.game_board[pos].color != self.color:
                possible_moves.append(pos)
        except (IndexError, KeyError, AttributeError):
            pass

        try:
            pos = letters2[letters[self.pos[0]]+1] + str(int(self.pos[1]) + mod)
            if self.game_board[pos].color != self.color:
                possible_moves.append(pos)
        except (IndexError, KeyError, AttributeError):
            pass

        return possible_moves

class AbstractKing(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'K', color, pos)
        if color == 0:
            super().__init__(board, 'k', color, pos)

        self.left_castle = True
        self.right_castle = True
    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []

        x, y = convert_position(self.pos)

        for i in range(3):
            for j in range(3):
                try:
                    pos = (x - 1 + i, y - 1 + j)

                    if (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7):
                        if self.game_board[convert_position_to_str(pos)] == 0:
                            if not self.is_checked(convert_position_to_str(pos)):
                                possible_moves.append(convert_position_to_str(pos))
                        
                        elif self.game_board[convert_position_to_str(pos)].color != self.color:
                            if not self.is_checked(convert_position_to_str(pos)):
                                possible_moves.append(convert_position_to_str(pos))
                except (IndexError, KeyError):
                    pass

        if self.left_castle and not self.is_checked(self.pos):
            try:
                x, y = convert_position(self.pos)
                if self.game_board.content[y][0].castle:
                    castle = True
                    for i in range(3):
                        if self.game_board.content[y][x-i-1] != 0:
                            castle = False

                    if not self.is_checked(convert_position_to_str(pos)) and castle:
                        possible_moves.append(convert_position_to_str((x - 2, y)))
            except (IndexError, KeyError, AttributeError):
                pass

        if self.right_castle and not self.is_checked(self.pos):
            try:
                x, y = convert_position(self.pos)
                if self.game_board.content[y][7].castle:
                    castle = True
                    for i in range(2):
                        if self.game_board.content[y][x+i+1] != 0:
                            castle = False
                    if not self.is_checked(convert_position_to_str(pos)) and castle:
                        possible_moves.append(convert_position_to_str((x + 2, y)))
            except (IndexError, KeyError, AttributeError):
                pass

        return possible_moves

    def is_checked(self, positionn):
        '''
        returns True if king is checked, False if not
        '''
        x, y = convert_position(positionn)
        possible_moves = []
        for i in range(-2, 5):
            for j in range(-2, 5):
                try:
                    if i ** 2 + j ** 2 == 5:
                        pos = (x + i, y + j)
                        if pos[0] <= 7 and pos[1] <= 7 and pos[0] >= 0 and pos[1] >= 0:
                            if self.game_board[convert_position_to_str(pos)] == 0:
                                possible_moves.append(convert_position_to_str(pos))
                        
                            elif self.game_board[convert_position_to_str(pos)].color != self.color:
                                possible_moves.append(convert_position_to_str(pos))
                except (IndexError, KeyError):
                    pass
        for poss in possible_moves:
            if isinstance(self.game_board[poss], AbstractKnight):
                return True

        possible_moves = []

        x, y = convert_position(positionn)

        diagonals = [[[x + i, y + i] for i in range(1, 8)],
                    [[x + i, y - i] for i in range(1, 8)],
                    [[x - i, y + i] for i in range(1, 8)],
                    [[x - i, y - i] for i in range(1, 8)]]

        for direction in diagonals:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass

        for poss in possible_moves:
            x, y = convert_position(poss)
            if isinstance(self.game_board[poss], AbstractBishop) or isinstance(self.game_board[poss], AbstractQueen):
                return True

        possible_moves = []

        x, y = convert_position(positionn)

        cross = [[[x + i, y] for i in range(1, 8 - x)],
                [[x - i, y] for i in range(1, x + 1)],
                [[x, y + i] for i in range(1, 8 - y)],
                [[x, y - i] for i in range(1, y + 1)]]

        for direction in cross:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass
        for poss in possible_moves:
            x, y = convert_position(poss)
            if isinstance(self.game_board[poss], AbstractRook) or isinstance(self.game_board[poss], AbstractQueen):
                return True
        return False


class AbstractKnight(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'N', color, pos)
        if color == 0:
            super().__init__(board, 'n', color, pos)

    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []

        x, y = convert_position(self.pos)

        for i in range(-2, 5):
            for j in range(-2, 5):
                try:
                    if i ** 2 + j ** 2 == 5:
                        pos = (x + i, y + j)
                        if pos[0] <= 7 and pos[1] <= 7 and pos[0] >= 0 and pos[1] >= 0:
                            if self.game_board[convert_position_to_str(pos)] == 0:
                                possible_moves.append(convert_position_to_str(pos))
                        
                            elif self.game_board[convert_position_to_str(pos)].color != self.color:
                                possible_moves.append(convert_position_to_str(pos))
                except (IndexError, KeyError):
                    pass
        return possible_moves

class AbstractBishop(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'B', color, pos)
        if color == 0:
            super().__init__(board, 'b', color, pos)
    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []

        

        x, y = convert_position(self.pos)

        diagonals = [[[x + i, y + i] for i in range(1, 8)],
                    [[x + i, y - i] for i in range(1, 8)],
                    [[x - i, y + i] for i in range(1, 8)],
                    [[x - i, y - i] for i in range(1, 8)]]

        for direction in diagonals:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass
        
        return possible_moves

class AbstractRook(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'R', color, pos)
        if color == 0:
            super().__init__(board, 'r', color, pos)
        self.castle = True
    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []

        x, y = convert_position(self.pos)

        cross = [[[x + i, y] for i in range(1, 8 - x)],
                [[x - i, y] for i in range(1, x + 1)],
                [[x, y + i] for i in range(1, 8 - y)],
                [[x, y - i] for i in range(1, y + 1)]]

        for direction in cross:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass
        
        return possible_moves


class AbstractQueen(AbstractPiece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            super().__init__(board, 'Q', color, pos)
        if color == 0:
            super().__init__(board, 'q', color, pos)
    
    def possible_moves(self):
        '''
        return a list of all possible moves for piece as names of cells a-h 1-8
        '''
        possible_moves = []

        x, y = convert_position(self.pos)

        cross = [[[x + i, y] for i in range(1, 8 - x)],
                [[x - i, y] for i in range(1, x + 1)],
                [[x, y + i] for i in range(1, 8 - y)],
                [[x, y - i] for i in range(1, y + 1)]]

        for direction in cross:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass
        

        diagonals = [[[x + i, y + i] for i in range(1, 8)],
                    [[x + i, y - i] for i in range(1, 8)],
                    [[x - i, y + i] for i in range(1, 8)],
                    [[x - i, y - i] for i in range(1, 8)]]

        for direction in diagonals:
            for position in direction:
                try:
                    if position[0] < 0 or position[1] < 0 or position[0] > 7 or position[1] > 7:
                        break
                    pos = (position[0], position[1])
                    if self.game_board[convert_position_to_str(pos)] == 0:
                        possible_moves.append(convert_position_to_str(pos))

                    elif self.game_board[convert_position_to_str(pos)].color != self.color:
                        possible_moves.append(convert_position_to_str(pos))
                        break
                    else:
                        break
                except (IndexError, KeyError):
                    pass
        
        return possible_moves


if __name__ == "__main__":
    board1 = AbstractBoardADT()
    AbstractPawn(board1, 1, "a2")
    AbstractPawn(board1, 1, "b2")
    AbstractPawn(board1, 1, "c2")
    AbstractPawn(board1, 1, "d2")
    AbstractPawn(board1, 1, "e2")
    AbstractPawn(board1, 1, "f2")
    AbstractPawn(board1, 1, "g2")
    AbstractPawn(board1, 1, "h2")

    AbstractKing(board1, 1, "e1")
    AbstractQueen(board1, 1, "d1")
    AbstractKnight(board1, 1, "b1")
    AbstractKnight(board1, 1, "g1")
    AbstractBishop(board1, 1, "c1")
    AbstractBishop(board1, 1, "f1")
    AbstractRook(board1, 1, "a1")
    AbstractRook(board1, 1, "h1")
    # Black
    p1 = AbstractPawn(board1, 0, "a7")
    AbstractPawn(board1, 0, "b7")
    AbstractPawn(board1, 0, "c7")
    AbstractPawn(board1, 0, "d7")
    AbstractPawn(board1, 0, "e7")
    AbstractPawn(board1, 0, "f7")
    AbstractPawn(board1, 0, "g7")
    AbstractPawn(board1, 0, "h7")

    AbstractKing(board1, 0, "e8")
    AbstractQueen(board1, 0, "d8")
    AbstractKnight(board1, 0, "b8")
    AbstractKnight(board1, 0, "g8")
    b1 = AbstractBishop(board1, 0, "c8")
    AbstractBishop(board1, 0, "f8")
    r1 = AbstractRook(board1, 0, "a8")
    AbstractRook(board1, 0, "h8")

    # b1.move(())
    # print(p1.possible_moves())
    print(board1)
    p1.move((0, 3))
    print(board1)
    # print(r1.possible_moves())
    board1.revert_last_move()
    print(board1)
    pprint(board1.content)
