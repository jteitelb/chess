import pygame
import board
from typing import Tuple

# trying out idea from:
# http://composingprograms.com/pages/27-object-abstraction.html#multiple-representations
# cool, but might be better to just use coords as canonical representation, avoid duplication
class Square_XY():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def s_file(self):
        return chr(self.x + ord('a'))
    @property
    def s_rank(self):
        return (8 - self.y)
    
    def __repr__(self):
        return f"({self.x},{self.y})"

class Square_FR():
    def __init__(self, square_name):
        s_file, s_rank = square_name
        self.s_file = s_file.lower()
        self.s_rank = s_rank
    @property
    def x(self):
        return ord(self.s_file) - ord('a')
    @property
    def y(self):
        return (8 - int(self.s_rank))
    
    def __repr__(self):
        return f"{self.s_file}{self.s_rank}"


def square_coords(square: str) -> Tuple[int, int]:
    if not type(square) is str:
        raise TypeError("expected string")
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

class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, square):
        super().__init__()
        self.square = square
        self.color = (self.square.x + self.square.y) % 2
        self.image = pygame.Surface(SQUARE_DIMENSIONS)
        
        if (square.x,square.y) in highlighted:
            self.image.fill(HIGHLIGHT_COLOR)
            # print(squareName((s_file, s_rank)), (s_file, s_rank))
        elif self.color:
            self.image.fill(BLACK_SQUARE)
        else:
            self.image.fill(WHITE_SQUARE)
        self.rect = self.image.get_rect()
        self.rect.x = self.square.x * SQUARE_SIZE
        self.rect.y = self.square.y * SQUARE_SIZE
    
    @property
    def name(self):
        return f"{self.square.s_file}{self.square.s_rank}"

    def __repr__(self):
        return f"{self.name}: {C_MAP[self.color]}"

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
        if type(square) == str:
            new_coords = square_coords(square)
        else:
            new_coords = square
        if valid_coord(new_coords):
            self.coords = square_coords(square)
        else:
            raise ValueError("Invalid Coordinates")
        (self.rect.x, self.rect.y) = board_to_screen(self.coords)

    def get_image_filename(self):
        return f"pieces/{self.color.lower()}{self.piece_type}.png"

    def draw(self):
        window.blit(self.image, board_to_screen(self.coords))

    # probe in a straight line given a direction e.g. (0,1) will probe downward
    # return a list of squares on the board in the direction probed up to and including the first non-empty square
    def probe_line(self, direction):
        results = []
        current = add_coords(self.coords, direction)
        searching = True
        while searching:
            found = peek(current)
            results.append(square_name(current))
            if (peek(current) != None) or (not valid_coord(current)):
                searching = False
            current = add_coords(current, direction)
        return results
    
    def probe_multi(self, directions):
        res = []
        for d in directions:
            res += self.probe_line(d)

    def relative(self, relative_pos):
        return add_coords(self.coords, relative_pos)

    def get_moves(self):
        if self.piece_type == "P":
            return self.get_pawn_moves()

    # TODO: promotions and en passant
    def get_pawn_moves(self):
        moves = []
        if self.color == "W":
            single_move = self.relative((0,-1))
            double_move = self.relative((0,-2))
        elif self.color == "B":
            single_move = self.relative((0,1))
            double_move = self.relative((0,2))
        else:
            raise ValueError("unexpected color")

        if peek(single_move) == None:
            moves.append(single_move)
            if peek(double_move) == None:
                moves.append(double_move)
        
        # captures
        (x,y) = single_move
        l_capture = (x-1, y)
        r_capture = (x+1, y)
        l_piece = peek(l_capture)
        r_piece = peek(r_capture)
        if l_piece != None and l_piece.color != self.color:
            moves.append(l_capture)
        if r_piece != None and r_piece.color != self.color:
            moves.append(r_capture)

        return moves

    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {square_name(self.coords)}"


def valid_coord(coord):
    (x,y) = coord
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    return True

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

# create squares
squares = pygame.sprite.Group()
for y in range(8):
    for x in range(8):
        temp = SquareSprite(Square_XY(x,y))
        squares.add(temp)
for s in squares:
    print(s)

# create pieces
white_pieces = generate_pieces("W")
black_pieces = generate_pieces("B")
pieces = white_pieces.copy()
pieces.add(black_pieces)

# peek a square by name or coordinates e.g. "A1" or (0,7)
# returns the first piece found, or None if no pieces are on the square
def peek(square):
    if type(square) == tuple:
        peek_coords = square
    else:
        peek_coords = square_coords(square)

    if not valid_coord(peek_coords):
        return None

    for p in pieces:
        if p.coords == peek_coords:
            return p
    return None

""" 
epawn = peek("e2")
# add black pieces to d3 f3
peek("d7").move("d3")
peek("f7").move("f3")
print([square_name(m) for m in epawn.get_moves()])

peek("a2").move("a6")
peek("c2").move("c6")
print([square_name(m) for m in peek("b7").get_moves()])
"""

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

    
