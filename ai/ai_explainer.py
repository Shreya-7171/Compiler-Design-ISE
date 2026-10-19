class AIExplainer:

    def format_suggestions(self, ai_response):
        return f"""
========================================
      AI OPTIMIZATION ANALYSIS
========================================

{ai_response}

========================================
"""