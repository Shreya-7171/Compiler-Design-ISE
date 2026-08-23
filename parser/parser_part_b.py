class ParserPartB:

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

    def parse_pick(self):
        token = self.current_token()

        if token.type != "PICK":
            self.syntax_error("Expected PICK")

        self.advance()
        return True

    def parse_drop(self):
        token = self.current_token()

        if token.type != "DROP":
            self.syntax_error("Expected DROP")

        self.advance()
        return True

    def parse_wait(self):
        token = self.current_token()

        if token.type != "WAIT":
            self.syntax_error("Expected WAIT")

        self.advance()

        token = self.current_token()

        if token.type != "NUMBER":
            self.syntax_error("Expected NUMBER after WAIT")

        self.advance()
        return True