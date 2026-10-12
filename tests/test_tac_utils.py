
import os
import sys

# Add the project root folder to Python's search path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from intermediate.tac_utils import format_instruction


def test_format_instruction():
    result = format_instruction("MOVE FORWARD, 10")
    assert result == "MOVE FORWARD, 10"


if __name__ == "__main__":
    test_format_instruction()
    print("TAC utilities test passed!")
