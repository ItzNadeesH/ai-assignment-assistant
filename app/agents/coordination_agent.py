from tools.pdf_reader import read_pdf
from state.state import AgentState
from config.llm_config import llm
import os

def coordination_agent(state: AgentState):
    user_input = state["input"]

    content = user_input

    if user_input.endswith(".pdf") and os.path.exists(user_input):
        state["logs"].append("Detected PDF input")
        pdf_text = read_pdf(state["input"])
        content = pdf_text

    prompt = f"""
    You are a coordinator agent.

    Break the task into:
    1. A clear step-by-step PLAN
    2. A SHORT GitHub search query, suitable for this assigment (only a few keywords)

    Return output in this EXACT format:

    PLAN:
    <your plan>

    QUERY:
    <search keywords>

    TASK:
    {content}
    """

    response = llm.invoke(prompt)
    output = response.content if hasattr(response, "content") else str(response)
    
    plan = ""
    query = ""

    try:
        if "QUERY:" in output:
            parts = output.split("QUERY:")
            plan_part = parts[0].replace("PLAN:", "").strip()
            query_part = parts[1].strip()

            plan = plan_part
            query = query_part
        else:
            plan = output
            query = state["input"]  # fallback

    except Exception:
        plan = output
        query = state["input"]

    # Save into state
    state["plan"] = plan
    state["github_query"] = query

    state["logs"].append(f"Plan extracted: {plan}")
    state["logs"].append(f"GitHub query: {query}")

    return state