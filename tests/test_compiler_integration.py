
from icg.tac_generator import generate_tac_text_from_source


def test_full_source_to_tac_pipeline():
    source = """START
MOVE FORWARD 10
TURN LEFT
PICK
WAIT 4
DROP
END"""

    expected = """START
MOVE FORWARD 10
TURN LEFT
PICK
WAIT 4
DROP
END"""

    assert generate_tac_text_from_source(source) == expected


def test_invalid_program_does_not_generate_tac():
    source = """START
DROP
END"""

    try:
        generate_tac_text_from_source(source)
        assert False, "Expected semantic analysis to reject DROP without PICK"
    except Exception as error:
        assert "DROP" in str(error)
