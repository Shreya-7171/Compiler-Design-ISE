class ParserPartA:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def current_token(self):
        return self.tokens[self.current]

    def advance(self):
        self.current += 1

    def syntax_error(self, message):
        token = self.current_token()

        raise SyntaxError(
            f"Syntax Error at line {token.line}, "
            f"column {token.column}: {message}"
        )

    # START
    def parse_start(self):
        token = self.current_token()

        if token.type != "START":
            self.syntax_error("Expected START")

        self.advance()
        return True

    # END
    def parse_end(self):
        token = self.current_token()

        if token.type != "END":
            self.syntax_error("Expected END")

        self.advance()
        return True
    
    # MOVE
    # MOVE FORWARD NUMBER
    # MOVE BACKWARD NUMBER
    def parse_move(self):
        token = self.current_token()

        if token.type != "MOVE":
            self.syntax_error("Expected MOVE")

        self.advance()

        token = self.current_token()

        if token.type not in ("FORWARD", "BACKWARD"):
            self.syntax_error(
                "Expected FORWARD or BACKWARD after MOVE"
            )

        self.advance()

        token = self.current_token()

        if token.type != "NUMBER":
            self.syntax_error(
                "Expected NUMBER after MOVE direction"
            )

        self.advance()

        return True

    # TURN
    # TURN LEFT
    # TURN RIGHT
    def parse_turn(self):
        token = self.current_token()

        if token.type != "TURN":
            self.syntax_error("Expected TURN")

        self.advance()

        token = self.current_token()

        if token.type not in ("LEFT", "RIGHT"):
            self.syntax_error(
                "Expected LEFT or RIGHT after TURN"
            )

        self.advance()

        return True
    # NEWLINE
    def parse_newline(self):
        token = self.current_token()

        if token.type != "NEWLINE":
            self.syntax_error("Expected NEWLINE")

        self.advance()
        return True
    # EOF
    def parse_eof(self):
        token = self.current_token()

        if token.type != "EOF":
            self.syntax_error("Expected EOF")

        self.advance()
        return True
    # INVALID
    def parse_invalid(self):
        token = self.current_token()

        if token.type != "INVALID":
            self.syntax_error("Expected INVALID")

        self.syntax_error(
            f"Invalid token: {token.value}"
        )