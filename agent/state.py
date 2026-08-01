from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class AgentState(TypedDict):
    """Represents the state of an agent."""

    messages: Annotated[list[dict], add_messages]