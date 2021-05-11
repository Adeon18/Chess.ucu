import pygame
import sys
from os import path

from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        # Make screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scr_width, self.scr_height = pygame.display.get_surface().get_size()
        pygame.display.set_caption(TITLE)
        # Load data and start te clock
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        """
        Load all the external data
        """
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')

        self.white_pieces = {}
        for piece in WHITE_PIECES:
            original_image = pygame.image.load(path.join(img_folder, WHITE_PIECES[piece]))
            self.white_pieces[piece] = pygame.transform.scale(original_image, (60, 60))
        
        self.black_pieces = {}
        for piece in BLACK_PIECES:
            original_image = pygame.image.load(path.join(img_folder, BLACK_PIECES[piece]))
            self.black_pieces[piece] = pygame.transform.scale(original_image, (60, 60))

        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))


    def new(self):
        """
        New game
        """
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.positions = pygame.sprite.LayeredUpdates()
        self.pieces = pygame.sprite.LayeredUpdates()
        self.create_board()
        self.board = BoardADT()
        Pawn(self, self.board, 1, "b2")
        Pawn(self, self.board, 0, "c3")

        King(self, self.board, 0, "c4")

        Knight(self, self.board, 0, "c6")

        Bishop(self, self.board, 1, "e6")

        Rook(self, self.board, 1, "d6")

        Queen(self, self.board, 1, "h6")

        self.draw_debug = False
        self.paused = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        """
        The whole game process logic that need to be updated each second
        """
        self.all_sprites.update()


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
        
        # for x in range(4*TILESIZE, WIDTH - 4*TILESIZE, TILESIZE):
        #     for y in range(TILESIZE, HEIGHT - 1*TILESIZE, TILESIZE):
        #         if ((x+y) / TILESIZE) % 2 == 0:
        #             pygame.draw.rect(self.screen, LIGHTBROWN, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT))
        #         else:
        #             pygame.draw.rect(self.screen, BROWN, pygame.Rect(x, y, TILEWIDTH, TILEHEIGHT))
        # self.screen.blit(self.black_pieces["queen"], (5*TILESIZE, 5*TILESIZE))

        # self.screen.blit(self.white_pieces["queen"], (300, 100))

    def create_board(self):
        for x in range(8):
            for y in range(8):
                if (x+y) % 2 == 0:
                    pos = Position(self, x, y, LIGHTBROWN)
                    # print("lol")
                else:
                    pos = Position(self, x, y, BROWN)
                # Piece(self, pos, x, y)
    
    
    def select_click(self, pos):
        """
        Select a piece
        """
        if 4* TILESIZE <= pos[0] <= WIDTH - 4* TILESIZE and 1 * TILESIZE <= pos[1] <= WIDTH - 1 * TILESIZE:
            for piece in self.pieces:
                piece.selected = False
                if piece.rect.collidepoint(pos):
                    return piece
    
    def move_click(self, pos):
        """
        Select a place for the piece to go to
        """
        if 4* TILESIZE <= pos[0] <= WIDTH - 4* TILESIZE and 1 * TILESIZE <= pos[1] <= WIDTH - 1 * TILESIZE:
            for position in self.positions:
                position.selected = False
                if position.rect.collidepoint(pos):
                    return position.grid_x, position.grid_y


    def draw(self):
        """
        Blit everything to the screen each frame
        """
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)

        self.draw_grid()
        self.draw_hud()
        # self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
            # sprite.draw()
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, sprite.rect, 1)
            # Draw selected border 
            if hasattr(sprite, "selected") and sprite.selected:
                pygame.draw.rect(self.screen, RED, sprite.rect, 3)
            if hasattr(sprite, "draw_add_data") and sprite.draw_add_data:
                sprite.draw_possible_moves()
            

        if self.draw_debug:
            self.draw_text("{:.2f}".format(self.clock.get_fps()), 25, CYAN, self.scr_width / 2, 30)

        # What to draw if paused
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', 105, RED, self.scr_width / 2, self.scr_height / 2)
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.quit()
                if event.key == pygame.K_F3:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                pos = self.select_click(mouse_position)
                if pos:
                    self.board.deselect_all()
                    pos.selected = True

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y, align='center'):
        font = pygame.font.SysFont('Consolas', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_hud(self):
        for i in range(1, 9):
            side1_x = 3*TILESIZE + TILESIZE/2
            side2_x = WIDTH - 4*TILESIZE + TILESIZE/2
            y = i * TILESIZE + TILESIZE/2
            self.draw_text(str(i), 20, WHITE, side1_x, y)
            self.draw_text(str(i), 20, WHITE, side2_x, y)



# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()