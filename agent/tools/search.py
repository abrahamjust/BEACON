import os

from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from agent.events import EventType, create_event, log_event

load_dotenv()

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env")

tavily_search = TavilySearchResults(
    api_key=TAVILY_API_KEY,
    max_results=2,
    search_depth='advanced',
    max_tokens=1000
)

@tool
def search_web(query: str):
    """
    Search the web for up-to-date information.

    Use this tool when current information or internet
    search is required to answer the user's question.
    """

    event = create_event(
                EventType.TOOL_CALLED,
                {
                    "tool": "search_web",
                    "query": query
                }
            )
    log_event(event)

    try:
        results = tavily_search.invoke(query)
        formatted = []
        for result in results:
            formatted.append(
                f"Title: {result['title']}\n"
                f"Content: {result['content']}\n"
                f"URL: {result['url']}"
            )

        formatted_results = "\n\n".join(formatted)

        event = create_event(
                    EventType.TOOL_COMPLETED,
                    {
                        "tool": "search_web",
                        "query": query,
                        "result": len(results)
                    }
                )
        log_event(event)

        return formatted_results if formatted_results else "No results found."
    except Exception as e:

        event = create_event(
                    EventType.ERROR,
                    {
                        "tool": "search_web",
                        "error": str(e)
                    }
                )
        log_event(event)

        return f"Error: {e}"
