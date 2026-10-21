
from lexer.lexer import Lexer
from parser.parser import Parser
from parser.tree_visualizer import TreeVisualizer
from semantic.semantic_analyzer import SemanticAnalyzer, SemanticError

from icg.tac_generator import generate_tac_from_source
from optimizer.optimization_pipeline import OptimizationPipeline
from codegen.target_code_generator import TargetCodeGenerator


# ---------------------------------------------------------
# SOURCE PROGRAM
# ---------------------------------------------------------

source_code = """START
MOVE FORWARD 10
TURN LEFT
PICK
WAIT 4
DROP
END
"""


print("=" * 60)
print("RCL COMPILER")
print("=" * 60)

print("\nSOURCE CODE")
print("-" * 60)
print(source_code)


# ---------------------------------------------------------
# PHASE 1: LEXICAL ANALYSIS
# ---------------------------------------------------------

print("=" * 60)
print("PHASE 1: LEXICAL ANALYSIS")
print("=" * 60)

lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)


# ---------------------------------------------------------
# PHASE 2: SYNTAX ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PHASE 2: SYNTAX ANALYSIS")
print("=" * 60)

try:
    parser = Parser(tokens)

    # Parser generates the actual syntax tree
    tree = parser.parse()

    print("\nParsing successful!")
    print("Parse tree generated.")

    # Visualizer can be enabled later if required
    # visualizer = TreeVisualizer(tree)
    # visualizer.run()

except SyntaxError as e:
    print("\nSyntax Error:")
    print(e)
    raise SystemExit(1)


# ---------------------------------------------------------
# PHASE 3: SEMANTIC ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PHASE 3: SEMANTIC ANALYSIS")
print("=" * 60)

try:
    semantic_analyzer = SemanticAnalyzer(tokens)

    semantic_analyzer.analyze()

    print("\nSemantic analysis successful!")

except SemanticError as e:
    print("\nSemantic Error:")
    print(e)
    raise SystemExit(1)


# ---------------------------------------------------------
# PHASE 4: THREE ADDRESS CODE GENERATION
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PHASE 4: THREE ADDRESS CODE GENERATION")
print("=" * 60)

try:
    # Generate actual TACInstruction objects
    tac = generate_tac_from_source(source_code)

    for instruction in tac:
        print(instruction)

except (SyntaxError, SemanticError, ValueError) as e:
    print("\nTAC Generation Error:")
    print(e)
    raise SystemExit(1)


# ---------------------------------------------------------
# PHASE 5: CODE OPTIMIZATION + AI ANALYSIS
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PHASE 5: CODE OPTIMIZATION + AI ANALYSIS")
print("=" * 60)

try:
    optimization_pipeline = OptimizationPipeline()

    optimized_tac, ai_report = optimization_pipeline.run(tac)

    print("\nOPTIMIZED TAC")
    print("-" * 60)

    for instruction in optimized_tac:
        print(instruction)

    print("\nAI OPTIMIZATION REPORT")
    print("-" * 60)
    print(ai_report)

except Exception as e:
    print("\nOptimization Error:")
    print(e)
    raise SystemExit(1)



# ---------------------------------------------------------
# PHASE 6: TARGET CODE GENERATION
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("PHASE 6: TARGET CODE GENERATION")
print("=" * 60)

try:
    target_generator = TargetCodeGenerator()

    target_code = target_generator.generate(optimized_tac)

    print("\nFINAL TARGET CODE")
    print("-" * 60)

    for line in target_code:
        print(line)

except (TypeError, ValueError) as e:
    print("\nTarget Code Generation Error:")
    print(e)
    raise SystemExit(1)


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("COMPILATION SUCCESSFUL")
print("=" * 60)