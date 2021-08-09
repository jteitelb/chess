import pygame
from typing import Tuple

def squareCoord(strCoord: str) -> Tuple[int, int]:
    if not type(strCoord) is str:
        raise TypeError("expeced string")
    if len(strCoord) != 2:
        raise ValueError("expected 2 characters")
    (s_file, s_rank) = strCoord
    s_file = s_file.upper()
    if s_file < "A" or s_file > "H":
        raise ValueError("invalid file")

    if s_rank < "1" or s_rank > "8":
        raise ValueError("invalid rank")

    xVal = ord(s_file) - ord('A')
    yVal = 8 - int(s_rank)
    return (xVal, yVal)

def squareName(coordinate: Tuple[int, int]) -> str:
    if not type(coordinate) is tuple:
        raise TypeError("expected tuple")

    (x,y) = coordinate
    if x < 0 or x > 7 or y < 0 or y > 7:
        raise ValueError("invalid x or y coordinate")
    letter = chr(x + ord('A'))
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

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (self.x + self.y) % 2
        self.image = pygame.Surface(SQUARE_DIMENSIONS)
        
        if (x,y) in highlighted:
            self.image.fill(HIGHLIGHT_COLOR)
            # print(squareName((s_file, s_rank)), (s_file, s_rank))
        elif self.color:
            self.image.fill(BLACK_SQUARE)
        else:
            self.image.fill(WHITE_SQUARE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * SQUARE_SIZE
        self.rect.y = self.y * SQUARE_SIZE

    def name(self):
        return squareName((self.x, self.y))

    def __str__(self):
        return f"{self.name()}: {C_MAP[self.color]}"

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, pieceType, coords):
        super().__init__()
        self.color = color
        self.pieceType = pieceType
        self.coords = coords
        self.image = pygame.transform.scale(pygame.image.load(self.getImageFile()), SQUARE_DIMENSIONS)
        self.rect = self.image.get_rect()
        (self.rect.x, self.rect.y) = board_to_screen(self.coords)

    def getImageFile(self):
        return f"pieces/{self.color.lower()}{self.pieceType}.png"

    def draw(self):
        window.blit(self.image, board_to_screen(self.coords))


def generatePieces(color):
    if color == "W":
        backRank = 7
        frontLine = 6
    elif color == "B":
        backRank = 0
        frontLine = 1
    else:
        raise ValueError("invalid color")

    pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]

    result = pygame.sprite.Group()
    for x, piece in enumerate(pieces):
        tmp = Piece(color, piece, (x, backRank))
        result.add(tmp)
    for x in range(8):
        tmp = Piece(color, "P", (x, frontLine))
        result.add(tmp)
    return result

# whitePawn = Piece("W","P", (0,6))

board = [(i,j) for j in range(8) for i in range(8)]

squares = pygame.sprite.Group()
for s in board:
    temp = Square(s[0], s[1])
    # print(temp.rank, temp.file, temp.color, temp.rgbval, temp.rect.x, temp.rect.y)
    squares.add(temp)

white_pieces = generatePieces("W")
black_pieces = generatePieces("B")

if __name__ == "__main__":
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    running = True
    while running:
        #window.fill((100,255,255))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        squares.draw(window)
        white_pieces.draw(window)
        black_pieces.draw(window)
        pygame.display.update()

    
