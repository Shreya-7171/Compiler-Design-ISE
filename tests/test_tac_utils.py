
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from intermediate.tac_utils import format_instruction, format_instructions
from icg.intermediate_code import TACInstruction


def test_format_instruction():
    instruction = TACInstruction("MOVE", "FORWARD", 10)
    assert format_instruction(instruction) == "MOVE FORWARD 10"


def test_format_instructions():
    instructions = [
        TACInstruction("START"),
        TACInstruction("MOVE", "FORWARD", 10),
        TACInstruction("END"),
    ]

    assert format_instructions(instructions) == (
        "START\n"
        "MOVE FORWARD 10\n"
        "END"
    )


def test_format_empty_instructions():
    assert format_instructions([]) == ""


if __name__ == "__main__":
    test_format_instruction()
    test_format_instructions()
    test_format_empty_instructions()
    print("TAC utilities tests passed!")
