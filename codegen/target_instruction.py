"""Target instruction representation for the Robot Command Language (RCL) backend.

This module defines `TargetInstruction`, representing a single low-level target
instruction for the RCL compiler (Phase 7: Target Code Generation).
It provides structured storage, validation, and deterministic formatting into
human-readable target code.
"""

from dataclasses import dataclass, field
from typing import Any


SUPPORTED_OPCODES: frozenset[str] = frozenset(
    {"START", "END", "MOVE", "TURN", "WAIT", "PICK", "DROP"}
)

SUPPORTED_MOVE_DIRECTIONS: frozenset[str] = frozenset({"FORWARD", "BACKWARD"})

SUPPORTED_TURN_DIRECTIONS: frozenset[str] = frozenset({"LEFT", "RIGHT"})


def _check_positive_numeric(value: Any, name: str, op: str) -> None:
    """Validate that a numeric value is strictly positive (> 0)."""
    if isinstance(value, bool):
        raise TypeError(f"{op} {name} cannot be a boolean, got {value!r}")
    if isinstance(value, (int, float)):
        if value <= 0:
            raise ValueError(f"{op} {name} must be a positive number, got {value}")
    elif isinstance(value, str):
        try:
            numeric_val = float(value)
            if numeric_val <= 0:
                raise ValueError(f"{op} {name} must be a positive number, got {value}")
        except ValueError as err:
            # Re-raise if it was our positive number check
            if "must be a positive number" in str(err):
                raise
            # Otherwise, non-numeric strings (e.g. register identifiers like "R1") are allowed


@dataclass(frozen=True)
class TargetInstruction:
    """Structured representation of one target-code instruction for RCL.

    Attributes:
        opcode: Operation code (e.g., 'START', 'MOVE', 'TURN', 'WAIT', 'PICK', 'DROP', 'END').
        operand1: First operand if required (e.g., direction 'FORWARD'/'BACKWARD' for MOVE,
                  direction 'LEFT'/'RIGHT' for TURN, duration for WAIT).
        operand2: Second operand if required (e.g., distance for MOVE).
        result: Optional target destination, register, or label (defaults to None).
        validate: When True (default), validates instruction format and values.
    """

    opcode: str
    operand1: Any = None
    operand2: Any = None
    result: Any = None
    validate: bool = field(default=True, compare=False, repr=False)

    def __post_init__(self) -> None:
        """Normalize fields and validate instruction format."""
        if not isinstance(self.opcode, str):
            raise TypeError(
                f"Opcode must be a string, got {type(self.opcode).__name__}"
            )

        stripped_opcode = self.opcode.strip()
        if not stripped_opcode:
            raise ValueError("Opcode cannot be empty")

        normalized_opcode = stripped_opcode.upper()
        object.__setattr__(self, "opcode", normalized_opcode)

        # Normalize direction operands to uppercase strings if applicable
        if normalized_opcode in {"MOVE", "TURN"} and isinstance(self.operand1, str):
            object.__setattr__(self, "operand1", self.operand1.strip().upper())

        if self.validate:
            self.validate_instruction()

    @property
    def operator(self) -> str:
        """Alias for opcode, consistent with TACInstruction."""
        return self.opcode

    @property
    def arg1(self) -> Any:
        """Alias for operand1, consistent with TACInstruction."""
        return self.operand1

    @property
    def arg2(self) -> Any:
        """Alias for operand2, consistent with TACInstruction."""
        return self.operand2

    def validate_instruction(self) -> None:
        """Validate that opcode and operands match RCL target specifications."""
        op = self.opcode

        if op not in SUPPORTED_OPCODES:
            supported = ", ".join(sorted(SUPPORTED_OPCODES))
            raise ValueError(
                f"Unsupported opcode {op!r}. Supported opcodes are: {supported}"
            )

        if op in {"START", "END", "PICK", "DROP"}:
            if self.operand1 is not None or self.operand2 is not None:
                raise ValueError(
                    f"{op} instruction does not accept operands, "
                    f"got operand1={self.operand1!r}, operand2={self.operand2!r}"
                )

        elif op == "MOVE":
            if self.operand1 is None:
                raise ValueError(
                    "MOVE instruction requires direction as operand1 ('FORWARD' or 'BACKWARD')"
                )
            if self.operand1 not in SUPPORTED_MOVE_DIRECTIONS:
                supported = ", ".join(sorted(SUPPORTED_MOVE_DIRECTIONS))
                raise ValueError(
                    f"Unsupported MOVE direction {self.operand1!r}. Supported directions are: {supported}"
                )
            if self.operand2 is None:
                raise ValueError("MOVE instruction requires distance as operand2")
            _check_positive_numeric(self.operand2, "distance", "MOVE")

        elif op == "TURN":
            if self.operand1 is None:
                raise ValueError(
                    "TURN instruction requires direction as operand1 ('LEFT' or 'RIGHT')"
                )
            if self.operand1 not in SUPPORTED_TURN_DIRECTIONS:
                supported = ", ".join(sorted(SUPPORTED_TURN_DIRECTIONS))
                raise ValueError(
                    f"Unsupported TURN direction {self.operand1!r}. Supported directions are: {supported}"
                )
            if self.operand2 is not None:
                raise ValueError(
                    f"TURN instruction does not accept operand2, got {self.operand2!r}"
                )

        elif op == "WAIT":
            if self.operand1 is None:
                raise ValueError("WAIT instruction requires duration as operand1")
            _check_positive_numeric(self.operand1, "duration", "WAIT")
            if self.operand2 is not None:
                raise ValueError(
                    f"WAIT instruction does not accept operand2, got {self.operand2!r}"
                )

    def __str__(self) -> str:
        """Convert structured instruction to deterministic target-code string."""
        op = self.opcode

        if op in {"START", "END", "PICK", "DROP"}:
            return op

        if op == "MOVE":
            tokens = [op]
            if self.operand1 is not None:
                tokens.append(str(self.operand1))
            if self.operand2 is not None:
                tokens.append(str(self.operand2))
            return " ".join(tokens)

        if op in {"TURN", "WAIT"}:
            tokens = [op]
            if self.operand1 is not None:
                tokens.append(str(self.operand1))
            return " ".join(tokens)

        # Fallback for generic / unvalidated instructions
        tokens = [op]
        for operand in (self.operand1, self.operand2, self.result):
            if operand is not None:
                tokens.append(str(operand))
        return " ".join(tokens)

    @classmethod
    def from_tac(cls, tac: Any, validate: bool = True) -> "TargetInstruction":
        """Construct a TargetInstruction from an existing TACInstruction.

        The existing TAC instruction is not modified.

        Args:
            tac: A TACInstruction instance or duck-typed equivalent.
            validate: Whether to validate the resulting TargetInstruction.

        Returns:
            A new TargetInstruction instance.
        """
        opcode = getattr(tac, "opcode", getattr(tac, "operator", None))
        if opcode is None:
            raise ValueError(
                f"Cannot convert {tac!r} to TargetInstruction: missing opcode/operator"
            )

        return cls(
            opcode=str(opcode),
            operand1=getattr(tac, "operand1", None),
            operand2=getattr(tac, "operand2", None),
            result=getattr(tac, "result", None),
            validate=validate,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return the instruction fields as a plain dictionary."""
        return {
            "opcode": self.opcode,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "result": self.result,
        }
