from chess import *
import pytest

@pytest.fixture
def supply_squareNames():
    squareNames = list(map(squareName, board))
    return squareNames

def test_squareCoord():
    assert squareCoord("A8") == (0,0)
    assert squareCoord("A1") == (0,7)
    assert squareCoord("H1") == (7,7)
    assert squareCoord("H8") == (7,0)

def test_squareName():
    assert squareName((0,0)) == "A8"
    assert squareName((0,7)) == "A1"
    assert squareName((7,0)) == "H8"
    assert squareName((7,7)) == "H1"

def test_squareCoord2():
    c = (0,0)
    for c in board:
        assert squareCoord(squareName(c)) == c

    with pytest.raises(TypeError):
        squareCoord((3,4))

    badValues = ["", "A", "3", "A ", " 3", "A23", "A0", " A3", "I5", "85", "AE", "%5", "8&", "$@"]
    for val in badValues:
        with pytest.raises(ValueError):
            squareCoord(val)

def test_squareName2(supply_squareNames):
    for s in supply_squareNames:
        assert squareName(squareCoord(s)) == s
    with pytest.raises(TypeError):
        squareName("A1")


