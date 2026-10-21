from lexer.rcl_token import TokenType
from semantic.symbol_table import SymbolTable


class SemanticError(Exception):
    """Raised when a semantic rule is violated."""
    pass


class SemanticAnalyzer:

    def __init__(self, tokens):

        self.tokens = tokens
        self.current = 0

        # Robot state
        self.carrying = False

        # Symbol table
        self.symbol_table = SymbolTable()

        # Counters for repeated commands
        self.move_count = 0
        self.turn_count = 0
        self.wait_count = 0

    # --------------------------------------------------
    # CURRENT TOKEN
    # --------------------------------------------------

    def current_token(self):

        if self.current >= len(self.tokens):
            return None

        return self.tokens[self.current]

    # --------------------------------------------------
    # ADVANCE
    # --------------------------------------------------

    def advance(self):

        self.current += 1

    # --------------------------------------------------
    # SEMANTIC ERROR
    # --------------------------------------------------

    def semantic_error(self, message):

        token = self.current_token()

        if token is None:
            raise SemanticError(message)

        raise SemanticError(
            f"Semantic Error at line {token.line}, "
            f"column {token.column}: {message}"
        )

    # --------------------------------------------------
    # SKIP NEWLINES
    # --------------------------------------------------

    def skip_newlines(self):

        while (
            self.current_token() is not None
            and self.current_token().type == TokenType.NEWLINE
        ):
            self.advance()

    # --------------------------------------------------
    # START
    # --------------------------------------------------

    def check_start(self):

        token = self.current_token()

        if token.type != TokenType.START:
            self.semantic_error(
                "Program must start with START"
            )

        self.symbol_table.add_symbol(
            "program",
            "RCL"
        )

        self.advance()

    # --------------------------------------------------
    # END
    # --------------------------------------------------

    def check_end(self):

        token = self.current_token()

        if token.type != TokenType.END:
            self.semantic_error(
                "Expected END"
            )

        self.symbol_table.add_symbol(
            "program_end",
            True
        )

        self.advance()

    # --------------------------------------------------
    # MOVE
    #
    # Semantic rule:
    # Distance must be greater than 0
    # --------------------------------------------------

    def check_move(self):

        token = self.current_token()

        if token.type != TokenType.MOVE:
            self.semantic_error(
                "Expected MOVE"
            )

        self.advance()

        # Get direction
        direction_token = self.current_token()

        if direction_token.type not in (
            TokenType.FORWARD,
            TokenType.BACKWARD
        ):
            self.semantic_error(
                "MOVE requires FORWARD or BACKWARD"
            )

        self.advance()

        # Get distance
        number_token = self.current_token()

        if number_token.type != TokenType.NUMBER:
            self.semantic_error(
                "MOVE requires a valid NUMBER"
            )

        # Semantic validation
        if number_token.value <= 0:
            self.semantic_error(
                "MOVE distance must be greater than 0"
            )

        # Add information to symbol table
        self.move_count += 1

        self.symbol_table.add_symbol(
            f"move_{self.move_count}_direction",
            direction_token.value
        )

        self.symbol_table.add_symbol(
            f"move_{self.move_count}_distance",
            number_token.value
        )

        self.advance()

    # --------------------------------------------------
    # TURN
    # --------------------------------------------------

    def check_turn(self):

        token = self.current_token()

        if token.type != TokenType.TURN:
            self.semantic_error(
                "Expected TURN"
            )

        self.advance()

        direction_token = self.current_token()

        if direction_token.type not in (
            TokenType.LEFT,
            TokenType.RIGHT
        ):
            self.semantic_error(
                "TURN requires LEFT or RIGHT"
            )

        # Add information to symbol table
        self.turn_count += 1

        self.symbol_table.add_symbol(
            f"turn_{self.turn_count}_direction",
            direction_token.value
        )

        self.advance()

    # --------------------------------------------------
    # WAIT
    #
    # Semantic rule:
    # Duration must be greater than 0
    # --------------------------------------------------

    def check_wait(self):

        token = self.current_token()

        if token.type != TokenType.WAIT:
            self.semantic_error(
                "Expected WAIT"
            )

        self.advance()

        duration_token = self.current_token()

        if duration_token.type != TokenType.NUMBER:
            self.semantic_error(
                "WAIT requires a valid NUMBER"
            )

        # Semantic validation
        if duration_token.value <= 0:
            self.semantic_error(
                "WAIT duration must be greater than 0"
            )

        # Add information to symbol table
        self.wait_count += 1

        self.symbol_table.add_symbol(
            f"wait_{self.wait_count}_duration",
            duration_token.value
        )

        self.advance()

    # --------------------------------------------------
    # PICK
    #
    # Semantic rule:
    # Robot cannot PICK while already carrying
    # --------------------------------------------------

    def check_pick(self):

        token = self.current_token()

        if token.type != TokenType.PICK:
            self.semantic_error(
                "Expected PICK"
            )

        if self.carrying:
            self.semantic_error(
                "Cannot PICK: robot is already carrying an object"
            )

        # Update robot state
        self.carrying = True

        # Update symbol table
        self.symbol_table.add_symbol(
            "carrying",
            self.carrying
        )

        self.advance()

    # --------------------------------------------------
    # DROP
    #
    # Semantic rule:
    # Robot must be carrying something
    # --------------------------------------------------

    def check_drop(self):

        token = self.current_token()

        if token.type != TokenType.DROP:
            self.semantic_error(
                "Expected DROP"
            )

        if not self.carrying:
            self.semantic_error(
                "Cannot DROP: robot is not carrying an object"
            )

        # Update robot state
        self.carrying = False

        # Update symbol table
        self.symbol_table.add_symbol(
            "carrying",
            self.carrying
        )

        self.advance()

    # --------------------------------------------------
    # INVALID
    # --------------------------------------------------

    def check_invalid(self):

        token = self.current_token()

        self.semantic_error(
            f"Invalid token: {token.value}"
        )

    # --------------------------------------------------
    # COMMAND
    # --------------------------------------------------

    def check_command(self):

        token = self.current_token()

        if token is None:
            return

        if token.type == TokenType.MOVE:

            self.check_move()

        elif token.type == TokenType.TURN:

            self.check_turn()

        elif token.type == TokenType.WAIT:

            self.check_wait()

        elif token.type == TokenType.PICK:

            self.check_pick()

        elif token.type == TokenType.DROP:

            self.check_drop()

        elif token.type == TokenType.INVALID:

            self.check_invalid()

        else:

            self.semantic_error(
                f"Unexpected token: {token.type}"
            )

    # --------------------------------------------------
    # DISPLAY SYMBOL TABLE
    # --------------------------------------------------

    def display_symbol_table(self):

        print("\nSYMBOL TABLE")
        print("-" * 40)

        self.symbol_table.display()

    # --------------------------------------------------
    # MAIN SEMANTIC ANALYSIS
    # --------------------------------------------------

    def analyze(self):

        # Ignore newlines before START
        self.skip_newlines()

        # Check START
        self.check_start()

        # Ignore newline after START
        self.skip_newlines()

        # Process commands until END
        while (
            self.current_token() is not None
            and self.current_token().type != TokenType.END
        ):

            # Check current command
            self.check_command()

            # After every command there must be
            # either NEWLINE or END
            if (
                self.current_token() is not None
                and self.current_token().type != TokenType.NEWLINE
                and self.current_token().type != TokenType.END
            ):

                self.semantic_error(
                    "Expected NEWLINE after command"
                )

            # Skip NEWLINE tokens
            self.skip_newlines()

        # Check END
        self.check_end()

        # Skip newlines after END
        self.skip_newlines()

        # Program must end with EOF
        token = self.current_token()

        if token is None or token.type != TokenType.EOF:

            self.semantic_error(
                "Expected EOF after END"
            )

        # Display symbol table
        self.display_symbol_table()

        return True