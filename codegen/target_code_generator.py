
"""Generate assembly-like target code from RCL TAC instructions."""

from collections.abc import Iterable

from icg.intermediate_code import TACInstruction


class TargetCodeGenerator:
    """Convert RCL TAC instructions into assembly-like target code."""

    SUPPORTED_COMMANDS = {
        "START",
        "END",
        "MOVE",
        "TURN",
        "PICK",
        "DROP",
        "WAIT",
    }

    def __init__(self):
        self.register = "R1"

    def generate(self, instructions: Iterable[TACInstruction]) -> list[str]:
        """Return assembly-like target-code lines."""
        target_code = []

        for index, instruction in enumerate(instructions):
            if not isinstance(instruction, TACInstruction):
                raise TypeError(
                    f"Instruction {index} must be a TACInstruction"
                )

            command = instruction.operator.upper()

            if command not in self.SUPPORTED_COMMANDS:
                raise ValueError(
                    f"Unsupported target command at instruction {index}: {command}"
                )

            if command == "START":
                target_code.append("START:")

            elif command == "END":
                target_code.append("HALT")

            elif command == "MOVE":
                direction = str(instruction.operand1).upper()
                distance = instruction.operand2

                if direction not in {"FORWARD", "BACKWARD"}:
                    raise ValueError(
                        f"Unsupported MOVE direction: {direction}"
                    )

                target_code.append(f"MOV {self.register}, {distance}")
                target_code.append(f"MOVE_{direction} {self.register}")

            elif command == "TURN":
                direction = str(instruction.operand1).upper()

                if direction not in {"LEFT", "RIGHT"}:
                    raise ValueError(
                        f"Unsupported TURN direction: {direction}"
                    )

                target_code.append(f"TURN_{direction}")

            elif command == "PICK":
                target_code.append("PICK")

            elif command == "DROP":
                target_code.append("DROP")

            elif command == "WAIT":
                duration = instruction.operand1

                if duration is None:
                    raise ValueError("WAIT requires a duration")

                target_code.append(f"WAIT {duration}")

        return target_code


def generate_target_code(
    instructions: Iterable[TACInstruction],
) -> list[str]:
    """Convenience function for generating target code."""
    return TargetCodeGenerator().generate(instructions)
