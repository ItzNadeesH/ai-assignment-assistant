from tools.file_writer import write_to_file
from tools.code_executor import run_python_code
from state.state import AgentState
from config.llm_config import llm

def evaluation_agent(state: AgentState):

    solution = state.get("solution", "")

    # 🧠 Split Content + Code (same format as solution agent)
    content_part = ""
    code_part = ""

    try:
        if "Code:" in solution:
            parts = solution.split("Code:")
            content_part = parts[0].replace("Content:", "").strip()
            code_part = parts[1].strip()
        else:
            content_part = solution
            code_part = "NONE"
    except Exception:
        content_part = solution
        code_part = "NONE"

    # 🧠 Evaluate Content
    content_prompt = f"""
    Evaluate the following theoretical answer.

    Respond in this format:
    Content Evaluation:
    <GOOD / AVERAGE / POOR>
    Reason:
    <brief explanation>

    CONTENT:
    {content_part}
    """

    content_res = llm.invoke(content_prompt)
    content_eval = content_res.content if hasattr(content_res, "content") else str(content_res)

    # 🧠 Evaluate Code (only if exists)
    code_eval = "No code provided."

    if code_part and code_part != "NONE":

        # 🛠 Execute code for validation
        execution_result = run_python_code(code_part)
        state["logs"].append(f"[TOOL] Code Execution (Evaluation): {execution_result}")

        code_prompt = f"""
        Evaluate the following Python code.

        Execution Result:
        {execution_result}

        Respond in this format:
        Code Evaluation:
        <CORRECT / PARTIAL / INCORRECT>
        Reason:
        <brief explanation>

        CODE:
        {code_part}
        """

        code_res = llm.invoke(code_prompt)
        code_eval = code_res.content if hasattr(code_res, "content") else str(code_res)

    # 📊 Combine final evaluation
    final_evaluation = f"""
    ===== EVALUATION REPORT =====

    {content_eval}

    {code_eval}
    """

    state["evaluation"] = final_evaluation
    state["logs"].append(f"Evaluation: {final_evaluation}")

    # 🛠 Save evaluation report
    file_result = write_to_file("evaluation.txt", final_evaluation)
    state["logs"].append(f"[TOOL] File Writer: {file_result}")

    return state