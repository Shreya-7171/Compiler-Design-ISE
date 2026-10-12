from icg.tac_generator import (
    TACGenerator,
    generate_tac,
    generate_tac_text,
)


def test_generate_tac():
    statements = [
        {"cmd": "START"},
        {"cmd": "MOVE", "direction": "FORWARD", "distance": 10},
        {"cmd": "TURN", "direction": "LEFT"},
        {"cmd": "PICK"},
        {"cmd": "DROP"},
        {"cmd": "WAIT", "duration": 5},
        {"cmd": "END"},
    ]

    instructions = generate_tac(statements)

    assert len(instructions) == 7
    assert str(instructions[0]) == "START"
    assert str(instructions[1]) == "MOVE FORWARD 10"
    assert str(instructions[2]) == "TURN LEFT"
    assert str(instructions[3]) == "PICK"
    assert str(instructions[4]) == "DROP"
    assert str(instructions[5]) == "WAIT 5"
    assert str(instructions[6]) == "END"


def test_generate_tac_text():
    statements = [
        {"cmd": "START"},
        {"cmd": "MOVE", "direction": "BACKWARD", "distance": 20},
        {"cmd": "TURN", "direction": "RIGHT"},
        {"cmd": "END"},
    ]

    result = generate_tac_text(statements)

    expected = """START
MOVE BACKWARD 20
TURN RIGHT
END"""

    assert result == expected


def test_tac_generator_class():
    generator = TACGenerator()

    statements = [
        {"cmd": "START"},
        {"cmd": "PICK"},
        {"cmd": "END"},
    ]

    result = generator.generate_text(statements)

    assert result == """START
PICK
END"""


def test_invalid_command():
    generator = TACGenerator()

    statements = [
        {"cmd": "START"},
        {"cmd": "INVALID"},
    ]

    try:
        generator.generate(statements)
        assert False
    except ValueError as error:
        assert "unsupported command" in str(error)