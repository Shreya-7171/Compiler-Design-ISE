from codegen.target_code_generator import TargetCodeGenerator
from icg.tac_generator import generate_tac_from_source
from optimizer.optimization_pipeline import OptimizationPipeline


def test_full_codegen_pipeline():
    source = """START
MOVE FORWARD 10
TURN LEFT
PICK
WAIT 4
DROP
END
"""

    # Phase 4: TAC
    tac = generate_tac_from_source(source)

    # Phase 5: Optimization
    pipeline = OptimizationPipeline()
    optimized_tac, _ = pipeline.run(tac)

    # Phase 7: Target Code Generation
    generator = TargetCodeGenerator()
    target_code = generator.generate(optimized_tac)

    assert target_code == [
        "START",
        "MOVE FORWARD 10",
        "TURN LEFT",
        "PICK",
        "WAIT 4",
        "DROP",
        "END",
    ]