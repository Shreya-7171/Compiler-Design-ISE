
"""Algebraic simplification for three-address code (TAC)."""

from icg.intermediate_code import TACInstruction


def _is_number(value):
    """Check whether a value is numeric."""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False


def _is_zero(value):
    return _is_number(value) and float(value) == 0


def _is_one(value):
    return _is_number(value) and float(value) == 1


def simplify_instruction(instruction):
    """Apply safe algebraic identities to one TAC instruction."""
    operator = instruction.operator.upper()
    left = instruction.operand1
    right = instruction.operand2
    result = instruction.result

    if operator == "ADD":
        if _is_zero(right):
            return TACInstruction("ASSIGN", left, None, result)
        if _is_zero(left):
            return TACInstruction("ASSIGN", right, None, result)

    elif operator == "SUB":
        if _is_zero(right):
            return TACInstruction("ASSIGN", left, None, result)

    elif operator == "MUL":
        if _is_one(right):
            return TACInstruction("ASSIGN", left, None, result)
        if _is_one(left):
            return TACInstruction("ASSIGN", right, None, result)
        if _is_zero(left) or _is_zero(right):
            return TACInstruction("ASSIGN", 0, None, result)

    elif operator == "DIV":
        if _is_one(right):
            return TACInstruction("ASSIGN", left, None, result)

    return instruction


def simplify_algebraic(instructions):
    """Return a new list with algebraic identities simplified."""
    return [simplify_instruction(item) for item in instructions]
