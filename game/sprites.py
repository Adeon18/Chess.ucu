import pygame
from copy import deepcopy
from settings import *
from bestmove import *
from pprint import pprint
from time import sleep

letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
letters2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


def convert_position(string):
    '''
    '''
    x, y = string[0], string[1]
    x = letters[x]
    y = 8 - int(y)
    return x, y


def convert_position_to_str(pos):
    '''
    '''
    x, y = pos[0], pos[1]
    x = letters2[x]
    y = 8-y
    res = str(x) + str(y)
    return res


class BoardADT:
    '''
    board data type which contains all the information about the chess game
    '''
    def __init__(self, copy=None):
        '''
        initialise an empty board
        '''
        if copy:
            self.init_from_copy()
        else:
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
            self.en_passant = ""
            self.winning_team = ""
            self.white_points = 0
            self.black_points = 0

    def init_from_copy(self, copy):
        old_content, self.moves, self.en_passant, self.winning_team, self.white_points, self.black_points = copy
        for row in old_content:
            print(row)

    def __getitem__(self, pos):
        '''
        '''
        x, y = convert_position(pos)
        return self.content[y][x]

    def add_piece(self, piece, position):
        '''
        '''
        x, y = convert_position(position)
        self.content[y][x] = piece

    def remove_piece(self, position):
        '''
        '''
        x, y = convert_position(position)
        self.content[y][x] = 0
    
    def __str__(self):
        result = ""
        for i in self.content:
            for j in i:
                result += str(j) + " "
            result += "\n"
        return result
    
    def deselect_all(self):
        """
        Deselect all pieces
        """
        for row in self.content:
            for elem in row:
                if elem != 0:
                    elem.selected = False
    
    def check_moves(self, pos):
        """
        Check if we are allowed to move dependng on the color
        """
        x, y = pos
        if self.moves % 2 == 0:
            if self.content[y][x] != 0:
                if self.content[y][x].color == 1:
                    return True
        else:
            if self.content[y][x] != 0:
                if self.content[y][x].color == 0:
                    if self.content[y][x].game.against_player:
                        return True
                    elif self.content[y][x].game.against_bot:
                        return False

    def make_computer_move(self):
        print("Ready to make computer move, moves =", self.moves)
        # sleep(0.5)
        try:
            chosen_piece, chosen_move = best_move(self, depth=DEPTH)
        except TypeError:
            self.winning_team = 1
            return None
        print(f"Computer chose {chosen_piece} to move to {chosen_move}")
        chosen_move = (letters[chosen_move[0]], 8 - int(chosen_move[1]))
        chosen_piece.move(chosen_move)
        print(chosen_piece, chosen_move)
        # self.moves += 1

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

    def possible_computer_moves(self):
        # print(board.content)
        possible_computer_moves = []
        for row in self.content:
            for piece in row:
                if str(piece) == str(piece).lower():
                    try:
                        # print(f"{piece} can make following moves: {piece.possible_moves()}")
                        for move in piece.possible_moves():
                            possible_computer_moves.append((piece, move))
                    except AttributeError:
                        pass
        # print(f"All possible moves for computer: {possible_computer_moves}")
        return possible_computer_moves


