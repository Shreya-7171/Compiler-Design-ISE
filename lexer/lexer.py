import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "lexer")
    )
)


from rcl_token import TokenType, Token

# Keywords supported by RCL
KEYWORDS = {
    "START": TokenType.START,
    "END": TokenType.END,
    "MOVE": TokenType.MOVE,
    "FORWARD": TokenType.FORWARD,
    "BACKWARD": TokenType.BACKWARD,
    "TURN": TokenType.TURN,
    "LEFT": TokenType.LEFT,
    "RIGHT": TokenType.RIGHT,
    "PICK": TokenType.PICK,
    "DROP": TokenType.DROP,
    "WAIT": TokenType.WAIT
}


class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    # Move to the next character
    def advance(self):
        current_char = self.source[self.position]

        if current_char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

    # Read a word such as MOVE, START, LEFT, etc.
    def read_word(self):
        start_column = self.column
        word = ""

        while (
            self.position < len(self.source)
            and self.source[self.position].isalpha()
        ):
            word += self.source[self.position]
            self.advance()

        # Check whether the word is a valid RCL keyword
        if word in KEYWORDS:
            return Token(
                KEYWORDS[word],
                word,
                self.line,
                start_column
            )

        # If it is not a keyword, mark it as invalid
        return Token(
            TokenType.INVALID,
            word,
            self.line,
            start_column
        )

    # Read a number such as 10, 25, 100, etc.
    def read_number(self):
        start_column = self.column
        number = ""

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            number += self.source[self.position]
            self.advance()

        return Token(
            TokenType.NUMBER,
            int(number),
            self.line,
            start_column
        )

    # Convert the complete source code into tokens
    def tokenize(self):
        tokens = []

        while self.position < len(self.source):

            current_char = self.source[self.position]

            # Ignore spaces
            if current_char == " ":
                self.advance()
                continue

            # Ignore tabs
            if current_char == "\t":
                self.advance()
                continue

            # Handle newline
            if current_char == "\n":
                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\\n",
                        self.line,
                        self.column
                    )
                )

                self.advance()
                continue

            # Handle words
            if current_char.isalpha():
                tokens.append(self.read_word())
                continue

            # Handle numbers
            if current_char.isdigit():
                tokens.append(self.read_number())
                continue

            # Handle invalid characters
            tokens.append(
                Token(
                    TokenType.INVALID,
                    current_char,
                    self.line,
                    self.column
                )
            )

            self.advance()

        # Add EOF token at the end
        tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.line,
                self.column
            )
        )

        return tokens


# Test the lexer
if __name__ == "__main__":

    source = """START
MOVE FORWARD 10
TURN LEFT
PICK
WAIT 2
DROP
END"""

    lexer = Lexer(source)

    tokens = lexer.tokenize()

    print("TOKENS:")
    print("-------")

    for token in tokens:
        print(token)