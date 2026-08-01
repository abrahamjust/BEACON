from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
        
    Mathematical expressions can include numbers, operators (+, -, *, /), and parentheses.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"