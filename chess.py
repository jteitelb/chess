import pygame
from typing import Tuple

import board
from util import *
from square import Square

WHITE_SQUARE = (255, 231, 184)
BLACK_SQUARE = (179, 133, 91)
HIGHLIGHT_COLOR = (255,255,50)

COLOR_MAP = {0: "W", 1: "B"}
highlighted = []

""" 
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
 """

class SquareSprite(pygame.sprite.Sprite):
    def __init__(self, square):
        super().__init__()
        self.square = square
        self.color = COLOR_MAP[(self.square.x + self.square.y) % 2]
        self.image = pygame.Surface(SQUARE_DIMENSIONS)
        
        if (square.x,square.y) in highlighted:
            self.image.fill(HIGHLIGHT_COLOR)
        elif self.color == "B":
            self.image.fill(BLACK_SQUARE)
        elif self.color == "W":
            self.image.fill(WHITE_SQUARE)
        else:
            raise ValueError("Unexpected Color")
        self.rect = self.image.get_rect()
        self.rect.x = self.square.x * SQUARE_SIZE
        self.rect.y = self.square.y * SQUARE_SIZE

    def __repr__(self):
        return f"{self.square.name}: {self.color}"

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, piece_type, square):
        super().__init__()
        self.color = color
        self.piece_type = piece_type
        self.square = Square(square)
        self.image = pygame.transform.scale(pygame.image.load(self.get_image_filename()), SQUARE_DIMENSIONS)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = self.square.screen_coords

    def move(self, square):
        if type(square) != Square:
            square = Square(square)
        self.square = square
        (self.rect.x, self.rect.y) = self.square.screen_coords

    def get_image_filename(self):
        return f"pieces/{self.color.lower()}{self.piece_type}.png"

    # probe in a straight line given a direction e.g. (0,1) will probe downward
    # return a list of squares on the board in the direction probed up to and including the first non-empty square
    def probe_line(self, direction):
        (dx, dy) = direction
        results = []
        current = self.square
        while True:
            try:
                current = current.relative(dx, dy)
            except ValueError:
                break
            results.append(current)
            if current.peek(pieces) != None:
                break
        return results
    
    def probe_multi(self, directions):
        res = []
        for d in directions:
            res += self.probe_line(d)

    def get_moves(self):
        if self.piece_type == "P":
            return self.get_pawn_moves()

    # TODO: promotions and en passant
    def get_pawn_moves(self):
        moves = []
        if self.color == "W":
            single_move = self.square.relative(0,-1)
            double_move = self.square.relative(0,-2)
        elif self.color == "B":
            single_move = self.square.relative(0,1)
            double_move = self.square.relative(0,2)
        else:
            raise ValueError("unexpected color")

        if single_move.peek(pieces) == None:
            moves.append(single_move)
            if double_move.peek(pieces) == None:
                moves.append(double_move)
        
        # captures
        (x,y) = single_move.coords
        l_capture = Square((x-1, y))
        r_capture = Square((x+1, y))
        l_piece = l_capture.peek(pieces)
        r_piece = r_capture.peek(pieces)
        if l_piece != None and l_piece.color != self.color:
            moves.append(l_capture)
        if r_piece != None and r_piece.color != self.color:
            moves.append(r_capture)

        return moves

    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {self.square.name}"

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


# create squares
squares = pygame.sprite.Group()
for y in range(8):
    for x in range(8):
        temp = SquareSprite(Square((x,y)))
        squares.add(temp)

# create pieces
white_pieces = generate_pieces("W")
black_pieces = generate_pieces("B")
pieces = white_pieces.copy()
pieces.add(black_pieces)

################################################################

epawn = Square("e2").peek(pieces)
# add black pieces to d3 f3
Square("d7").peek(pieces).move("d3")
Square("f7").peek(pieces).move("f3")
print([m.name for m in epawn.get_moves()])

Square("a2").peek(pieces).move("a6")
Square("c2").peek(pieces).move("c6")
print([m.name for m in Square("b7").peek(pieces).get_moves()])

print([s.name for s in Square("d1").peek(pieces).probe_line((-1,-1))])


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

    