class Piece(pygame.sprite.Sprite):
    '''
    parent class for all pieces
    '''
    def __init__(self, game, board, tipe, color, pos):
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
        self.groups = game.all_sprites, game.pieces
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game_board = board
        # self.position = position
        self.grid_x, self.grid_y = convert_position(pos)
        self.rect = self.image.get_rect()
        self.rect.centerx = TILESIZE + self.grid_x * TILESIZE + TILESIZE/2
        self.rect.centery = 1*TILESIZE + self.grid_y * TILESIZE + TILESIZE/2

        self.selected = False
        self.draw_add_data = False

        self.tipe = tipe
        self.pos = pos
        self.color = color
        self.game_board.add_piece(self, self.pos)

        self.move_stack = [self.pos]
    
    def __repr__(self):
        return self.tipe
    
    def draw_possible_moves(self):
        """
        Draw possible positions for movement
        """
        possibilities = [convert_position(x) for x in self.possible_moves()]
        for pos in possibilities:
            # Define the center of the circle
            center = (TILESIZE + pos[0] * TILESIZE + TILESIZE/2, 1*TILESIZE + pos[1] * TILESIZE + TILESIZE/2)
            pygame.draw.circle(self.game.screen, RED, center, PATHRADIUS)

    def update(self):
        # keys = pygame.key.get_pressed()
        if self.selected and self.game_board.check_moves((self.grid_x, self.grid_y)):
            self.draw_add_data = True
            if pygame.mouse.get_pressed()[0]:
                handled = pygame.mouse.get_pressed()[0]
                mouse_position = pygame.mouse.get_pos()
                nxt_pos = self.game.move_click(mouse_position)
                # print(self.possible_moves())
                if nxt_pos in [convert_position(x) for x in self.possible_moves()]:
                    self.move(nxt_pos)
        else:
            self.draw_add_data = False
    
    def move(self, next_pos, hypothetical=False):
        """
        Move the figure to the next position
        """
        old_white_points, old_black_points = self.game_board.white_points, self.game_board.black_points
        if next_pos:
            self.grid_x, self.grid_y = next_pos  # This is to keep track of the pos
            self.rect.centerx = TILESIZE + next_pos[0] * TILESIZE + TILESIZE/2
            self.rect.centery = 1*TILESIZE + next_pos[1] * TILESIZE + TILESIZE/2
            # Get the next pos
            next_pos = convert_position_to_str(next_pos)
            # print(next_pos)
            self.move_stack.append(next_pos)

            # print(isinstance(self, King))
            if isinstance(self, Rook):
                self.castle = False
                try:
                    if self.game_board[next_pos].tipe == "k":
                        self.game_board.winning_team = 1
                        self.game.playing = False
                    elif self.game_board[next_pos].tipe == "K":
                        self.game_board.winning_team = 0
                        self.game.playing = False
                    else:
                        if self.color == 1:
                            self.game_board.white_points += POINTS[self.game_board[next_pos].tipe]
                        else:
                            self.game_board.black_points += POINTS[self.game_board[next_pos].tipe]
                    self.game_board[next_pos].kill()
                except AttributeError:
                    pass
                self.game_board.add_piece(self, next_pos)
                self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
            
            elif isinstance(self, King):

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
                    try:
                        # Check for the points and the king death
                        if self.game_board[next_pos].tipe == "k":
                            self.game_board.winning_team = 1
                            self.game.playing = False
                        elif self.game_board[next_pos].tipe == "K":
                            self.game_board.winning_team = 0
                            self.game.playing = False
                        else:
                            if self.color == 1:
                                self.game_board.white_points += POINTS[self.game_board[next_pos].tipe]
                            else:
                                self.game_board.black_points += POINTS[self.game_board[next_pos].tipe]
                            self.game_board[next_pos].kill()
                    except AttributeError:
                        pass
                    self.game_board.add_piece(self, next_pos)
                    self.game_board.remove_piece(self.pos)
                    self.game_board.moves += 1
            
            elif isinstance(self, Pawn):
                # print(self.color, next_pos[1])
                if int(next_pos[1]) == 8 or int(next_pos[1]) == 1:
                    try:
                        if self.color == 1:
                                self.game_board.white_points += POINTS[self.game_board[next_pos].tipe]
                        else:
                                self.game_board.black_points += POINTS[self.game_board[next_pos].tipe]
                        self.game_board[next_pos].kill()
                    except AttributeError:
                        pass
                    # print("QUEEEEN")
                    self.game_board.add_piece(Queen(self.game, self.game_board, self.color, next_pos), next_pos)
                    self.game_board.remove_piece(self.pos)
                    self.kill()
                    
                else:
                    try:
                        if self.color == 1:
                                self.game_board.white_points += POINTS[self.game_board[next_pos].tipe]
                        else:
                                self.game_board.black_points += POINTS[self.game_board[next_pos].tipe]
                        self.game_board[next_pos].kill()
                    except:
                        pass
                    self.game_board.add_piece(self, next_pos)
                    self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
            else:
                try:
                    if self.game_board[next_pos].tipe == "k":
                        self.game_board.winning_team = 1
                        self.game.playing = False
                    elif self.game_board[next_pos].tipe == "K":
                        self.game_board.winning_team = 0
                        self.game.playing = False
                    else:
                        if self.color == 1:
                            self.game_board.white_points += POINTS[self.game_board[next_pos].tipe]
                        else:
                            self.game_board.black_points += POINTS[self.game_board[next_pos].tipe]
                    self.game_board[next_pos].kill()
                except AttributeError:
                    pass
                self.game_board.add_piece(self, next_pos)
                self.game_board.remove_piece(self.pos)
                self.game_board.moves += 1
                    
            # Update the board


            self.pos = next_pos
            # print(self.game_board)
            # Deselect and change turns
            
            self.selected = False
            self.draw_add_data = False

        if hypothetical:
            self.game_board.winning_team = ""
            self.game_board.white_points = old_white_points
            self.game_board.black_points = old_black_points
            self.game.playing = True

    def revert_last_move(self):
        self.move_stack = self.move_stack[:-1]
        self.move(convert_position(self.move_stack[-1]))
        self.game_board.moves -= 2


