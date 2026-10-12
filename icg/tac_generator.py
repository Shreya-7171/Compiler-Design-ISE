from typing import Any, Iterable

from .intermediate_code import (
    TACInstruction,
    IntermediateCodeGenerator,
    generate_from_source,
)


class TACGenerator:
    def __init__(self):
        self.generator = IntermediateCodeGenerator()

    def generate(self, statements: Iterable[dict[str, Any]]) -> list[TACInstruction]:
        return self.generator.generate(statements)

    def generate_from_source(self, source: str) -> list[TACInstruction]:
        return generate_from_source(source)

    def generate_text(self, statements: Iterable[dict[str, Any]]) -> str:
        instructions = self.generate(statements)
        return "\n".join(str(instruction) for instruction in instructions)

    def generate_text_from_source(self, source: str) -> str:
        instructions = self.generate_from_source(source)
        return "\n".join(str(instruction) for instruction in instructions)


def generate_tac(statements: Iterable[dict[str, Any]]) -> list[TACInstruction]:
    return TACGenerator().generate(statements)


def generate_tac_text(statements: Iterable[dict[str, Any]]) -> str:
    return TACGenerator().generate_text(statements)


def generate_tac_from_source(source: str) -> list[TACInstruction]:
    return TACGenerator().generate_from_source(source)


def generate_tac_text_from_source(source: str) -> str:
    return TACGenerator().generate_text_from_source(source)