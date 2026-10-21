"""Unit tests for TargetInstruction representation (Phase 7 - Member 1)."""

import pytest
from dataclasses import FrozenInstanceError

from codegen import (
    SUPPORTED_MOVE_DIRECTIONS,
    SUPPORTED_OPCODES,
    SUPPORTED_TURN_DIRECTIONS,
    TargetInstruction,
)
from icg.intermediate_code import TACInstruction


# ---------------------------------------------------------------------------
# 1. Creation of a TargetInstruction
# ---------------------------------------------------------------------------
def test_creation_of_target_instruction():
    """Verify that TargetInstruction correctly stores opcode and operands."""
    instruction = TargetInstruction("MOVE", "FORWARD", 10)

    assert instruction.opcode == "MOVE"
    assert instruction.operand1 == "FORWARD"
    assert instruction.operand2 == 10
    assert instruction.result is None

    # Test property aliases for compatibility
    assert instruction.operator == "MOVE"
    assert instruction.arg1 == "FORWARD"
    assert instruction.arg2 == 10

    # Test dictionary export
    assert instruction.to_dict() == {
        "opcode": "MOVE",
        "operand1": "FORWARD",
        "operand2": 10,
        "result": None,
    }


def test_target_instruction_is_immutable():
    """Ensure TargetInstruction instances are frozen and cannot be mutated."""
    instruction = TargetInstruction("START")
    with pytest.raises(FrozenInstanceError):
        instruction.opcode = "END"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# 2. Formatting of START and END
# ---------------------------------------------------------------------------
def test_formatting_of_start_and_end():
    """Verify string formatting of START and END."""
    start_instruction = TargetInstruction("START")
    end_instruction = TargetInstruction("END")

    assert str(start_instruction) == "START"
    assert str(end_instruction) == "END"


# ---------------------------------------------------------------------------
# 3. Formatting of MOVE FORWARD 10
# ---------------------------------------------------------------------------
def test_formatting_of_move_forward_10():
    """Verify string formatting of MOVE FORWARD 10."""
    instruction = TargetInstruction("MOVE", "FORWARD", 10)
    assert str(instruction) == "MOVE FORWARD 10"


# ---------------------------------------------------------------------------
# 4. Formatting of MOVE BACKWARD 5
# ---------------------------------------------------------------------------
def test_formatting_of_move_backward_5():
    """Verify string formatting of MOVE BACKWARD 5."""
    instruction = TargetInstruction("MOVE", "BACKWARD", 5)
    assert str(instruction) == "MOVE BACKWARD 5"


# ---------------------------------------------------------------------------
# 5. Formatting of TURN LEFT and TURN RIGHT
# ---------------------------------------------------------------------------
def test_formatting_of_turn_left_and_right():
    """Verify string formatting of TURN LEFT and TURN RIGHT."""
    turn_left = TargetInstruction("TURN", "LEFT")
    turn_right = TargetInstruction("TURN", "RIGHT")

    assert str(turn_left) == "TURN LEFT"
    assert str(turn_right) == "TURN RIGHT"


# ---------------------------------------------------------------------------
# 6. Formatting of WAIT 5
# ---------------------------------------------------------------------------
def test_formatting_of_wait_5():
    """Verify string formatting of WAIT 5."""
    instruction = TargetInstruction("WAIT", 5)
    assert str(instruction) == "WAIT 5"


# ---------------------------------------------------------------------------
# 7. Formatting of PICK and DROP
# ---------------------------------------------------------------------------
def test_formatting_of_pick_and_drop():
    """Verify string formatting of PICK and DROP."""
    pick = TargetInstruction("PICK")
    drop = TargetInstruction("DROP")

    assert str(pick) == "PICK"
    assert str(drop) == "DROP"


# ---------------------------------------------------------------------------
# 8. Instructions with optional operands
# ---------------------------------------------------------------------------
def test_instructions_with_optional_operands_default_to_none():
    """Verify default operand values when optional operands are omitted."""
    start = TargetInstruction("START")
    assert start.operand1 is None
    assert start.operand2 is None
    assert start.result is None

    turn = TargetInstruction("TURN", "LEFT")
    assert turn.operand2 is None
    assert turn.result is None

    wait = TargetInstruction("WAIT", 5)
    assert wait.operand2 is None
    assert wait.result is None

    move = TargetInstruction("MOVE", "FORWARD", 10)
    assert move.result is None


