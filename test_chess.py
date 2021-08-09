from chess import *
import pytest

@pytest.fixture
def supply_squareNames():
    squareNames = list(map(square_name, board_coords))
    return squareNames

def test_squareCoord():
    assert square_coords("a8") == (0,0)
    assert square_coords("a1") == (0,7)
    assert square_coords("H1") == (7,7)
    assert square_coords("H8") == (7,0)

def test_squareName():
    assert square_name((0,0)) == "a8"
    assert square_name((0,7)) == "a1"
    assert square_name((7,0)) == "h8"
    assert square_name((7,7)) == "h1"

def test_squareCoord2():
    c = (0,0)
    for c in board_coords:
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


