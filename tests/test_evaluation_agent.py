import os
from app.agents import evaluation_agent

def test_evaluation_agent():
    state = {
        "solution": """Content:
This is a simple explanation.

Code:
def add(a,b):
    return a+b
""",
        "evaluation": "",
        "logs": []
    }

    result = evaluation_agent(state)

    assert "evaluation" in result and result["evaluation"] != ""
    assert os.path.exists("output/evaluation.txt")

    print("Evaluation Test Passed")