import sys
import os

# Allow Python to find the project modules
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from lexer.lexer import Lexer
from semantic.semantic_analyzer import (
    SemanticAnalyzer,
    SemanticError
)


def make_tokens(source):
    lexer = Lexer(source)
    return lexer.tokenize()

# Valid program

def test_valid_program():
    source = """START
MOVE FORWARD 10
MOVE BACKWARD 5
TURN LEFT
TURN RIGHT
PICK
WAIT 2
DROP
END"""

    tokens = make_tokens(source)

    analyzer = SemanticAnalyzer(tokens)

    assert analyzer.analyze() is True

    print(" Valid program test passed")


# Invalid MOVE direction

def test_invalid_move_direction():
    source = """START
MOVE LEFT 10
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" Invalid MOVE direction test passed")


# MOVE without NUMBER

def test_move_without_number():
    source = """START
MOVE FORWARD
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" MOVE without NUMBER test passed")


# Invalid TURN direction

def test_invalid_turn_direction():
    source = """START
TURN FORWARD
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" Invalid TURN direction test passed")


# WAIT without NUMBER

def test_wait_without_number():
    source = """START
WAIT
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" WAIT without NUMBER test passed")


# Invalid token

def test_invalid_token():
    source = """START
MOVE FORWARD 10
XYZ
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" INVALID token test passed")



# Missing START

def test_missing_start():
    source = """MOVE FORWARD 10
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" Missing START test passed")



# Missing END

def test_missing_end():
    source = """START
MOVE FORWARD 10"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" Missing END test passed")



# NEWLINE check

def test_missing_newline():
    source = """START
MOVE FORWARD 10 TURN LEFT
END"""

    tokens = make_tokens(source)

    try:
        SemanticAnalyzer(tokens).analyze()
        assert False, "Expected SemanticError"

    except SemanticError:
        print(" Missing NEWLINE test passed")



# Run all tests

if __name__ == "__main__":

    test_valid_program()

    test_invalid_move_direction()
    test_move_without_number()

    test_invalid_turn_direction()

    test_wait_without_number()

    test_invalid_token()

    test_missing_start()
    test_missing_end()

    test_missing_newline()

    print("\nAll Member 2 Semantic Analyzer tests passed!")