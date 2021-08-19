from util import *

from square import Square, squareify

class Piece:
    def __init__(self, color, piece_type, square):
        self.color = color
        self.piece_type = piece_type
        self.square = squareify(square)

    def move(self, square):
        if type(square) != Square:
            square = Square(square)
        self.square = square
        # (self.rect.x, self.rect.y) = self.square.screen_coords

    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {self.square.name}"
    
    def __repr__(self):
        return str(self)
