'''
main module for the chess
pygame interface is located here
'''
import pygame
import sys
from os import path

from settings import *
from sprites import *
from bestmove import evaluate_board
import time


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
        self.opponent = None
        self.additional_update = False

    def load_data(self):
        """
        Load all the external data
        """
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.font_folder = path.join(game_folder, 'fonts')

        self.board_icon = pygame.image.load(path.join(img_folder, "board.icon.png"))
        self.board_icon = pygame.transform.scale(self.board_icon, (200, 200))

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

        self.outro_dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.outro_dim_screen.fill((181, 159, 110, 180))

    def new(self):
        """
        New game
        """
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.positions = pygame.sprite.LayeredUpdates()
        self.pieces = pygame.sprite.LayeredUpdates()
        # Create board
        self.create_board()
        self.board = BoardADT()
        # Get the flags
        if self.opponent == "player":
            self.against_player = True
            self.against_bot = False
        elif self.opponent == "PC":
            self.against_player = False
            self.against_bot = True
        else:
            raise IndexError("No side chosen smh")
        # Put the figures on the board
        # Black
        Pawn(self, self.board, 0, "a7")
        Pawn(self, self.board, 0, "b7")
        Pawn(self, self.board, 0, "c7")
        Pawn(self, self.board, 0, "d7")
        Pawn(self, self.board, 0, "e7")
        Pawn(self, self.board, 0, "f7")
        Pawn(self, self.board, 0, "g7")
        Pawn(self, self.board, 0, "h7")

        King(self, self.board, 0, "e8")
        Queen(self, self.board, 0, "d8")
        Knight(self, self.board, 0, "b8")
        Knight(self, self.board, 0, "g8")
        Bishop(self, self.board, 0, "c8")
        Bishop(self, self.board, 0, "f8")
        Rook(self, self.board, 0, "a8")
        Rook(self, self.board, 0, "h8")
        # White
        Pawn(self, self.board, 1, "a2")
        Pawn(self, self.board, 1, "b2")
        Pawn(self, self.board, 1, "c2")
        Pawn(self, self.board, 1, "d2")
        Pawn(self, self.board, 1, "e2")
        Pawn(self, self.board, 1, "f2")
        Pawn(self, self.board, 1, "g2")
        Pawn(self, self.board, 1, "h2")

        King(self, self.board, 1, "e1")
        Queen(self, self.board, 1, "d1")
        Knight(self, self.board, 1, "b1")
        Knight(self, self.board, 1, "g1")
        Bishop(self, self.board, 1, "c1")
        Bishop(self, self.board, 1, "f1")
        Rook(self, self.board, 1, "a1")
        Rook(self, self.board, 1, "h1")
        # print(f"Board evaluated: {evaluate_board(self.board)}")

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
        # print(self.board.white_points)
        # print(self.board.black_points)
        # ticks = pygame.time.get_ticks()
        if self.additional_update:
            self.additional_update = False
            self.update()
            time.sleep(0.5)
        if self.against_bot:
            if self.board.moves % 2 != 0: # bot move
                # if pygame.time.get_ticks() - ticks
                # pygame.time.wait(1000)
                self.board.make_computer_move()
                # self.board.deselect_all()

    def draw_grid(self):
        """
        Just a debugging tool for grid drawing
        """
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
        if TILESIZE <= pos[0] <= 9 * TILESIZE and 1 * TILESIZE <= pos[1] <= WIDTH - 1 * TILESIZE:
            for piece in self.pieces:
                piece.selected = False
                if piece.rect.collidepoint(pos):
                    return piece
    
    def move_click(self, pos):
        """
        Select a place for the piece to go to
        """
        if TILESIZE <= pos[0] <= 9* TILESIZE and 1 * TILESIZE <= pos[1] <= WIDTH - 1 * TILESIZE:
            for position in self.positions:
                position.selected = False
                if position.rect.collidepoint(pos):
                    return position.grid_x, position.grid_y

    def draw(self):
        """
        Blit everything to the screen each frame
        """
        self.screen.fill(BGCOLOR2)

        # self.draw_grid()
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
        """
        Show menu before the game start
        """
        self.screen.fill(BGCOLOR2)
        # Draw text and graphics
        self.draw_text("Chess.ucu", LARGEFONTSZ, DARKGREY, WIDTH // 2, HEIGHT / 7, align="center")
        self.draw_text("A chess game with 2 game modes", 30, DARKGREY, WIDTH // 2, HEIGHT / 4, align="center")
        self.screen.blit(self.board_icon, (WIDTH//2 - 100, HEIGHT//2 - 100))
        self.draw_text("Press 0 to play against a friend", SMALLFONTSZ, DARKGREY, WIDTH // 2, HEIGHT - HEIGHT//5, align="center")
        self.draw_text("Press 1 to play against the computer", SMALLFONTSZ, DARKGREY, WIDTH // 2, HEIGHT - HEIGHT//7, align="center")
        # Flip the display
        pygame.display.flip()
        # 
        self.wait_for_game_mode()

    def show_go_screen(self):
        """
        Show Outro screen
        """
        self.screen.blit(self.dim_screen, (0, 0))
        # Draw text and graphics
        # Put an if here
        if self.board.winning_team == 1:
            self.draw_text("WHITE WON", LARGEFONTSZ, WHITE, WIDTH // 2, HEIGHT // 3, align="center", fontname="Monospace_bold.ttf")
        elif self.board.winning_team == 0:
            self.draw_text("BLACK WON", LARGEFONTSZ, WHITE, WIDTH // 2, HEIGHT // 3, align="center", fontname="Monospace_bold.ttf")
        self.draw_text("Press 0 to play against a friend", SMALLFONTSZ, LIGHTBROWN, WIDTH // 2, HEIGHT - HEIGHT//5, align="center")
        self.draw_text("Press 1 to play against PC", SMALLFONTSZ, LIGHTBROWN, WIDTH // 2, HEIGHT - HEIGHT//7, align="center")
        # Flip the display
        pygame.display.flip()
        # 
        self.wait_for_game_mode()

    def wait_for_game_mode(self):
        """
        This is the same as wait for key, but it waits for user
        to choose PVP or PV(AI)
        """
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        self.opponent = "player"
                        waiting = False
                    if event.key == pygame.K_1:
                        self.opponent = "PC"
                        waiting = False

    def wait_for_key(self):
        """
        Wait for ANY key pressed by the user
        """
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

    def draw_text(self, text, size, color, x, y, align='center', fontname="Monospace_default.ttf"):
        """
        Helper for drawing text on the screen
        """
        font = pygame.font.Font(path.join(self.font_folder, fontname), size)
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
        """
        Draw the HUD and everything related
        """
        self.draw_board_notation_hud()
        self.draw_points()
    
    def draw_board_notation_hud(self):
        """
        Draw the notation, border for the board, used by draw_hud
        """
        # Draw the board numbers
        for i in range(8, 0, -1):
            # Left side
            side1_x = TILESIZE/2
            # Right side
            side2_x = 9*TILESIZE + TILESIZE/2
            # Y's are all the same
            y = abs(i-9) * TILESIZE + TILESIZE/2
            # Draw the numbers
            self.draw_text(str(i), SMALLFONTSZ, BLACK, side1_x, y)
            # self.draw_text(str(i), SMALLFONTSZ, BLACK, side2_x, y)
        # Draw letters on the board
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for i, letter in enumerate(letters):
            # Define the upper row
            up_y = TILESIZE/2
            # Define the lower row
            down_y = HEIGHT - TILESIZE/2
            # Define a stable x for both
            x = TILESIZE + i*TILESIZE + TILESIZE/2
            # Draw the letters
            self.draw_text(letter.upper(), SMALLFONTSZ, BLACK, x, up_y)
            # self.draw_text(letter, SMALLFONTSZ, BLACK, x, down_y)
        # Draw a border around the board
        pygame.draw.rect(self.screen, DARKGREY, pygame.Rect(TILESIZE, TILESIZE,\
                                                         TILESIZE*8, TILESIZE*8), int(BORDERSIZE*1.2))
    
    def draw_points(self):
        """
        Draw blue and white points to the screen
        """
        self.draw_text("WHITE", MEDIUMFONTSZ, WHITE, WIDTH//4 + MEDIUMFONTSZ, HEIGHT - HEIGHT//6, fontname="Monospace_bold.ttf")
        self.draw_text("BLACK", MEDIUMFONTSZ, BLACK, WIDTH//2 + WIDTH//4 - MEDIUMFONTSZ, HEIGHT - HEIGHT//6, fontname="Monospace_bold.ttf")

        self.draw_text(f"{self.board.white_points}", MEDIUMFONTSZ, WHITE, WIDTH//4 + MEDIUMFONTSZ, HEIGHT - HEIGHT//12, fontname="Monospace_bold.ttf")
        self.draw_text(f"{self.board.black_points}", MEDIUMFONTSZ, BLACK, WIDTH//2 + WIDTH//4 - MEDIUMFONTSZ, HEIGHT - HEIGHT//12, fontname="Monospace_bold.ttf")
        # self.draw_text(letter, 25, BLACK, x, down_y)


if __name__ == "__main__":
    # create the game object
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()
