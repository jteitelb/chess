import pygame
import board
from typing import Tuple


def square_coords(square: str) -> Tuple[int, int]:
    if not type(square) is str:
        raise TypeError("expeced string")
    if len(square) != 2:
        raise ValueError("expected 2 characters")
    (s_file, s_rank) = square
    s_file = s_file.lower()
    if s_file < "a" or s_file > "h":
        raise ValueError("invalid file")

    if s_rank < "1" or s_rank > "8":
        raise ValueError("invalid rank")

    xVal = ord(s_file) - ord('a')
    yVal = 8 - int(s_rank)
    return (xVal, yVal)

def square_name(coords: Tuple[int, int]) -> str:
    if not type(coords) is tuple:
        raise TypeError("expected tuple")

    (x,y) = coords
    if x < 0 or x > 7 or y < 0 or y > 7:
        raise ValueError("invalid x or y coordinate")
    letter = chr(x + ord('a'))
    rank = 8 - y
    return f"{letter}{rank}"

BOARD_LENGTH = 560
WIN_WIDTH = BOARD_LENGTH
WIN_HEIGHT = BOARD_LENGTH
SQUARE_SIZE = BOARD_LENGTH // 8
SQUARE_DIMENSIONS = (SQUARE_SIZE, SQUARE_SIZE)

WHITE_SQUARE = (255, 231, 184)
BLACK_SQUARE = (179, 133, 91)
HIGHLIGHT_COLOR = (255,255,50)

def board_to_screen(coord):
    (x,y) = coord
    return (SQUARE_SIZE * x, SQUARE_SIZE * y)

C_MAP = {0: "W", 1: "B"}

# highlighted = [(0,0), squareCoord("E4"), squareCoord("A3"), squareCoord("H8")]
highlighted = []

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (self.x + self.y) % 2
        self.image = pygame.Surface(SQUARE_DIMENSIONS)
        
        if (x,y) in highlighted:
            self.image.fill(HIGHLIGHT_COLOR)
            # print(squareName((s_file, s_rank)), (s_file, s_rank))
        elif self.color:
            self.image.fill(BLACK_SQUARE)
        else:
            self.image.fill(WHITE_SQUARE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * SQUARE_SIZE
        self.rect.y = self.y * SQUARE_SIZE

    def name(self):
        return square_name((self.x, self.y))

    def __str__(self):
        return f"{self.name()}: {C_MAP[self.color]}"

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, piece_type, coords):
        super().__init__()
        self.color = color
        self.piece_type = piece_type
        self.coords = coords
        self.image = pygame.transform.scale(pygame.image.load(self.get_image_filename()), SQUARE_DIMENSIONS)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = board_to_screen(self.coords)

    def get_square(self):
        return square_name(self.coords)

    def move(self, square):
        self.coords = square_coords(square)
        (self.rect.x, self.rect.y) = board_to_screen(self.coords)

    def get_image_filename(self):
        return f"pieces/{self.color.lower()}{self.piece_type}.png"

    def draw(self):
        window.blit(self.image, board_to_screen(self.coords))
    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {square_name(self.coords)}"


def generate_pieces(color):
    if color == "W":
        back_rank = 7
        front_line = 6
    elif color == "B":
        back_rank = 0
        front_line = 1
    else:
        raise ValueError("invalid color")

    pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]

    result = pygame.sprite.Group()
    for x, piece in enumerate(pieces):
        tmp = Piece(color, piece, (x, back_rank))
        result.add(tmp)
    for x in range(8):
        tmp = Piece(color, "P", (x, front_line))
        result.add(tmp)
    return result


def add_coords(a, b):
    return tuple(x + y for x, y in zip(a,b))

# get all coordinates on the board
board_coords = [(i,j) for j in range(8) for i in range(8)]

# create squares
squares = pygame.sprite.Group()
for s in board_coords:
    temp = Square(s[0], s[1])
    squares.add(temp)

# create pieces
white_pieces = generate_pieces("W")
black_pieces = generate_pieces("B")
pieces = white_pieces.copy()
pieces.add(black_pieces)

# peek a square by name e.g. "A1"
# returns the first piece found, or None if no pieces are on the square
def peek(square):
    peek_coords = square_coords(square)
    for p in pieces:
        if p.coords == peek_coords:
            return p
    return None



if __name__ == "__main__":
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    running = True
    while running:
        #window.fill((100,255,255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        squares.draw(window)
        pieces.draw(window)
        pygame.display.update()

    
