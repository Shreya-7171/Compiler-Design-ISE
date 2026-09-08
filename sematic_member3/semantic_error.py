# ==============================================================================
# File: semantic_errors.py
# Project: RCL (Robot Command Language) Compiler
# Member 3: Semantic Errors + Testing
#
# Purpose:
#   ParserPartA / ParserPartB only check GRAMMAR (is this a legal sequence of
#   tokens?). They don't know that "MOVE FORWARD -5" is nonsense, that a
#   program has to start with START and end with END, or that "DROP" before
#   any "PICK" makes no physical sense. That's what semantic analysis is for:
#   catching statements that are syntactically fine but semantically invalid.
#
#   SemanticAnalyzer takes the full token stream from the Lexer, re-uses
#   ParserPartA/B to confirm each statement is grammatically valid, builds a
#   structured statement list out of it, and then checks that list against
#   RCL's semantic rules.
# ==============================================================================

import sys
import os

# Allow "from parser_part_a import ParserPartA" / "from parser_part_b import ..."
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "parser"))
)
# Allow "from lexer import Lexer, Token, TokenType"
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from parser_part_a import ParserPartA
from parser_part_b import ParserPartB
from lexer import Lexer, Token, TokenType


# ==============================================================================
# SemanticError
# ==============================================================================
class SemanticError(Exception):
    """
    Raised when an RCL program is syntactically valid (it parses fine) but
    violates a rule about what the program actually *means*.
    """

    def __init__(self, message, line=None):
        self.message = message
        self.line = line

        if line is not None:
            full_message = f"Semantic Error at line {line}: {message}"
        else:
            full_message = f"Semantic Error: {message}"

        super().__init__(full_message)


