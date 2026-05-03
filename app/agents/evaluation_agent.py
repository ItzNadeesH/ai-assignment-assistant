from typing import Tuple

from tools.file_writer import write_to_file
from tools.code_executor import run_python_code
from state.state import AgentState
from config.llm_config import llm


def _split_solution(solution: str) -> Tuple[str, str]:
    """Split `solution` into a content part and a code part.

    Preserves original behavior: if no `Code:` marker is present, returns
    the full solution as content and `"NONE"` for the code part.
    """
    try:
        if "Code:" in solution:
            parts = solution.split("Code:", 1)
            content_part = parts[0].replace("Content:", "").strip()
            code_part = parts[1].strip()
        else:
            content_part = solution
            code_part = "NONE"
    except Exception:
        content_part = solution
        code_part = "NONE"
    return content_part, code_part


def _llm_invoke(prompt: str) -> str:
    """Invoke the configured LLM and return a string result safely."""
    res = llm.invoke(prompt)
    return getattr(res, "content", str(res))


def evaluation_agent(state: AgentState):
    """Evaluate a solution stored in `state['solution']`.

    This function was refactored for clarity only; behavior remains the same.
    """

    solution = state.get("solution", "")

    # Split Content + Code (same format as solution agent)
    content_part, code_part = _split_solution(solution)

    # Build content evaluation prompt
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

    content_eval = _llm_invoke(content_prompt)

    # Evaluate Code (only if exists)
    code_eval = "No code provided."

    if code_part and code_part != "NONE":
        # Execute code for validation and log the result
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

        code_eval = _llm_invoke(code_prompt)

    # Combine final evaluation
    final_evaluation = f"""
    ===== EVALUATION REPORT =====

    {content_eval}

    {code_eval}
    """

    state["evaluation"] = final_evaluation
    state["logs"].append(f"Evaluation: {final_evaluation}")

    # Save evaluation report
    file_result = write_to_file("evaluation.txt", final_evaluation)
    state["logs"].append(f"[TOOL] File Writer: {file_result}")

    return state