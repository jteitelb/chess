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

    def __repr__(self):
        return f"PieceSprite:{self.piece.color.lower()}{self.piece.piece_type} {self.piece.square.name}"


    def update(self):
        (self.rect.x, self.rect.y) = self.piece.square.screen_coords


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

epawn = board.peek("e2")
# add black pieces to d3 f3
board.peek("d7").move("d3")
board.peek("f7").move("f3")
print([m.name for m in board.get_moves(epawn)])

board.peek("a2").move("a6")
board.peek("c2").move("c6")
print([m.name for m in board.get_moves(board.peek("b7"))])

print([s.name for s in board.probe_line(board.peek("d1"), (-1,-1))])

clickedPiece = None

if __name__ == "__main__":
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (x,y) = pos
                clicked = Square((x//SQUARE_SIZE, y//SQUARE_SIZE))
                if clickedPiece == None:
                    clickedPiece = board.peek(clicked)
                    print(clicked.name)
                else:
                    captured = board.peek(clicked)
                    print(captured)
                    print(type(captured))
                    if captured != None:
                        for p in pieceGroup:
                            if p.piece == captured:
                                p.kill()
                    clickedPiece.move(clicked)
                    clickedPiece = None


        

        squares.draw(window)
        pieceGroup.draw(window)
        pieceGroup.update()
        
        pygame.display.update()

    
