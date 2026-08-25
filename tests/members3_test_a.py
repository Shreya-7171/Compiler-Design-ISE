import sys
import os

# Allow Python to find parser_part_a.py
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "parser")
    )
)

from parser_part_a import ParserPartA


# Fake Token class for testing
class Token:
    def __init__(self, token_type, value=None, line=1, column=1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column


# TEST 1: START

def test_start():
    tokens = [
        Token("START", "START", 1, 1)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_start()

    assert result is True

    print(" START test passed")

# TEST 2: END
#
def test_end():
    tokens = [
        Token("END", "END", 1, 1)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_end()

    assert result is True

    print(" END test passed")


# TEST 3: MOVE FORWARD NUMBER

def test_move_forward():
    tokens = [
        Token("MOVE", "MOVE", 1, 1),
        Token("FORWARD", "FORWARD", 1, 6),
        Token("NUMBER", 10, 1, 14)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_move()

    assert result is True

    print("MOVE FORWARD NUMBER test passed")

# TEST 4: MOVE BACKWARD NUMBER

def test_move_backward():
    tokens = [
        Token("MOVE", "MOVE", 1, 1),
        Token("BACKWARD", "BACKWARD", 1, 6),
        Token("NUMBER", 5, 1, 15)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_move()

    assert result is True

    print("✓ MOVE BACKWARD NUMBER test passed")


# TEST 5: TURN LEFT

def test_turn_left():
    tokens = [
        Token("TURN", "TURN", 1, 1),
        Token("LEFT", "LEFT", 1, 6)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_turn()

    assert result is True

    print("✓ TURN LEFT test passed")


# TEST 6: TURN RIGHT

def test_turn_right():
    tokens = [
        Token("TURN", "TURN", 1, 1),
        Token("RIGHT", "RIGHT", 1, 6)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_turn()

    assert result is True

    print("✓ TURN RIGHT test passed")


# TEST 7: NEWLINE

def test_newline():
    tokens = [
        Token("NEWLINE", "\n", 1, 1)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_newline()

    assert result is True

    print("✓ NEWLINE test passed")


# TEST 8: EOF

def test_eof():
    tokens = [
        Token("EOF", None, 1, 1)
    ]

    parser = ParserPartA(tokens)

    result = parser.parse_eof()

    assert result is True

    print("✓ EOF test passed")


# TEST 9: INVALID TOKEN

def test_invalid():
    tokens = [
        Token("INVALID", "@", 1, 1)
    ]

    parser = ParserPartA(tokens)

    try:
        parser.parse_invalid()
        assert False
    except SyntaxError:
        print("✓ INVALID token test passed")

# TEST 10: INVALID MOVE DIRECTION

def test_invalid_move_direction():
    tokens = [
        Token("MOVE", "MOVE", 1, 1),
        Token("LEFT", "LEFT", 1, 6),
        Token("NUMBER", 10, 1, 11)
    ]

    parser = ParserPartA(tokens)

    try:
        parser.parse_move()
        assert False
    except SyntaxError:
        print("✓ Invalid MOVE direction test passed")


# TEST 11: MOVE WITHOUT NUMBER

def test_move_without_number():
    tokens = [
        Token("MOVE", "MOVE", 1, 1),
        Token("FORWARD", "FORWARD", 1, 6)
    ]

    parser = ParserPartA(tokens)

    try:
        parser.parse_move()
        assert False
    except (SyntaxError, IndexError):
        print("✓ MOVE without NUMBER test passed")


# TEST 12: INVALID TURN DIRECTION

def test_invalid_turn():
    tokens = [
        Token("TURN", "TURN", 1, 1),
        Token("FORWARD", "FORWARD", 1, 6)
    ]

    parser = ParserPartA(tokens)

    try:
        parser.parse_turn()
        assert False
    except SyntaxError:
        print("✓ Invalid TURN direction test passed")


# RUN ALL TESTS

if __name__ == "__main__":

    test_start()
    test_end()

    test_move_forward()
    test_move_backward()

    test_turn_left()
    test_turn_right()

    test_newline()
    test_eof()
    test_invalid()

    test_invalid_move_direction()
    test_move_without_number()
    test_invalid_turn()

    print("\nAll Parser Part A tests passed!")