# from piece import Piece
from square import Square

pieces = []

# get the piece on a given square
# takes square or name or coordinates e.g. "A1" or (0,7)
# returns the first piece found, or None if empty or invalid
def peek(square):
    if type(square) != Square:
        square = Square(square)
    if not square.is_valid():
        return None
    for p in pieces:
        if p.square.coords == square.coords:
            return p
    return None
