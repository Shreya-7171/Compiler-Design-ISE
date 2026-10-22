#semantic error 
from lexer.lexer import Lexer
from parser.parser import Parser
from parser.tree_visualizer import TreeVisualizer
from semantic.semantic_analyzer import SemanticAnalyzer, SemanticError


# =========================================================
# SOURCE PROGRAM
# =========================================================

source_code = """START
PICK
PICK
DROP
END
"""


print("=" * 60)
print("RCL COMPILER - SEMANTIC ERROR DEMO")
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
    print("Syntax is valid.")
    print("Parse tree generated.")

    # Show parse tree
    visualizer = TreeVisualizer(tree)
    visualizer.run()

except SyntaxError as e:

    print("\nSYNTAX ERROR")
    print("-" * 60)
    print(e)

    raise SystemExit(1)


# =========================================================
# PHASE 3: SEMANTIC ANALYSIS
# =========================================================

print("\n" + "=" * 60)
print("PHASE 3: SEMANTIC ANALYSIS")
print("=" * 60)

try:

    semantic_analyzer = SemanticAnalyzer(tokens)

    semantic_analyzer.analyze()

    print("\nSemantic analysis successful!")

except SemanticError as e:

    print("\nSEMANTIC ERROR")
    print("-" * 60)
    print(e)

    print("\nCompilation stopped at Phase 3.")

    raise SystemExit(1)


# =========================================================
# PHASE 4, 5, 6
# =========================================================

print("\nPhase 4, 5 and 6 will not execute.")