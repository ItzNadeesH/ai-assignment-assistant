from tools.code_executor import run_python_code
from tools.file_writer import write_to_file
from state.state import AgentState
from config.llm_config import llm

def solution_agent(state: AgentState):

    prompt = f"""
    You are a solution agent.

    Solve the assignment.

    IMPORTANT:
    - Separate your answer into TWO sections

    Content:
    <answers to theory / explanation questions>

    Code:
    <only Python code if required, otherwise write NONE>

    RULES:
    - Do NOT mix content and code
    - Do NOT include markdown

    REQUIREMENTS:
    {state['plan']}
    """

    response = llm.invoke(prompt)
    output = response.content if hasattr(response, "content") else str(response)

    # 🧠 Parse output
    content_part = ""
    code_part = ""

    try:
        if "Code:" in output:
            parts = output.split("Code:")
            content_part = parts[0].replace("Content:", "").strip()
            code_part = parts[1].strip()
        else:
            content_part = output
            code_part = "NONE"
    except Exception:
        content_part = output
        code_part = "NONE"

    state["solution"] = content_part
    state["logs"].append(f"Content: {content_part}")

    # 🛠 Save content
    write_to_file("report.txt", content_part)
    state["logs"].append("[TOOL] File Writer: report.txt saved")

    # 🧠 Handle code only if exists
    if code_part and code_part != "NONE":

        state["logs"].append(f"Code detected: {code_part}")

        # 🛠 Execute code
        execution_result = run_python_code(code_part)
        state["logs"].append(f"[TOOL] Code Execution: {execution_result}")

        # 🛠 Save code
        write_to_file("solution.py", code_part)
        state["logs"].append("[TOOL] File Writer: solution.py saved")

    else:
        state["logs"].append("[INFO] No code required")

    return state