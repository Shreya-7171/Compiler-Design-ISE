from icg.intermediate_code import TACInstruction
from optimizer.optimization_pipeline import OptimizationPipeline
from animation.optimization_animation import run_optimization_animation


def main():

    # Sample TAC for demonstration
    tac = [
        TACInstruction("ADD", 10, 20, "t1"),
        TACInstruction("ADD", "x", 0, "t2"),
        TACInstruction("MUL", "t1", 1, "t3"),
        TACInstruction("ADD", "t3", "t2", "t4"),
        TACInstruction("WAIT", "t4")
    ]

    # Run the actual Phase 6 pipeline
    pipeline = OptimizationPipeline()

    optimized_tac, report = pipeline.run(tac)

    # Show animated result
    run_optimization_animation(
        tac,
        optimized_tac,
        report
    )


if __name__ == "__main__":
    main()