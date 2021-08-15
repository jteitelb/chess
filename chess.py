import pygame
from typing import Tuple

import board
from util import *
from square import Square
from piece import Piece

WHITE_SQUARE = (255, 231, 184)
BLACK_SQUARE = (179, 133, 91)
HIGHLIGHT_COLOR = (255,255,50)

COLOR_MAP = {0: "W", 1: "B"}
highlighted = []

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

class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, piece):
        super().__init__()
        self.piece = piece
        self.image = pygame.transform.scale(pygame.image.load(self.get_image_filename()), SQUARE_DIMENSIONS)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = self.piece.square.screen_coords

    def get_image_filename(self):
        return f"pieces/{self.piece.color.lower()}{self.piece.piece_type}.png"

    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {self.square.name}"


# create SquareSprites
squares = pygame.sprite.Group()
for y in range(8):
    for x in range(8):
        squares.add(SquareSprite(Square((x,y))))

# create PieceSprites
pieceGroup = pygame.sprite.Group()
for piece in board.pieces:
    pieceGroup.add(PieceSprite(piece))

################################################################

# epawn = Square("e2").peek(pieces)
# # add black pieces to d3 f3
# Square("d7").peek(pieces).move("d3")
# Square("f7").peek(pieces).move("f3")
# print([m.name for m in epawn.get_moves()])

# Square("a2").peek(pieces).move("a6")
# Square("c2").peek(pieces).move("c6")
# print([m.name for m in Square("b7").peek(pieces).get_moves()])

# print([s.name for s in Square("d1").peek(pieces).probe_line((-1,-1))])


if __name__ == "__main__":
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        squares.draw(window)
        pieceGroup.draw(window)
        pygame.display.update()

    
