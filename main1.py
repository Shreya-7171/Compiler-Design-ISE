from lexer.lexer import Lexer
from parser.parser import Parser

 #syntax error
# =========================================================
# SOURCE PROGRAM
# =========================================================

source_code = """START
MOVE LEFT 10
TURN RIGHT
PICK
DROP
END
"""


print("=" * 60)
print("RCL COMPILER - SYNTAX ERROR DEMO")
print("=" * 60)

print("\nSOURCE CODE")
print("-" * 60)
print(source_code)


# =========================================================
# PHASE 1: LEXICAL ANALYSIS
# =========================================================

print("\n" + "=" * 60)
print("PHASE 1: LEXICAL ANALYSIS")
print("=" * 60)

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)

print("\nLexical analysis successful!")


# =========================================================
# PHASE 2: SYNTAX ANALYSIS
# =========================================================

print("\n" + "=" * 60)
print("PHASE 2: SYNTAX ANALYSIS")
print("=" * 60)

try:

    parser = Parser(tokens)

    tree = parser.parse()

    print("\nParsing successful!")
    print("Parse tree generated.")

except SyntaxError as e:

    print("\nSYNTAX ERROR")
    print("-" * 60)
    print(e)

    print("\nCompilation stopped at Phase 2.")

    raise SystemExit(1)


# =========================================================
# PHASE 3
# =========================================================

print("\nPhase 3 will not execute because syntax analysis failed.")