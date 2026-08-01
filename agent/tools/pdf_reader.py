from langchain_core.tools import tool

@tool
def pdf_reader(file_path: str):
    """
    Read and extract text from a PDF file.

    Use this tool when you need to analyze the content of a PDF document.
    """
    # Implementation for reading PDF would go here
    pass