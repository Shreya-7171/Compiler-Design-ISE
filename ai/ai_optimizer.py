import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


class AIOptimizer:

    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="openai/gpt-oss-20b",
            temperature=0
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
You are an AI compiler optimization assistant.

Analyze the following Three Address Code (TAC).

Identify:
1. Possible constant folding
2. Constant propagation opportunities
3. Dead code
4. Algebraic simplification
5. Any other useful optimization

Do NOT modify the TAC.
Only provide optimization suggestions and explain why
each suggestion can improve the code.

TAC:
{tac}

Give the response in this format:

Optimization Suggestions:
- Optimization:
  Instruction:
  Explanation:

If no optimization is possible, clearly say:
"No further optimization suggested."
"""
        )

    def analyze(self, tac):
        tac_text = "\n".join(str(instruction) for instruction in tac)

        chain = self.prompt | self.llm

        response = chain.invoke({
            "tac": tac_text
        })

        content = response.content

        if not content:
            return "No further optimization suggested."

        return content