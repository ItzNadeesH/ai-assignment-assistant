import subprocess
import tempfile

def run_python_code(code: str) -> str:
    """
    Executes Python code safely.

    Args:
        code (str): Python code

    Returns:
        str: output or error
    """
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            file_path = f.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.stdout:
            return result.stdout
        else:
            return result.stderr

    except Exception as e:
        return str(e)