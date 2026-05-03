from graph.workflow import app

initial_state = {
    "input": "data/example.pdf",
    "github_query": "",
    "plan": "",
    "solution": "",
    "critique": "",
    "logs": []
}

app.invoke(initial_state)