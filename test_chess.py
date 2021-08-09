from chess import *
import pytest

@pytest.fixture
def supply_squareNames():
    squareNames = list(map(squareName, board_coords))
    return squareNames

def test_squareCoord():
    assert squareCoords("a8") == (0,0)
    assert squareCoords("a1") == (0,7)
    assert squareCoords("H1") == (7,7)
    assert squareCoords("H8") == (7,0)

def test_squareName():
    assert squareName((0,0)) == "a8"
    assert squareName((0,7)) == "a1"
    assert squareName((7,0)) == "h8"
    assert squareName((7,7)) == "h1"

def test_squareCoord2():
    c = (0,0)
    for c in board_coords:
        assert squareCoords(squareName(c)) == c

    with pytest.raises(TypeError):
        squareCoords((3,4))

    badValues = ["", "A", "3", "A ", " 3", "A23", "A0", " A3", "I5", "85", "AE", "%5", "8&", "$@"]
    for val in badValues:
        with pytest.raises(ValueError):
            squareCoords(val)

def test_squareName2(supply_squareNames):
    for s in supply_squareNames:
        assert squareName(squareCoords(s)) == s
    with pytest.raises(TypeError):
        squareName("A1")


