from util import *

def squareify(maybeSquare):
    if type(maybeSquare) == Square:
        square = maybeSquare
    else:
        square = Square(maybeSquare)
    return square

class Square:
    def __init__(self, square):
        if type(square) == tuple:
            if len(square) != 2:
                raise TypeError("Square expects 2 coordinates")
            (x,y) = square
            if type(x) != int or type(y) != int:
                raise TypeError("Square expects integers when tuple given")
            (self.x, self.y) = square
        elif type(square) == str:
            (f, r) = square
            self.x = ord(f.lower()) - ord('a')
            self.y = (8 - int(r))
        else:
            raise TypeError("Expected tuple or str")
            
        if not self.is_valid():
            raise ValueError("Attempted to create invalid Square")
    @property
    def coords(self):
        return (self.x, self.y)
    @property
    def s_file(self):
        return chr(self.x + ord('a'))
    @property
    def s_rank(self):
        return (8 - self.y)
    @property
    def name(self):
        return f"{self.s_file}{self.s_rank}"
    @property
    def screen_coords(self):
        return (SQUARE_SIZE * self.x, SQUARE_SIZE * self.y)

    def is_valid(self):
        (x,y) = self.coords
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        return True
    
    # TODO: take out of square class
    def peek(self, pieces):
        if not self.is_valid():
            return None
        for p in pieces:
            if p.square.coords == self.coords:
                return p
        return None
    
    def relative(self, dx, dy):
        return Square((self.x + dx, self.y + dy))

    def __repr__(self):
        return f"({self.x},{self.y})"