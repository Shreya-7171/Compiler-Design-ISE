from icg.intermediate_code import TACInstruction, generate_from_source
from optimizer import fold_constants


def test_folds_supported_numeric_operators():
    instructions = [
        TACInstruction("ADD", 10, 20, "t1"),
        TACInstruction("SUB", 10, 3, "t2"),
        TACInstruction("MUL", 8, 2, "t3"),
        TACInstruction("DIV", 7, 2, "t4"),
        TACInstruction("MOD", 10, 3, "t5"),
        TACInstruction("LT", 2, 3, "t6"),
    ]

    folded = fold_constants(instructions)

    assert [(item.operator, item.operand1, item.result) for item in folded] == [
        ("ASSIGN", 30, "t1"),
        ("ASSIGN", 7, "t2"),
        ("ASSIGN", 16, "t3"),
        ("ASSIGN", 3.5, "t4"),
        ("ASSIGN", 1, "t5"),
        ("ASSIGN", True, "t6"),
    ]


def test_folds_negative_integer_and_float_operands():
    instructions = [
        TACInstruction("ADD", -4, 1, "t1"),
        TACInstruction("MUL", 2.5, -2, "t2"),
    ]

    folded = fold_constants(instructions)

    assert [item.operand1 for item in folded] == [-3, -5.0]


def test_keeps_unfoldable_operations_unchanged():
    variable_operation = TACInstruction("ADD", "value", 5, "t1")
    text_operation = TACInstruction("MUL", "left", "right", "t2")

    folded = fold_constants([variable_operation, text_operation])

    assert folded == [variable_operation, text_operation]


def test_division_by_zero_is_left_unchanged():
    instruction = TACInstruction("DIV", 8, 0, "t1")

    assert fold_constants([instruction]) == [instruction]


def test_empty_input_returns_a_new_empty_list():
    instructions = []

    folded = fold_constants(instructions)

    assert folded == []
    assert folded is not instructions


def test_does_not_mutate_input_and_accepts_real_icg_output():
    instructions = [
        TACInstruction("ADD", 10, 20, "t1"),
        *generate_from_source("START\nMOVE FORWARD 10\nEND"),
    ]
    original = instructions.copy()

    folded = fold_constants(instructions)

    assert instructions == original
    assert instructions[0].operator == "ADD"
    assert folded[0] == TACInstruction("ASSIGN", 30, result="t1")
    assert folded[1:] == original[1:]
