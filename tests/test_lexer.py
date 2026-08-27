

from lexer.lexer import Lexer
from lexer import rcl_token as rcl_token_


def test_basic_commands():
    source = """
    START
    MOVE 10
    FORWARD 5
    TURN LEFT
    END
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    token_types = [token.type for token in tokens]

    assert rcl_token_.TokenType.START in token_types
    assert rcl_token_.TokenType.MOVE in token_types
    assert rcl_token_.TokenType.FORWARD in token_types
    assert rcl_token_.TokenType.TURN in token_types
    assert rcl_token_.TokenType.LEFT in token_types
    assert rcl_token_.TokenType.END in token_types


def test_numbers():
    source = "MOVE 10"

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    assert any(
        token.type == rcl_token_.TokenType.NUMBER and token.value == 10
        for token in tokens
    )


def test_robot_commands():
    source = """
    START
    MOVE 20
    FORWARD 10
    BACKWARD 5
    TURN RIGHT
    PICK
    DROP
    WAIT
    END
    """

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    token_types = [token.type for token in tokens]

    assert rcl_token_.TokenType.START in token_types
    assert rcl_token_.TokenType.MOVE in token_types
    assert rcl_token_.TokenType.FORWARD in token_types
    assert rcl_token_.TokenType.BACKWARD in token_types
    assert rcl_token_.TokenType.TURN in token_types
    assert rcl_token_.TokenType.RIGHT in token_types
    assert rcl_token_.TokenType.PICK in token_types
    assert rcl_token_.TokenType.DROP in token_types
    assert rcl_token_.TokenType.WAIT in token_types
    assert rcl_token_.TokenType.END in token_types