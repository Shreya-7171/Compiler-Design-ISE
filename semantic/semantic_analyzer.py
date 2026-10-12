from lexer.rcl_token import TokenType


class SemanticError(Exception):
    """Raised when a semantic rule is violated."""
    pass


class SemanticAnalyzer:

    def __init__(self, tokens):

        self.tokens = tokens
        self.current = 0

        # Robot state
        self.carrying = False

    def current_token(self):

        if self.current >= len(self.tokens):
            return None

        return self.tokens[self.current]

    def advance(self):

        self.current += 1

    def semantic_error(self, message):

        token = self.current_token()

        if token is None:
            raise SemanticError(message)

        raise SemanticError(
            f"Semantic Error at line {token.line}, "
            f"column {token.column}: {message}"
        )

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

        self.advance()

    # --------------------------------------------------
    # MOVE
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

        token = self.current_token()

        if token.type not in (
            TokenType.FORWARD,
            TokenType.BACKWARD
        ):
            self.semantic_error(
                "MOVE requires FORWARD or BACKWARD"
            )

        self.advance()

        token = self.current_token()

        if token.type != TokenType.NUMBER:
            self.semantic_error(
                "MOVE requires a valid NUMBER"
            )

        # Check distance
        if token.value <= 0:
            self.semantic_error(
                "MOVE distance must be greater than 0"
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

        token = self.current_token()

        if token.type not in (
            TokenType.LEFT,
            TokenType.RIGHT
        ):
            self.semantic_error(
                "TURN requires LEFT or RIGHT"
            )

        self.advance()

    # --------------------------------------------------
    # WAIT
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

        token = self.current_token()

        if token.type != TokenType.NUMBER:
            self.semantic_error(
                "WAIT requires a valid NUMBER"
            )

        # Check wait duration
        if token.value <= 0:
            self.semantic_error(
                "WAIT duration must be greater than 0"
            )

        self.advance()

    # --------------------------------------------------
    # PICK
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

        self.carrying = True

        self.advance()

    # --------------------------------------------------
    # DROP
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

        self.carrying = False

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
    # MAIN SEMANTIC ANALYSIS
    # --------------------------------------------------

    def analyze(self):

        self.skip_newlines()

        self.check_start()

        self.skip_newlines()

        while (
            self.current_token() is not None
            and self.current_token().type != TokenType.END
        ):

            self.check_command()

            if (
                self.current_token() is not None
                and self.current_token().type != TokenType.NEWLINE
                and self.current_token().type != TokenType.END
            ):

                self.semantic_error(
                    "Expected NEWLINE after command"
                )

            self.skip_newlines()

        self.check_end()

        self.skip_newlines()

        token = self.current_token()

        if token is None or token.type != TokenType.EOF:

            self.semantic_error(
                "Expected EOF after END"
            )

        return True