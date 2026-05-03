from app.agents import coordination_agent

def test_coordinator_agent():
    state = {
        "input": "Write a Python program to calculate GPA",
        "plan": "",
        "github_query": "",
        "solution": "",
        "evaluation": "",
        "logs": []
    }

    result = coordination_agent(state)

    assert "plan" in result and result["plan"] != ""
    assert "github_query" in result and result["github_query"] != ""

    print("Coordinator Test Passed")