class Pawn(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["pawn"]
            super().__init__(game, board, 'P', color, pos)
        if color == 0:
            self.image = game.black_pieces["pawn"]
            super().__init__(game, board, 'p', color, pos)

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


class King(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["king"]
            super().__init__(game, board, 'K', color, pos)
        if color == 0:
            self.image = game.black_pieces["king"]
            super().__init__(game, board, 'k', color, pos)

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
            if isinstance(self.game_board[poss], Knight):
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
            if isinstance(self.game_board[poss], Bishop) or isinstance(self.game_board[poss], Queen):
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
            if isinstance(self.game_board[poss], Rook) or isinstance(self.game_board[poss], Queen):
                return True
        return False


class Knight(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["knight"]
            super().__init__(game, board, 'N', color, pos)
        if color == 0:
            self.image = game.black_pieces["knight"]
            super().__init__(game, board, 'n', color, pos)

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


class Bishop(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["bishop"]
            super().__init__(game, board, 'B', color, pos)
        if color == 0:
            self.image = game.black_pieces["bishop"]
            super().__init__(game, board, 'b', color, pos)
    
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


class Rook(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["rook"]
            super().__init__(game, board, 'R', color, pos)
        if color == 0:
            self.image = game.black_pieces["rook"]
            super().__init__(game, board, 'r', color, pos)
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


class Queen(Piece):
    '''
    a class representing a pown piece
    '''
    def __init__(self, game, board, color, pos):
        '''
        initialise a pawn with its colour and position
        white color is represented as 1
        black color is represented as 0
        possibility of en passant capture is declared by default as False
        '''
        if color == 1:
            self.image = game.white_pieces["queen"]
            super().__init__(game, board, 'Q', color, pos)
        if color == 0:
            self.image = game.black_pieces["queen"]
            super().__init__(game, board, 'q', color, pos)
    
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


class Position(pygame.sprite.Sprite):
    def __init__(self, game, grid_x, grid_y, color):
        self.groups = game.all_sprites, game.positions
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.image = pygame.Surface((TILEWIDTH, TILEHEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.piece = None
        self.selected = False

        self.rect.x = TILESIZE + self.grid_x * TILESIZE
        self.rect.y = 1*TILESIZE + self.grid_y * TILESIZE


# class Piece(pygame.sprite.Sprite):
#     def __init__(self, game, grid_x, grid_y):
#         self.groups = game.all_sprites, game.pieces
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         # self.position = position
#         self.grid_x = grid_x
#         self.grid_y = grid_y
#         self.image = game.black_pieces["pawn"]
#         self.rect = self.image.get_rect()
#         self.rect.centerx = 4*TILESIZE + self.grid_x * TILESIZE + TILESIZE/2
#         self.rect.centery = 1*TILESIZE + self.grid_y * TILESIZE + TILESIZE/2

#         self.selected = False
    
#     def update(self):
#         # keys = pygame.key.get_pressed()
#         if pygame.mouse.get_pressed()[0] and self.selected:
#             mouse_position = pygame.mouse.get_pos()
#             nxt_pos = self.game.move_click(mouse_position)
#             self.move(nxt_pos)
    
#     def move(self, next_pos):
#         if next_pos:
#             self.rect.centerx = 4*TILESIZE + next_pos[0] * TILESIZE + TILESIZE/2
#             self.rect.centery = 1*TILESIZE + next_pos[1] * TILESIZE + TILESIZE/2
#         self.selected = False


# if __name__ == "__main__":
#     board1 = BoardADT()
#     piece1 = Knight(None, board1, 1, "a2")
