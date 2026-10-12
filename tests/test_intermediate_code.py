import pytest

from icg.intermediate_code import (
    IntermediateCodeGenerator,
    TACInstruction,
    generate_from_source,
    generate_intermediate_code,
)
from sematic_member3.semantic_error import SemanticError


def test_instruction_fields_and_common_aliases():
    instruction = TACInstruction("ADD", "left", "right", "t1")

    assert instruction.operator == instruction.opcode == "ADD"
    assert instruction.operand1 == instruction.arg1 == "left"
    assert instruction.operand2 == instruction.arg2 == "right"
    assert instruction.result == "t1"
    assert str(instruction) == "t1 = left + right"


@pytest.mark.parametrize(
    ("instruction", "expected"),
    [
        (TACInstruction("ASSIGN", 12, result="distance"), "distance = 12"),
        (TACInstruction("LABEL", result="L1"), "L1:"),
        (TACInstruction("GOTO", result="L2"), "GOTO L2"),
        (TACInstruction("IF_FALSE_GOTO", "ready", result="L3"), "IF_FALSE ready GOTO L3"),
        (TACInstruction("MOVE", "FORWARD", 10), "MOVE FORWARD 10"),
        (TACInstruction("TURN", "LEFT"), "TURN LEFT"),
        (TACInstruction("WAIT", 5), "WAIT 5"),
        (TACInstruction("PICK"), "PICK"),
    ],
)
def test_instruction_formatting(instruction, expected):
    assert str(instruction) == expected


def test_temporaries_and_labels_are_unique_and_resettable():
    generator = IntermediateCodeGenerator()

    assert [generator.new_temp() for _ in range(3)] == ["t1", "t2", "t3"]
    assert [generator.new_label() for _ in range(3)] == ["L1", "L2", "L3"]

    generator.reset()

    assert generator.new_temp() == "t1"
    assert generator.new_label() == "L1"


def test_generators_have_independent_name_sequences():
    first = IntermediateCodeGenerator()
    second = IntermediateCodeGenerator()

    assert first.new_temp() == second.new_temp() == "t1"
    assert first.new_label() == second.new_label() == "L1"


def test_lower_all_supported_semantic_commands_in_order():
    statements = [
        {"cmd": "START"},
        {"cmd": "MOVE", "direction": "FORWARD", "distance": 10},
        {"cmd": "TURN", "direction": "LEFT"},
        {"cmd": "PICK"},
        {"cmd": "WAIT", "duration": 5},
        {"cmd": "DROP"},
        {"cmd": "MOVE", "direction": "BACKWARD", "distance": 3},
        {"cmd": "END"},
    ]

    code = generate_intermediate_code(statements)

    assert [instruction.operator for instruction in code] == [
        "START", "MOVE", "TURN", "PICK", "WAIT", "DROP", "MOVE", "END"
    ]
    assert [str(instruction) for instruction in code] == [
        "START",
        "MOVE FORWARD 10",
        "TURN LEFT",
        "PICK",
        "WAIT 5",
        "DROP",
        "MOVE BACKWARD 3",
        "END",
    ]
    assert code[1].operand1 == "FORWARD"
    assert code[1].operand2 == 10
    assert code[4].operand1 == 5


def test_empty_statement_list_generates_empty_code():
    assert generate_intermediate_code([]) == []


def test_source_pipeline_uses_existing_lexer_and_semantic_analysis():
    source = "START\nMOVE FORWARD 10\nTURN RIGHT\nPICK\nWAIT 2\nDROP\nEND"

    assert [str(instruction) for instruction in generate_from_source(source)] == [
        "START",
        "MOVE FORWARD 10",
        "TURN RIGHT",
        "PICK",
        "WAIT 2",
        "DROP",
        "END",
    ]


def test_source_pipeline_preserves_semantic_errors():
    with pytest.raises(SemanticError, match="DROP"):
        generate_from_source("START\nDROP\nEND")


@pytest.mark.parametrize(
    ("statements", "error"),
    [
        ([{"cmd": "JUMP"}], "unsupported command"),
        ([{"cmd": "MOVE", "distance": 5}], "missing 'direction'"),
        ([{"cmd": "MOVE", "direction": "LEFT", "distance": 5}], "unsupported MOVE direction"),
        ([{"cmd": "TURN", "direction": "FORWARD"}], "unsupported TURN direction"),
        ([{"cmd": "WAIT"}], "missing 'duration'"),
    ],
)
def test_unsupported_or_incomplete_statements_raise_clear_errors(statements, error):
    with pytest.raises(ValueError, match=error):
        generate_intermediate_code(statements)


def test_non_dictionary_statement_is_rejected():
    with pytest.raises(TypeError, match="must be a dictionary"):
        generate_intermediate_code([None])
