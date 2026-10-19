"""Substitute known numeric constants into RCL three-address code.

Instructions without labels, jumps, or branches are treated as straight-line
code. When control-flow instructions are present, known values are discarded
at labels and after jumps or branches to avoid propagating across paths.
"""

from dataclasses import replace

from icg.intermediate_code import TACInstruction

_BINARY_OPERATORS = {
    "ADD",
    "SUB",
    "MUL",
    "DIV",
    "MOD",
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
}
_CONTROL_FLOW_OPERATORS = {
    "GOTO",
    "JUMP",
    "IF_TRUE_GOTO",
    "IF_FALSE_GOTO",
}


def _is_numeric_constant(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _substitute(value: object, known: dict[str, int | float]) -> object:
    if isinstance(value, str) and value in known:
        return known[value]
    return value


def propagate_constants(tac: list[TACInstruction]) -> list[TACInstruction]:
    """Return a new TAC list with known numeric constants substituted."""
    propagated: list[TACInstruction] = []
    known: dict[str, int | float] = {}

    for instruction in tac:
        operator = instruction.operator.upper()
        if operator == "LABEL":
            known.clear()

        updates: dict[str, object] = {}
        if operator == "ASSIGN":
            updates["operand1"] = _substitute(instruction.operand1, known)
        elif operator in _BINARY_OPERATORS:
            updates["operand1"] = _substitute(instruction.operand1, known)
            updates["operand2"] = _substitute(instruction.operand2, known)
        elif operator == "MOVE":
            updates["operand2"] = _substitute(instruction.operand2, known)
        elif operator == "WAIT":
            updates["operand1"] = _substitute(instruction.operand1, known)
        elif operator in _CONTROL_FLOW_OPERATORS:
            if operator in {"IF_TRUE_GOTO", "IF_FALSE_GOTO"}:
                updates["operand1"] = _substitute(instruction.operand1, known)

        updated = replace(instruction, **updates) if updates else instruction
        propagated.append(updated)

        if operator == "ASSIGN" and isinstance(instruction.result, str):
            known.pop(instruction.result, None)
            source = updated.operand1
            if _is_numeric_constant(source):
                known[instruction.result] = source
        elif operator in _BINARY_OPERATORS and isinstance(instruction.result, str):
            known.pop(instruction.result, None)

        if operator in _CONTROL_FLOW_OPERATORS:
            known.clear()

    return propagated
