"""
These are the game settings
"""

INF = 1000000

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (120, 68, 0)
LIGHTBROWN = (186, 141, 82)
CYAN = (104, 243, 243)

SMALLFONTSZ = 25
MEDIUMFONTSZ = 40
LARGEFONTSZ = 70

WIDTH = 640
HEIGHT = 760
TITLE = "Chess.ucu"
FPS = 60.0
# BGCOLOR = (184, 152, 83)
# BGCOLOR2 = (255, 255, 255)
BGCOLOR2 = (181, 159, 110)

TILESIZE = 64
TILEWIDTH = 64
TILEHEIGHT = 64

LETTERS = "abcdefgh"

BLACK_PIECES = {
    "bishop": "b_bishop.png",
    "king": "b_king.png",
    "pawn": "b_pawn.png",
    "knight": "b_knight.png",
    "rook": "b_rook.png",
    "queen": "b_queen.png",
}

WHITE_PIECES = {
    "bishop": "w_bishop.png",
    "king": "w_king.png",
    "pawn": "w_pawn.png",
    "knight": "w_knight.png",
    "rook": "w_rook.png",
    "queen": "w_queen.png",
}

POINTS = {
    "P": 1,
    "p": 1,
    "N": 3,
    "n": 3,
    "B": 3,
    "b": 3,
    "R": 5,
    "r": 5,
    "Q": 9,
    "q": 9,
    "K": 90,
    "k": 90
}

PATHRADIUS = 20
BORDERSIZE = 15

EVALUATION_POINTS = {"p": -10, "n": -30, "b": -30, "r": -50, "q": -90, "k": -900,
                     "P": 10, "N": 30, "B": 30, "R": 50, "Q": 90, "K": 900}

DEPTH = 2