# ==============================================================================
# SemanticAnalyzer
# ==============================================================================
class SemanticAnalyzer:
    """
    Walks the token stream produced by the Lexer, validates each statement's
    grammar with ParserPartA / ParserPartB, and enforces semantic rules on
    top of that: value ranges, program structure, and PICK/DROP consistency.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.statements = []  # populated by analyze()

    # ---------------------------------------------------------------
    # Step 1: split the flat token list into one token-list per line
    # ---------------------------------------------------------------
    def _split_into_lines(self):
        lines = []
        current_line = []

        for token in self.tokens:
            if token.type in (TokenType.NEWLINE, TokenType.EOF):
                if current_line:
                    lines.append(current_line)
                    current_line = []
            else:
                current_line.append(token)

        if current_line:
            lines.append(current_line)

        return lines

    @staticmethod
    def _with_eof(line_tokens):
        """ParserPartA/B expect a token list; give them a safe EOF-terminated copy."""
        last = line_tokens[-1]
        eof_token = Token(TokenType.EOF, "", last.line, last.column + 1)
        return line_tokens + [eof_token]

    # ---------------------------------------------------------------
    # Step 2: validate grammar + build a structured statement dict
    # ---------------------------------------------------------------
    def _parse_statement(self, line_tokens):
        first = line_tokens[0]
        padded = self._with_eof(line_tokens)

        if first.type == TokenType.START:
            ParserPartA(padded).parse_start()
            return {"cmd": "START", "line": first.line}

        if first.type == TokenType.END:
            ParserPartA(padded).parse_end()
            return {"cmd": "END", "line": first.line}

        if first.type == TokenType.MOVE:
            ParserPartA(padded).parse_move()
            direction = line_tokens[1].value
            distance = line_tokens[2].value
            return {
                "cmd": "MOVE",
                "direction": direction,
                "distance": distance,
                "line": first.line,
            }

        if first.type == TokenType.TURN:
            ParserPartA(padded).parse_turn()
            direction = line_tokens[1].value
            return {"cmd": "TURN", "direction": direction, "line": first.line}

        if first.type == TokenType.PICK:
            ParserPartB(padded).parse_pick()
            return {"cmd": "PICK", "line": first.line}

        if first.type == TokenType.DROP:
            ParserPartB(padded).parse_drop()
            return {"cmd": "DROP", "line": first.line}

        if first.type == TokenType.WAIT:
            ParserPartB(padded).parse_wait()
            duration = line_tokens[1].value
            return {"cmd": "WAIT", "duration": duration, "line": first.line}

        if first.type == TokenType.INVALID:
            raise SyntaxError(
                f"Syntax Error at line {first.line}, column {first.column}: "
                f"Invalid token '{first.value}'"
            )

        raise SyntaxError(
            f"Syntax Error at line {first.line}, column {first.column}: "
            f"Unexpected token '{first.value}'"
        )

    # ---------------------------------------------------------------
    # Public entry point
    # ---------------------------------------------------------------
    def analyze(self):
        """
        Parses + semantically validates the whole token stream.
        Returns the list of parsed statement dicts on success.
        Raises SyntaxError for grammar problems, SemanticError for
        meaning problems.
        """
        lines = self._split_into_lines()
        statements = [self._parse_statement(line) for line in lines]
        self.statements = statements

        self._check_structure(statements)
        self._check_value_ranges(statements)
        self._check_object_state(statements)

        return statements

    # ---------------------------------------------------------------
    # Rule group 1: overall program structure
    # ---------------------------------------------------------------
    def _check_structure(self, statements):
        if not statements:
            raise SemanticError("Program is empty; expected START ... END")

        if statements[0]["cmd"] != "START":
            raise SemanticError("Program must begin with START", statements[0]["line"])

        if statements[-1]["cmd"] != "END":
            raise SemanticError("Program must end with END", statements[-1]["line"])

        for stmt in statements[1:-1]:
            if stmt["cmd"] == "START":
                raise SemanticError("Duplicate START statement", stmt["line"])
            if stmt["cmd"] == "END":
                raise SemanticError(
                    "Unexpected END: statements found after END", stmt["line"]
                )

    # ---------------------------------------------------------------
    # Rule group 2: value ranges for numeric arguments
    # ---------------------------------------------------------------
    def _check_value_ranges(self, statements):
        for stmt in statements:
            if stmt["cmd"] == "MOVE" and stmt["distance"] <= 0:
                raise SemanticError(
                    f"MOVE distance must be a positive number, got {stmt['distance']}",
                    stmt["line"],
                )

            if stmt["cmd"] == "WAIT" and stmt["duration"] <= 0:
                raise SemanticError(
                    f"WAIT duration must be a positive number, got {stmt['duration']}",
                    stmt["line"],
                )

    # ---------------------------------------------------------------
    # Rule group 3: PICK/DROP must alternate sensibly
    # ---------------------------------------------------------------
    def _check_object_state(self, statements):
        holding = False

        for stmt in statements:
            if stmt["cmd"] == "PICK":
                if holding:
                    raise SemanticError(
                        "Cannot PICK: robot is already holding an object",
                        stmt["line"],
                    )
                holding = True

            elif stmt["cmd"] == "DROP":
                if not holding:
                    raise SemanticError(
                        "Cannot DROP: robot is not holding anything",
                        stmt["line"],
                    )
                holding = False


# ==============================================================================
# Convenience function: full pipeline in one call (lexer -> semantic analyzer)
# ==============================================================================
def analyze_source(source):
    """
    Lexes + semantically analyzes a full RCL source string.
    Returns the list of parsed statements on success.
    """
    tokens = Lexer(source).tokenize()
    return SemanticAnalyzer(tokens).analyze()


# ==============================================================================
# Self-test block
# ==============================================================================
if __name__ == "__main__":
    good_program = "START\nMOVE FORWARD 10\nTURN LEFT\nWAIT 5\nEND"
    print("Valid program statements:")
    for s in analyze_source(good_program):
        print(" ", s)

    # Note: the lexer has no "-" handling, so negative numbers like -5 can't
    # even be tokenized as a NUMBER - that would surface as a SyntaxError
    # from the parser layer, not a SemanticError. To trigger our semantic
    # rule (distance must be positive) we use 0, which IS a valid NUMBER
    # token but still violates the rule.
    bad_program = "START\nMOVE FORWARD 0\nEND"
    try:
        analyze_source(bad_program)
    except SemanticError as e:
        print("\nCaught expected semantic error:")
        print(" ", e)