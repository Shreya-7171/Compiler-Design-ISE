"""Constant-fold numeric operations in RCL three-address code."""

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


def _is_numeric_constant(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _evaluate(operator: str, left: int | float, right: int | float) -> int | float | bool:
    if operator == "ADD":
        return left + right
    if operator == "SUB":
        return left - right
    if operator == "MUL":
        return left * right
    if operator == "DIV":
        return left / right
    if operator == "MOD":
        return left % right
    if operator == "LT":
        return left < right
    if operator == "LE":
        return left <= right
    if operator == "GT":
        return left > right
    if operator == "GE":
        return left >= right
    if operator == "EQ":
        return left == right
    return left != right


def fold_constants(tac: list[TACInstruction]) -> list[TACInstruction]:
    """Return a new TAC list with operations on numeric literals folded.

    DIV uses true division (the selected RCL optimization convention). An
    operation that cannot be evaluated, including division by zero, is kept.
    """
    folded: list[TACInstruction] = []

    for instruction in tac:
        operator = instruction.operator.upper()
        if (
            operator not in _BINARY_OPERATORS
            or not _is_numeric_constant(instruction.operand1)
            or not _is_numeric_constant(instruction.operand2)
        ):
            folded.append(instruction)
            continue

        try:
            value = _evaluate(operator, instruction.operand1, instruction.operand2)
        except ZeroDivisionError:
            folded.append(instruction)
            continue

        folded.append(
            replace(
                instruction,
                operator="ASSIGN",
                operand1=value,
                operand2=None,
            )
        )

    return folded
