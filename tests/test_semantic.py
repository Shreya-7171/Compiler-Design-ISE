# ==============================================================================
# File: test_semantic.py
# Project: RCL (Robot Command Language) Compiler
# Member 3: Semantic Errors + Testing
# ==============================================================================

import sys
import os

# Allow "from semantic_error import ..."
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "sematic_member3")
    )
)

from semantic_error import analyze_source, SemanticError


# ------------------------------------------------------------------
# POSITIVE TEST CASES (valid RCL programs -> no error raised)
# ------------------------------------------------------------------

def test_valid_minimal_program():
    source = "START\nEND"
    statements = analyze_source(source)
    assert statements[0]["cmd"] == "START"
    assert statements[-1]["cmd"] == "END"


def test_valid_full_program():
    source = "START\nMOVE FORWARD 10\nTURN LEFT\nWAIT 5\nEND"
    statements = analyze_source(source)
    cmds = [s["cmd"] for s in statements]
    assert cmds == ["START", "MOVE", "TURN", "WAIT", "END"]


def test_valid_move_backward():
    source = "START\nMOVE BACKWARD 3\nEND"
    statements = analyze_source(source)
    move = statements[1]
    assert move["direction"] == "BACKWARD"
    assert move["distance"] == 3


def test_valid_turn_right():
    source = "START\nTURN RIGHT\nEND"
    statements = analyze_source(source)
    assert statements[1]["direction"] == "RIGHT"


def test_valid_pick_then_drop():
    source = "START\nPICK\nDROP\nEND"
    statements = analyze_source(source)
    cmds = [s["cmd"] for s in statements]
    assert cmds == ["START", "PICK", "DROP", "END"]


def test_valid_multiple_pick_drop_cycles():
    source = "START\nPICK\nDROP\nPICK\nDROP\nEND"
    statements = analyze_source(source)
    assert len(statements) == 6


# ------------------------------------------------------------------
# INVALID SEMANTIC TEST CASES (grammatically fine, semantically bad)
# ------------------------------------------------------------------

def test_missing_start():
    source = "MOVE FORWARD 10\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "START" in e.message


def test_missing_end():
    source = "START\nMOVE FORWARD 10"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "END" in e.message


def test_statement_after_end():
    source = "START\nEND\nMOVE FORWARD 10"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "END" in e.message


def test_duplicate_start():
    source = "START\nSTART\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "START" in e.message


def test_negative_move_distance():
    # Lexer has no "-" handling, so this is simulated at the analyzer level
    # via a program the lexer *can* produce: MOVE FORWARD 0 (non-positive).
    source = "START\nMOVE FORWARD 0\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "distance" in e.message


def test_zero_wait_duration():
    source = "START\nWAIT 0\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "WAIT" in e.message


def test_drop_without_pick():
    source = "START\nDROP\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "DROP" in e.message


def test_double_pick_without_drop():
    source = "START\nPICK\nPICK\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "PICK" in e.message


def test_empty_program():
    source = ""
    try:
        analyze_source(source)
        assert False, "Expected a SemanticError"
    except SemanticError as e:
        assert "empty" in e.message.lower()


# ------------------------------------------------------------------
# INTEGRATION: lexer + parser + semantic analyzer working together
# ------------------------------------------------------------------

def test_full_pipeline_valid_program():
    source = "START\nMOVE FORWARD 15\nTURN LEFT\nPICK\nWAIT 3\nDROP\nMOVE BACKWARD 5\nEND"
    statements = analyze_source(source)
    assert statements[0]["cmd"] == "START"
    assert statements[-1]["cmd"] == "END"
    assert len(statements) == 8


def test_full_pipeline_syntax_error_still_raised():
    # A grammar problem (missing NUMBER after MOVE direction) should surface
    # as a SyntaxError from the parser layer, not get swallowed as semantic.
    source = "START\nMOVE FORWARD\nEND"
    try:
        analyze_source(source)
        assert False, "Expected a SyntaxError"
    except SyntaxError:
        pass


# ------------------------------------------------------------------
# RUN ALL TESTS
# ------------------------------------------------------------------

if __name__ == "__main__":
    test_valid_minimal_program()
    test_valid_full_program()
    test_valid_move_backward()
    test_valid_turn_right()
    test_valid_pick_then_drop()
    test_valid_multiple_pick_drop_cycles()

    test_missing_start()
    test_missing_end()
    test_statement_after_end()
    test_duplicate_start()
    test_negative_move_distance()
    test_zero_wait_duration()
    test_drop_without_pick()
    test_double_pick_without_drop()
    test_empty_program()

    test_full_pipeline_valid_program()
    test_full_pipeline_syntax_error_still_raised()

    print("\nAll Member 3 semantic tests passed!")