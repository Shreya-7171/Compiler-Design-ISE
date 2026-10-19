from icg.intermediate_code import (
    TACInstruction,
    generate_from_source,
)
from optimizer import fold_constants, propagate_constants


def test_propagates_a_constant_to_later_uses():
    instructions = [
        TACInstruction("ASSIGN", 10, result="t1"),
        TACInstruction("ADD", "t1", 5, "t2"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated == [
        instructions[0],
        TACInstruction("ADD", 10, 5, "t2"),
    ]


def test_propagates_constants_through_assignment_chains():
    instructions = [
        TACInstruction("ASSIGN", 10, result="first"),
        TACInstruction("ASSIGN", "first", result="second"),
        TACInstruction("SUB", "second", 3, "result"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[1].operand1 == 10
    assert propagated[2].operand1 == 10


def test_reassignment_to_unknown_value_invalidates_known_constant():
    instructions = [
        TACInstruction("ASSIGN", 10, result="value"),
        TACInstruction("ASSIGN", "unknown", result="value"),
        TACInstruction("ADD", "value", 1, "result"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[1].operand1 == "unknown"
    assert propagated[2].operand1 == "value"


def test_unknown_variables_are_not_propagated():
    instruction = TACInstruction("ADD", "unknown", 2, "result")

    assert propagate_constants([instruction]) == [instruction]


def test_substitutes_constant_side_of_mixed_expression_only():
    instructions = [
        TACInstruction("ASSIGN", 4, result="fixed"),
        TACInstruction("MUL", "fixed", "unknown", "result"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[1] == TACInstruction("MUL", 4, "unknown", "result")


def test_clears_known_values_at_labels_and_after_branches():
    instructions = [
        TACInstruction("ASSIGN", 3, result="value"),
        TACInstruction("LABEL", result="L1"),
        TACInstruction("ADD", "value", 1, "after_label"),
        TACInstruction("ASSIGN", 4, result="condition"),
        TACInstruction("IF_TRUE_GOTO", "condition", result="L2"),
        TACInstruction("ADD", "condition", 1, "after_branch"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[2].operand1 == "value"
    assert propagated[4].operand1 == 4
    assert propagated[5].operand1 == "condition"


def test_clears_known_values_after_jumps():
    instructions = [
        TACInstruction("ASSIGN", 3, result="value"),
        TACInstruction("GOTO", result="L1"),
        TACInstruction("ADD", "value", 1, "after_jump"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[2].operand1 == "value"


def test_propagates_only_numeric_robot_arguments():
    instructions = [
        TACInstruction("ASSIGN", 12, result="distance"),
        TACInstruction("MOVE", "FORWARD", "distance"),
        TACInstruction("WAIT", "distance"),
        TACInstruction("ASSIGN", 1, result="LEFT"),
        TACInstruction("TURN", "LEFT"),
    ]

    propagated = propagate_constants(instructions)

    assert propagated[1].operand1 == "FORWARD"
    assert propagated[1].operand2 == 12
    assert propagated[2].operand1 == 12
    assert propagated[4].operand1 == "LEFT"


def test_empty_input_returns_a_new_empty_list():
    instructions = []

    propagated = propagate_constants(instructions)

    assert propagated == []
    assert propagated is not instructions


def test_does_not_mutate_input_and_accepts_real_icg_output():
    instructions = [
        TACInstruction("ASSIGN", 10, result="distance"),
        *generate_from_source("START\nMOVE FORWARD 10\nEND"),
    ]
    original = instructions.copy()

    propagated = propagate_constants(instructions)

    assert instructions == original
    assert propagated[1:] == original[1:]
    assert propagated is not instructions


def test_propagation_then_folding_composes():
    instructions = [
        TACInstruction("ASSIGN", 10, result="t1"),
        TACInstruction("ADD", "t1", 5, "t2"),
    ]

    optimized = fold_constants(propagate_constants(instructions))

    assert optimized[1] == TACInstruction("ASSIGN", 15, result="t2")
