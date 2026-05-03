import os
from app.agents import analysis_agent

def test_analysis_agent():
    state = {
        "input": "GPA calculator",
        "plan": "Create a GPA calculator in Python",
        "github_query": "python gpa calculator",
        "solution": "",
        "evaluation": "",
        "logs": []
    }

    result = analysis_agent(state)

    print(result)

    assert "plan" in result and result["plan"] != ""
    assert os.path.exists("output/github_projects.txt")

    print("Analysis Test Passed")