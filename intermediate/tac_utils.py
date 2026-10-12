
"""Utility functions for formatting Three Address Code (TAC)."""


def format_instruction(instruction):
    """Convert one TAC instruction into readable text."""
    return str(instruction)


def format_instructions(instructions):
    """Format multiple TAC instructions as newline-separated text."""
    return "\n".join(format_instruction(instruction) for instruction in instructions)
