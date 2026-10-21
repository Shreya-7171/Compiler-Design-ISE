
"""Generate final RCL target code from three-address-code instructions."""

from collections.abc import Iterable

from icg.intermediate_code import TACInstruction


class TargetCodeGenerator:
    """Convert RCL TAC instructions into target-code lines."""

    SUPPORTED_COMMANDS = {"START", "END", "MOVE", "TURN", "PICK", "DROP", "WAIT"}

    def generate(self, instructions: Iterable[TACInstruction]) -> list[str]:
        """Return target-code lines for the supplied TAC instructions."""
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

            if command in {"START", "END", "PICK", "DROP"}:
                line = command

            elif command == "MOVE":
                direction = str(instruction.operand1).upper()
                distance = instruction.operand2

                if direction not in {"FORWARD", "BACKWARD"}:
                    raise ValueError(f"Unsupported MOVE direction: {direction}")

                line = f"MOVE {direction} {distance}"

            elif command == "TURN":
                direction = str(instruction.operand1).upper()

                if direction not in {"LEFT", "RIGHT"}:
                    raise ValueError(f"Unsupported TURN direction: {direction}")

                line = f"TURN {direction}"

            else:  # WAIT
                duration = instruction.operand1

                if duration is None:
                    raise ValueError("WAIT requires a duration")

                line = f"WAIT {duration}"

            target_code.append(line)

        return target_code


def generate_target_code(instructions: Iterable[TACInstruction]) -> list[str]:
    """Convenience function for generating target code."""
    return TargetCodeGenerator().generate(instructions)
