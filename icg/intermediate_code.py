"""Three-address-code representation and lowering for the supported RCL."""

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class TACInstruction:
    """One intermediate instruction with two optional inputs and one result."""

    operator: str
    operand1: Any = None
    operand2: Any = None
    result: Any = None

    @property
    def opcode(self) -> str:
        """Alias commonly used by later compiler stages."""
        return self.operator

    @property
    def arg1(self) -> Any:
        return self.operand1

    @property
    def arg2(self) -> Any:
        return self.operand2

    def __str__(self) -> str:
        op = self.operator.upper()
        if op in {"ADD", "SUB", "MUL", "DIV", "MOD", "LT", "LE", "GT", "GE", "EQ", "NE"}:
            symbol = {
                "ADD": "+", "SUB": "-", "MUL": "*", "DIV": "/", "MOD": "%",
                "LT": "<", "LE": "<=", "GT": ">", "GE": ">=", "EQ": "==", "NE": "!=",
            }[op]
            return f"{self.result} = {self.operand1} {symbol} {self.operand2}"
        if op == "ASSIGN":
            return f"{self.result} = {self.operand1}"
        if op == "LABEL":
            return f"{self.result or self.operand1}:"
        if op in {"GOTO", "JUMP"}:
            return f"GOTO {self.result or self.operand1}"
        if op in {"IF_TRUE_GOTO", "IF_FALSE_GOTO"}:
            test = "IF" if op == "IF_TRUE_GOTO" else "IF_FALSE"
            return f"{test} {self.operand1} GOTO {self.result or self.operand2}"
        if op == "MOVE":
            return f"MOVE {self.operand1} {self.operand2}"
        if op in {"TURN"}:
            return f"TURN {self.operand1}"
        if op in {"WAIT"}:
            return f"WAIT {self.operand1}"
        if op in {"PICK", "DROP", "START", "END"}:
            return op
        fields = [str(value) for value in (self.operand1, self.operand2, self.result) if value is not None]
        return " ".join([op, *fields])


class IntermediateCodeGenerator:
    """Lower semantic-analysis statement dictionaries into RCL TAC."""

    _MOVE_DIRECTIONS = {"FORWARD", "BACKWARD"}
    _TURN_DIRECTIONS = {"LEFT", "RIGHT"}

    def __init__(self) -> None:
        self.instructions: list[TACInstruction] = []
        self._temp_count = 0
        self._label_count = 0

    def new_temp(self) -> str:
        """Return the next unique temporary name for this generation."""
        self._temp_count += 1
        return f"t{self._temp_count}"

    def new_label(self) -> str:
        """Return the next unique control-flow label for this generation."""
        self._label_count += 1
        return f"L{self._label_count}"

    def reset(self) -> None:
        """Clear emitted code and restart temporary and label numbering."""
        self.instructions.clear()
        self._temp_count = 0
        self._label_count = 0

    def generate(self, statements: Iterable[dict[str, Any]]) -> list[TACInstruction]:
        """Generate instructions from the dictionaries returned by SemanticAnalyzer."""
        self.reset()
        for index, statement in enumerate(statements):
            if not isinstance(statement, dict):
                raise TypeError(f"Statement {index} must be a dictionary")
            self.instructions.append(self._lower_statement(statement, index))
        return list(self.instructions)

    def _lower_statement(self, statement: dict[str, Any], index: int) -> TACInstruction:
        command = statement.get("cmd")
        if not isinstance(command, str):
            raise ValueError(f"Statement {index} is missing a string 'cmd'")
        command = command.upper()

        if command in {"START", "END", "PICK", "DROP"}:
            return TACInstruction(command)
        if command == "MOVE":
            direction = self._required(statement, "direction", index)
            distance = self._required(statement, "distance", index)
            if direction not in self._MOVE_DIRECTIONS:
                raise ValueError(f"Statement {index} has unsupported MOVE direction {direction!r}")
            return TACInstruction("MOVE", direction, distance)
        if command == "TURN":
            direction = self._required(statement, "direction", index)
            if direction not in self._TURN_DIRECTIONS:
                raise ValueError(f"Statement {index} has unsupported TURN direction {direction!r}")
            return TACInstruction("TURN", direction)
        if command == "WAIT":
            return TACInstruction("WAIT", self._required(statement, "duration", index))
        raise ValueError(f"Statement {index} has unsupported command {command!r}")

    @staticmethod
    def _required(statement: dict[str, Any], key: str, index: int) -> Any:
        if key not in statement:
            raise ValueError(f"Statement {index} ({statement.get('cmd')}) is missing {key!r}")
        return statement[key]


def generate_intermediate_code(
    statements: Iterable[dict[str, Any]],
) -> list[TACInstruction]:
    """Convenience API for lowering pre-parsed semantic statements."""
    return IntermediateCodeGenerator().generate(statements)


def generate_from_source(source: str) -> list[TACInstruction]:
    """Run the existing lexer and semantic analyzer, then lower their output."""
    from sematic_member3.semantic_error import analyze_source

    return generate_intermediate_code(analyze_source(source))