def test_instructions_with_explicit_none_operands():
    """Verify that explicitly passing None for optional operands works."""
    instruction = TargetInstruction("MOVE", "FORWARD", 10, result=None)
    assert instruction.result is None
    assert str(instruction) == "MOVE FORWARD 10"

    wait = TargetInstruction("WAIT", 5, operand2=None, result=None)
    assert str(wait) == "WAIT 5"


def test_instructions_with_keyword_arguments():
    """Verify instantiation using keyword arguments."""
    instruction = TargetInstruction(opcode="WAIT", operand1=3)
    assert instruction.opcode == "WAIT"
    assert instruction.operand1 == 3
    assert instruction.operand2 is None
    assert str(instruction) == "WAIT 3"


# ---------------------------------------------------------------------------
# 9. Consistent output formatting
# ---------------------------------------------------------------------------
def test_deterministic_and_clean_formatting():
    """Verify that string output contains no 'None', no commas, and no extra whitespace."""
    instructions = [
        TargetInstruction("START"),
        TargetInstruction("MOVE", "FORWARD", 10),
        TargetInstruction("TURN", "LEFT"),
        TargetInstruction("PICK"),
        TargetInstruction("WAIT", 5),
        TargetInstruction("DROP"),
        TargetInstruction("MOVE", "BACKWARD", 5),
        TargetInstruction("TURN", "RIGHT"),
        TargetInstruction("END"),
    ]

    for instruction in instructions:
        text = str(instruction)
        # Multiple conversions return the identical string
        assert str(instruction) == text
        # No 'None' anywhere in the output
        assert "None" not in text
        # No commas in output
        assert "," not in text
        # No leading or trailing whitespace
        assert text == text.strip()
        # No consecutive whitespace
        assert "  " not in text


def test_case_normalization_in_formatting():
    """Verify that lowercase opcodes and directions normalize to uppercase."""
    move = TargetInstruction("move", "forward", 10)
    turn = TargetInstruction("turn", "right")

    assert move.opcode == "MOVE"
    assert move.operand1 == "FORWARD"
    assert str(move) == "MOVE FORWARD 10"

    assert turn.opcode == "TURN"
    assert turn.operand1 == "RIGHT"
    assert str(turn) == "TURN RIGHT"


def test_float_operands_format_cleanly():
    """Verify formatting with float distance or duration."""
    move = TargetInstruction("MOVE", "FORWARD", 12.5)
    wait = TargetInstruction("WAIT", 1.5)

    assert str(move) == "MOVE FORWARD 12.5"
    assert str(wait) == "WAIT 1.5"


# ---------------------------------------------------------------------------
# 10. Appropriate handling of invalid input
# ---------------------------------------------------------------------------
def test_invalid_opcode_type_raises_type_error():
    """Opcode must be a string."""
    with pytest.raises(TypeError, match="Opcode must be a string"):
        TargetInstruction(123)  # type: ignore[arg-type]


def test_empty_opcode_raises_value_error():
    """Empty or whitespace-only opcode is rejected."""
    with pytest.raises(ValueError, match="Opcode cannot be empty"):
        TargetInstruction("")

    with pytest.raises(ValueError, match="Opcode cannot be empty"):
        TargetInstruction("   ")


def test_unsupported_opcode_raises_value_error():
    """Opcodes outside the supported RCL set are rejected."""
    with pytest.raises(ValueError, match="Unsupported opcode 'FLY'"):
        TargetInstruction("FLY")


def test_move_validation_errors():
    """Validate MOVE operand constraints."""
    # Missing direction
    with pytest.raises(ValueError, match="MOVE instruction requires direction"):
        TargetInstruction("MOVE", None, 10)

    # Invalid direction
    with pytest.raises(ValueError, match="Unsupported MOVE direction 'UP'"):
        TargetInstruction("MOVE", "UP", 10)

    # Missing distance
    with pytest.raises(ValueError, match="MOVE instruction requires distance"):
        TargetInstruction("MOVE", "FORWARD")

    # Non-positive distance (<= 0)
    with pytest.raises(ValueError, match="MOVE distance must be a positive number"):
        TargetInstruction("MOVE", "FORWARD", 0)

    with pytest.raises(ValueError, match="MOVE distance must be a positive number"):
        TargetInstruction("MOVE", "FORWARD", -5)

    with pytest.raises(ValueError, match="MOVE distance must be a positive number"):
        TargetInstruction("MOVE", "FORWARD", "-10")

    # Boolean passed as distance
    with pytest.raises(TypeError, match="MOVE distance cannot be a boolean"):
        TargetInstruction("MOVE", "FORWARD", True)


