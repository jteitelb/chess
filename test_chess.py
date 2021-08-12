from chess import *
import pytest

@pytest.fixture
def supply_board_coords():
    return [(i,j) for j in range(8) for i in range(8)]

@pytest.fixture
def supply_square_names(supply_board_coords):
    square_names = [Square(coords).name for coords in supply_board_coords]
    return square_names

@pytest.fixture
def black_pieces():
    return generate_pieces("B")

@pytest.fixture
def white_pieces():
    return generate_pieces("W")

def test_generate_pieces(black_pieces, white_pieces):
    assert len(black_pieces) == 16
    assert len(white_pieces) == 16

def test_square_init_by_name():
    assert Square("a8").coords == (0,0)
    assert Square("a1").coords == (0,7)
    assert Square("H1").coords == (7,7)
    assert Square("H8").coords == (7,0)
    assert Square("e4").coords == (4,4)

def test_square_init_by_coord():
    assert Square((0,0)).name == "a8"
    assert Square((0,7)).name == "a1"
    assert Square((7,7)).name == "h1"
    assert Square((7,0)).name == "h8"
    assert Square((4,4)).name == "e4"

@pytest.mark.parametrize("param",
    ["a9", "i1", "s0", "22", "#@",
    (-1,0), (0,-1), (0,8), (8,0), (20,20)])
def test_square_init_invalid_value(param):
    with pytest.raises(ValueError):
        Square(param)

@pytest.mark.parametrize("param",
    [7,(2.3,0), ("a3",), ("a", "3")])
def test_square_init_invalid_type(param):
    with pytest.raises(TypeError):
        Square(param)

def test_square_is_valid():
    assert Square("a1").is_valid()


"""
def test_squareCoord2(supply_board_coords):
    c = (0,0)
    for c in supply_board_coords:
        assert square_coords(square_name(c)) == c

    with pytest.raises(TypeError):
        square_coords((3,4))

    badValues = ["", "A", "3", "A ", " 3", "A23", "A0", " A3", "I5", "85", "AE", "%5", "8&", "$@"]
    for val in badValues:
        with pytest.raises(ValueError):
            square_coords(val)

def test_squareName2(supply_squareNames):
    for s in supply_squareNames:
        assert square_name(square_coords(s)) == s
    with pytest.raises(TypeError):
        square_name("A1")
"""

