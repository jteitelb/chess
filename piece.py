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
        (self.rect.x, self.rect.y) = self.square.screen_coords

    # probe in a straight line given a direction e.g. (0,1) will probe downward
    # return a list of squares on the board in the direction probed up to and including the first non-empty square
    
    # def probe_line(self, direction):
    #     (dx, dy) = direction
    #     results = []
    #     current = self.square
    #     while True:
    #         try:
    #             current = current.relative(dx, dy)
    #         except ValueError:
    #             break
    #         results.append(current)
    #         if current.peek(pieces) != None:
    #             break
    #     return results
    
    # def probe_multi(self, directions):
    #     res = []
    #     for d in directions:
    #         res += self.probe_line(d)

    # def get_moves(self):
    #     if self.piece_type == "P":
    #         return self.get_pawn_moves()

    # TODO: promotions and en passant
    # def get_pawn_moves(self):
    #     moves = []
    #     if self.color == "W":
    #         single_move = self.square.relative(0,-1)
    #         double_move = self.square.relative(0,-2)
    #     elif self.color == "B":
    #         single_move = self.square.relative(0,1)
    #         double_move = self.square.relative(0,2)
    #     else:
    #         raise ValueError("unexpected color")

    #     if single_move.peek(pieces) == None:
    #         moves.append(single_move)
    #         if double_move.peek(pieces) == None:
    #             moves.append(double_move)
        
    #     # captures
    #     (x,y) = single_move.coords
    #     l_capture = Square((x-1, y))
    #     r_capture = Square((x+1, y))
    #     l_piece = l_capture.peek(pieces)
    #     r_piece = r_capture.peek(pieces)
    #     if l_piece != None and l_piece.color != self.color:
    #         moves.append(l_capture)
    #     if r_piece != None and r_piece.color != self.color:
    #         moves.append(r_capture)

    #     return moves

    def __str__(self):
        return f"{self.color.lower()}{self.piece_type} {self.square.name}"
    
    def __repr__(self):
        return str(self)
