import os
from app.agents import solution_agent

def test_solution_agent():
    state = {
        "input": "Write a Python function to add two numbers",
        "plan": "Create a function that returns sum of two numbers",
        "solution": "",
        "evaluation": "",
        "logs": []
    }

    result = solution_agent(state)

    assert "solution" in result
    assert os.path.exists("output/report.txt") or os.path.exists("output/solution.py")

    print("Solution Test Passed")