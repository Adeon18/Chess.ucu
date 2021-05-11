import pygame
from settings import *
from pprint import pprint

letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
letters2 = {0: 'a', 1: 'b', 2: 'c', 3: 'c', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

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
    def __init__(self):
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
        self.rect.centerx = 4*TILESIZE + self.grid_x * TILESIZE + TILESIZE/2
        self.rect.centery = 1*TILESIZE + self.grid_y * TILESIZE + TILESIZE/2

        self.selected = False

        self.tipe = tipe
        self.pos = pos
        self.color = color
        self.game_board.add_piece(self, self.pos)
    
    def __repr__(self):
        return self.tipe
    
    def update(self):
        # keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0] and self.selected:
            mouse_position = pygame.mouse.get_pos()
            nxt_pos = self.game.move_click(mouse_position)
            # print(self.possible_moves())
            if nxt_pos in [convert_position(x) for x in self.possible_moves()]:
                self.move(nxt_pos)
    
    def move(self, next_pos):
        if next_pos:
            self.rect.centerx = 4*TILESIZE + next_pos[0] * TILESIZE + TILESIZE/2
            self.rect.centery = 1*TILESIZE + next_pos[1] * TILESIZE + TILESIZE/2
            print(next_pos)
            next_pos = convert_position_to_str(next_pos)
            
            self.game_board.add_piece(self, next_pos)
            self.game_board.remove_piece(self.pos)
            self.pos = next_pos
            print(self.game_board)
        self.selected = False

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

        pos = self.pos[0] + str(int(self.pos[1]) + mod)
        if self.game_board[pos] == 0:
            possible_moves.append(pos)
        
        pos = letters2[letters[self.pos[0]]-1] + str(int(self.pos[1]) + mod)
        if self.game_board[pos] != 0:
            possible_moves.append(pos)

        pos = letters2[letters[self.pos[0]]+1] + str(int(self.pos[1]) + mod)
        if self.game_board[pos] != 0:
            possible_moves.append(pos)

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

        self.rect.x = 4*TILESIZE + self.grid_x * TILESIZE
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
    