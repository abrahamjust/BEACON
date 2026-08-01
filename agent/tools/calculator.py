from langchain_core.tools import tool
from agent.events import EventType, create_event, log_event

@tool
def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns the result.
        
    Mathematical expressions can include numbers, operators (+, -, *, /), and parentheses.
    """

    event = create_event(
                EventType.TOOL_CALLED,
                {
                    "tool": "calculator",
                    "expression": expression
                }
            )
    log_event(event)

    try:
        result = eval(expression)

        event = create_event(
                    EventType.TOOL_COMPLETED,
                    {
                        "tool": "calculator",
                        "result": result
                    }
                )
        log_event(event)

        return str(result)
    except Exception as e:
        event = create_event(
                    EventType.ERROR,
                    {
                        "tool": "calculator",
                        "error": str(e)
                    }
                )
        log_event(event)

        return f"Error: {e}"
    
