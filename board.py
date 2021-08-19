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

# probe in a straight line given a direction e.g. (0,1) will probe downward
# return a list of squares on the board in the direction probed up to and including the first non-empty square
def probe_line(piece, direction):
    (dx, dy) = direction
    results = []
    current = piece.square
    while True:
        try:
            current = current.relative(dx, dy)
        except ValueError:
            break
        results.append(current)
        if peek(current) != None:
            break
    return results

def probe_multi(piece, directions):
    res = []
    for d in directions:
        res += probe_line(piece, d)

def get_moves(piece):
    if piece.piece_type == "P":
        return get_pawn_moves(piece)

# TODO: promotions and en passant
def get_pawn_moves(piece):
    moves = []
    if piece.color == "W":
        single_move = piece.square.relative(0,-1)
        double_move = piece.square.relative(0,-2)
    elif piece.color == "B":
        single_move = piece.square.relative(0,1)
        double_move = piece.square.relative(0,2)
    else:
        raise ValueError("unexpected color")

    if peek(single_move) == None:
        moves.append(single_move)
        if peek(double_move) == None:
            moves.append(double_move)
    
    # captures
    (x,y) = single_move.coords
    l_capture = Square((x-1, y))
    r_capture = Square((x+1, y))
    l_piece = peek(l_capture)
    r_piece = peek(r_capture)
    if l_piece != None and l_piece.color != piece.color:
        moves.append(l_capture)
    if r_piece != None and r_piece.color != piece.color:
        moves.append(r_capture)

    return moves
