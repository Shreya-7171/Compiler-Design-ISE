from ai.ai_optimizer import AIOptimizer
from ai.ai_explainer import AIExplainer


def test_ai_optimizer():

    tac = [
        "t1 = 10 + 20",
        "t2 = x + 0",
        "t3 = t1 * 1",
        "t4 = t2 + 5"
    ]

    optimizer = AIOptimizer()

    result = optimizer.analyze(tac)

    explainer = AIExplainer()

    formatted_result = explainer.format_suggestions(result)

    print("\n")
    print(formatted_result)

    assert result
    assert formatted_result