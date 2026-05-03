import fitz

def read_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path (str): Path to PDF file

    Returns:
        str: Extracted text
    """
    try:
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:
        return f"Error reading PDF: {str(e)}"