from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any
from enum import Enum

class EventType(Enum):
    USER_MESSAGE = "USER_MESSAGE"
    LLM_REQUEST = "LLM_REQUEST"
    LLM_RESPONSE = "LLM_RESPONSE"
    TOOL_CALLED = "TOOL_CALLED"
    TOOL_COMPLETED = "TOOL_COMPLETED"
    ERROR = "ERROR"
    CONVERSATION_STARTED = "CONVERSATION_STARTED"
    CONVERSATION_ENDED = "CONVERSATION_ENDED"
    GRAPH_TRANSITION = "GRAPH_TRANSITION"

@dataclass
class Event:
    timestamp: str
    event_type: str
    data: dict[str, Any]

    def to_dict(self):
        return asdict(self)

def create_event(event_type: EventType, data: dict[str, Any]) -> Event:
    return Event(
        timestamp=datetime.now().isoformat(),
        event_type=event_type.value,
        data=data
    )

def log_event(event: Event):
    print(
        f"[{event.timestamp}] "
        f"{event.event_type}: "
        f"{event.data}"
    )