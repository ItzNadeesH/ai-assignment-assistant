from app.graph.workflow import app

def test_full_pipeline():
    state = {
        "input": "Write a Python program to calculate GPA",
        "plan": "",
        "github_query": "",
        "solution": "",
        "evaluation": "",
        "logs": []
    }

    app.invoke(state)

    assert state["solution"] != ""
    assert state["evaluation"] != ""

    print("Full Pipeline Test Passed")