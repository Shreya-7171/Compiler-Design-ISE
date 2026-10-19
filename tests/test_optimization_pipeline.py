from optimizer.optimization_pipeline import OptimizationPipeline
from icg.intermediate_code import TACInstruction


def test_optimization_pipeline():

    tac = [
        TACInstruction("ADD", 10, 20, "t1"),
        TACInstruction("ADD", "x", 0, "t2"),
        TACInstruction("MUL", "t1", 1, "t3"),
        TACInstruction("ADD", "t3", "t2", "t4"),
        TACInstruction("WAIT", "t4")
    ]

    pipeline = OptimizationPipeline()

    optimized_tac, report = pipeline.run(tac)

    assert optimized_tac
    assert report