from state.state import AgentState
from config.llm_config import llm
from tools.github_tool import search_github_code
from tools.file_writer import write_to_file

def analysis_agent(state: AgentState):

    query = state.get("github_query", state["input"])
    repos = search_github_code(query)

    state["logs"].append(f"[TOOL] GitHub API used with query: {query}")

    formatted_repos = "\n".join([f"{i+1}. {repo}" for i, repo in enumerate(repos)])

    file_result = write_to_file("github_projects.txt", formatted_repos)
    state["logs"].append(f"[TOOL] File Writer: {file_result}")

    prompt = f"""
    You are an analysis agent.

    Convert the plan into clear, structured requirements.

    PLAN:
    {state['plan']}

    OUTPUT FORMAT:
    - List of requirements
    - Key features
    - Suggested approach
    """

    response = llm.invoke(prompt)
    output = response.content if hasattr(response, "content") else str(response)

    state["plan"] = output
    state["logs"].append(f"Analysis: {output}")

    return state