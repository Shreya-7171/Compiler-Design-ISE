import sys
import os

# Allows Python to find parser_part_b.py
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "parser")
    )
)

from parser_part_b import ParserPartB


# Fake token class for testing
class Token:
    def __init__(self, token_type, value=None, line=1, column=1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column


# ------------------------------------------------
# TEST 1: PICK
# ------------------------------------------------

def test_pick():
    tokens = [
        Token("PICK", "PICK", 1, 1)
    ]

    parser = ParserPartB(tokens)

    result = parser.parse_pick()

    assert result == True

    print("✓ PICK test passed")


# ------------------------------------------------
# TEST 2: DROP
# ------------------------------------------------

def test_drop():
    tokens = [
        Token("DROP", "DROP", 1, 1)
    ]

    parser = ParserPartB(tokens)

    result = parser.parse_drop()

    assert result == True

    print("✓ DROP test passed")


# ------------------------------------------------
# TEST 3: WAIT with NUMBER
# ------------------------------------------------

def test_wait():
    tokens = [
        Token("WAIT", "WAIT", 1, 1),
        Token("NUMBER", 5, 1, 6)
    ]

    parser = ParserPartB(tokens)

    result = parser.parse_wait()

    assert result == True

    print("✓ WAIT test passed")


# ------------------------------------------------
# TEST 4: Invalid PICK
# ------------------------------------------------

def test_invalid_pick():
    tokens = [
        Token("DROP", "DROP", 1, 1)
    ]

    parser = ParserPartB(tokens)

    try:
        parser.parse_pick()
        assert False

    except SyntaxError:
        print("✓ Invalid PICK test passed")


# ------------------------------------------------
# TEST 5: Invalid DROP
# ------------------------------------------------

def test_invalid_drop():
    tokens = [
        Token("PICK", "PICK", 1, 1)
    ]

    parser = ParserPartB(tokens)

    try:
        parser.parse_drop()
        assert False

    except SyntaxError:
        print("✓ Invalid DROP test passed")


# ------------------------------------------------
# TEST 6: WAIT without NUMBER
# ------------------------------------------------

def test_invalid_wait():
    tokens = [
        Token("WAIT", "WAIT", 1, 1),
        Token("LEFT", "LEFT", 1, 6)
    ]

    parser = ParserPartB(tokens)

    try:
        parser.parse_wait()
        assert False

    except SyntaxError:
        print("✓ Invalid WAIT test passed")


# ------------------------------------------------
# RUN ALL TESTS
# ------------------------------------------------

if __name__ == "__main__":

    test_pick()
    test_drop()
    test_wait()

    test_invalid_pick()
    test_invalid_drop()
    test_invalid_wait()

    print("\nAll Member 3 parser tests passed!")