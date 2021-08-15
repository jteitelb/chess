from piece import Piece
from square import Square


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

    result = [Piece(color, piece, (x, back_rank)) for x, piece in enumerate(pieces)]
    result += [Piece(color, "P", (x, front_line)) for x in range(8)]
    return result

# create pieces
white_pieces = generate_pieces("W")
black_pieces = generate_pieces("B")
pieces = white_pieces + black_pieces


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
