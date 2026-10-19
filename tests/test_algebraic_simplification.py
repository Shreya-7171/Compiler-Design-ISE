
import unittest

from icg.intermediate_code import TACInstruction
from optimizer.algebraic_simplification import (
    simplify_algebraic,
    simplify_instruction,
)


class TestAlgebraicSimplification(unittest.TestCase):
    def test_add_zero(self):
        result = simplify_instruction(TACInstruction("ADD", "x", 0, "t1"))
        self.assertEqual(result, TACInstruction("ASSIGN", "x", None, "t1"))

    def test_subtract_zero(self):
        result = simplify_instruction(TACInstruction("SUB", "x", 0, "t1"))
        self.assertEqual(result, TACInstruction("ASSIGN", "x", None, "t1"))

    def test_multiply_by_one(self):
        result = simplify_instruction(TACInstruction("MUL", "x", 1, "t1"))
        self.assertEqual(result, TACInstruction("ASSIGN", "x", None, "t1"))

    def test_multiply_by_zero(self):
        result = simplify_instruction(TACInstruction("MUL", "x", 0, "t1"))
        self.assertEqual(result, TACInstruction("ASSIGN", 0, None, "t1"))

    def test_divide_by_one(self):
        result = simplify_instruction(TACInstruction("DIV", "x", 1, "t1"))
        self.assertEqual(result, TACInstruction("ASSIGN", "x", None, "t1"))

    def test_leaves_non_simplifiable_instruction_unchanged(self):
        instruction = TACInstruction("SUB", "x", "y", "t1")
        self.assertEqual(simplify_instruction(instruction), instruction)

    def test_simplifies_instruction_list(self):
        instructions = [
            TACInstruction("ADD", "x", 0, "t1"),
            TACInstruction("END"),
        ]
        result = simplify_algebraic(instructions)
        self.assertEqual(result[0], TACInstruction("ASSIGN", "x", None, "t1"))
        self.assertEqual(result[1], instructions[1])


if __name__ == "__main__":
    unittest.main()
