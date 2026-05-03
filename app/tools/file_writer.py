from datetime import datetime
import os 

def write_to_file(file_path: str, content: str) -> str:
    """
    Writes content to a file.

    Args:
        file_path (str): Path to save file
        content (str): Content to write

    Returns:
        str: Success or error message
    """
    try:
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        # 🧠 Add timestamp (optional but professional)
        full_path = os.path.join(output_dir, file_path)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"File saved successfully at {full_path}"

    except Exception as e:
        return f"Error writing file: {str(e)}"