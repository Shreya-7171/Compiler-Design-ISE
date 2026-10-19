
import unittest

from icg.intermediate_code import TACInstruction
from optimizer.dead_code_elimination import eliminate_dead_code


class TestDeadCodeElimination(unittest.TestCase):
    def test_removes_unused_arithmetic_result(self):
        instructions = [
            TACInstruction("ADD", 2, 3, "t1"),
            TACInstruction("END"),
        ]

        result = eliminate_dead_code(instructions)

        self.assertEqual(result, [TACInstruction("END")])

    
    def test_keeps_arithmetic_result_that_is_used(self):
        instructions = [
            TACInstruction("ADD", 2, 3, "t1"),
            TACInstruction("MUL", "t1", 4, "t2"),
            TACInstruction("IF_TRUE_GOTO", "t2", None, "label1"),
            TACInstruction("END"),
        ]

        result = eliminate_dead_code(instructions)

        self.assertIn(instructions[0], result)
        self.assertIn(instructions[1], result)
        self.assertIn(instructions[2], result)
        self.assertIn(instructions[3], result)


    def test_preserves_robot_commands(self):
        instructions = [
            TACInstruction("START"),
            TACInstruction("PICK"),
            TACInstruction("MOVE", "FORWARD", 5),
            TACInstruction("DROP"),
            TACInstruction("END"),
        ]

        result = eliminate_dead_code(instructions)

        self.assertEqual(result, instructions)

    def test_does_not_modify_original_list(self):
        instructions = [
            TACInstruction("ADD", 2, 3, "t1"),
            TACInstruction("END"),
        ]

        eliminate_dead_code(instructions)

        self.assertEqual(len(instructions), 2)


if __name__ == "__main__":
    unittest.main()
