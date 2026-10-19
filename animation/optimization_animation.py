import time


def show_title():
    print("\n" + "=" * 60)
    print("          PHASE 6: CODE OPTIMIZATION + AI")
    print("=" * 60)
    time.sleep(1)


def show_stage(title):
    print("\n" + "-" * 60)
    print(f"  {title}")
    print("-" * 60)
    time.sleep(1)


def show_tac(title, tac):
    print(f"\n{title}")
    for instruction in tac:
        print(f"   {instruction}")
        time.sleep(0.4)


def run_optimization_animation(original_tac, optimized_tac, ai_report):
    show_title()

    show_stage("ORIGINAL TAC")
    show_tac("Before Optimization:", original_tac)

    show_stage("OPTIMIZATION PASSES")

    print("   🔍 Constant Propagation...")
    time.sleep(1)

    print("   ⚡ Constant Folding...")
    time.sleep(1)

    print("   ⚡ Algebraic Simplification...")
    time.sleep(1)

    print("   🗑️ Dead Code Elimination...")
    time.sleep(1)

    show_stage("OPTIMIZED TAC")
    show_tac("After Optimization:", optimized_tac)

    show_stage("AI OPTIMIZATION ANALYSIS")

    print("   🤖 AI is analyzing the TAC...")
    time.sleep(2)

    print("\n" + ai_report)

    show_stage("PHASE 6 COMPLETE")

    print("   ✓ Code optimization completed")
    print("   ✓ AI analysis completed")
    print("   ✓ Optimization report generated")

    print("\n" + "=" * 60)