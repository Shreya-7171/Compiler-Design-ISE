from optimizer.optimizer import Optimizer
from ai.ai_optimizer import AIOptimizer
from ai.ai_explainer import AIExplainer


class OptimizationPipeline:

    def __init__(self):
        self.optimizer = Optimizer()
        self.ai_optimizer = AIOptimizer()
        self.explainer = AIExplainer()

    def run(self, tac):
        # Rule-based optimization
        optimized_tac = self.optimizer.optimize(tac)

        # AI analysis
        ai_response = self.ai_optimizer.analyze(optimized_tac)

        # Format AI explanation
        report = self.explainer.format_suggestions(ai_response)

        return optimized_tac, report