def test_turn_validation_errors():
    """Validate TURN operand constraints."""
    # Missing direction
    with pytest.raises(ValueError, match="TURN instruction requires direction"):
        TargetInstruction("TURN")

    # Invalid direction
    with pytest.raises(ValueError, match="Unsupported TURN direction 'FORWARD'"):
        TargetInstruction("TURN", "FORWARD")

    # Unexpected second operand
    with pytest.raises(ValueError, match="TURN instruction does not accept operand2"):
        TargetInstruction("TURN", "LEFT", 10)


def test_wait_validation_errors():
    """Validate WAIT operand constraints."""
    # Missing duration
    with pytest.raises(ValueError, match="WAIT instruction requires duration"):
        TargetInstruction("WAIT")

    # Non-positive duration (<= 0)
    with pytest.raises(ValueError, match="WAIT duration must be a positive number"):
        TargetInstruction("WAIT", 0)

    with pytest.raises(ValueError, match="WAIT duration must be a positive number"):
        TargetInstruction("WAIT", -2.5)

    # Boolean passed as duration
    with pytest.raises(TypeError, match="WAIT duration cannot be a boolean"):
        TargetInstruction("WAIT", False)

    # Unexpected second operand
    with pytest.raises(ValueError, match="WAIT instruction does not accept operand2"):
        TargetInstruction("WAIT", 5, "extra")


@pytest.mark.parametrize("opcode", ["START", "END", "PICK", "DROP"])
def test_zero_operand_commands_reject_operands(opcode):
    """START, END, PICK, DROP must not have operands."""
    with pytest.raises(ValueError, match=f"{opcode} instruction does not accept operands"):
        TargetInstruction(opcode, "unwanted")

    with pytest.raises(ValueError, match=f"{opcode} instruction does not accept operands"):
        TargetInstruction(opcode, operand2="unwanted")


def test_bypass_validation_flag():
    """Setting validate=False allows custom or non-standard instructions."""
    custom = TargetInstruction("CUSTOM", "ARG1", "ARG2", validate=False)
    assert custom.opcode == "CUSTOM"
    assert str(custom) == "CUSTOM ARG1 ARG2"


# ---------------------------------------------------------------------------
# Integration with TAC: from_tac()
# ---------------------------------------------------------------------------
def test_from_tac_conversion_without_mutating_tac():
    """Ensure from_tac creates TargetInstruction and leaves TACInstruction intact."""
    tac_instructions = [
        TACInstruction("START"),
        TACInstruction("MOVE", "FORWARD", 10),
        TACInstruction("TURN", "LEFT"),
        TACInstruction("PICK"),
        TACInstruction("WAIT", 5),
        TACInstruction("DROP"),
        TACInstruction("MOVE", "BACKWARD", 5),
        TACInstruction("TURN", "RIGHT"),
        TACInstruction("END"),
    ]

    target_instructions = [TargetInstruction.from_tac(tac) for tac in tac_instructions]

    expected_strings = [
        "START",
        "MOVE FORWARD 10",
        "TURN LEFT",
        "PICK",
        "WAIT 5",
        "DROP",
        "MOVE BACKWARD 5",
        "TURN RIGHT",
        "END",
    ]

    assert [str(target) for target in target_instructions] == expected_strings

    # Verify TACInstruction remains unmodified
    assert tac_instructions[1].operator == "MOVE"
    assert tac_instructions[1].operand1 == "FORWARD"
    assert tac_instructions[1].operand2 == 10


def test_from_tac_missing_opcode_raises_error():
    """Attempting from_tac on an object with no opcode raises ValueError."""
    class Empty:
        pass

    with pytest.raises(ValueError, match="missing opcode/operator"):
        TargetInstruction.from_tac(Empty())


# ---------------------------------------------------------------------------
# Constants export check
# ---------------------------------------------------------------------------
def test_supported_constants_export():
    """Verify supported constants match RCL design."""
    assert "START" in SUPPORTED_OPCODES
    assert "END" in SUPPORTED_OPCODES
    assert "MOVE" in SUPPORTED_OPCODES
    assert "TURN" in SUPPORTED_OPCODES
    assert "WAIT" in SUPPORTED_OPCODES
    assert "PICK" in SUPPORTED_OPCODES
    assert "DROP" in SUPPORTED_OPCODES

    assert SUPPORTED_MOVE_DIRECTIONS == frozenset({"FORWARD", "BACKWARD"})
    assert SUPPORTED_TURN_DIRECTIONS == frozenset({"LEFT", "RIGHT"})
