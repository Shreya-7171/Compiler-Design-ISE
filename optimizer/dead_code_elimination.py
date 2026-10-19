"""Dead code elimination for TAC instructions."""

from icg.intermediate_code import TACInstruction


VALUE_OPERATORS = {
    "ADD", "SUB", "MUL", "DIV", "MOD",
    "LT", "LE", "GT", "GE", "EQ", "NE",
    "ASSIGN",
}

BINARY_OPERATORS = VALUE_OPERATORS - {"ASSIGN"}


def _used_values(instruction):
    """Return values read by an instruction."""
    operator = instruction.operator.upper()

    if operator in BINARY_OPERATORS:
        return {
            str(instruction.operand1),
            str(instruction.operand2)
        }

    if operator == "ASSIGN":
        return {str(instruction.operand1)}

    if operator == "MOVE":
        return {str(instruction.operand2)}

    if operator == "WAIT":
        return {str(instruction.operand1)}

    if operator in {"IF_TRUE_GOTO", "IF_FALSE_GOTO"}:
        return {str(instruction.operand1)}

    return set()


def eliminate_dead_code(instructions):
    """Remove unused computations and preserve robot/control instructions."""
    instructions = list(instructions)

    live = set()
    kept = []

    for instruction in reversed(instructions):
        operator = instruction.operator.upper()

        # Robot/control instructions are observable.
        if operator not in VALUE_OPERATORS:
            live.update(_used_values(instruction))
            kept.append(instruction)
            continue

        result = instruction.result
        result_name = str(result) if result is not None else None

        # Keep computation if its result is needed later.
        if result_name is None or result_name in live:
            if result_name is not None:
                live.discard(result_name)

            live.update(_used_values(instruction))
            kept.append(instruction)

    return list(reversed(kept))