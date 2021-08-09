state = [[None for i in range(8)] for j in range(8)]

def peek(coord):
    (x,y) = coord
    return state[y][x]

def insert(piece, coord):
    (x,y) = coord
    replaced = state[y][x]
    state[y][x] = piece
    return replaced

def show_board():
    for row in state:
        print(row)

# show_board()
# print(insert("x", (0,0)))
# show_board()