from agent.graph import agent_graph
from agent.events import EventType, create_event, log_event
from langchain_core.messages import HumanMessage
import uuid

conversation_id = str(uuid.uuid4())

event = create_event(
            EventType.CONVERSATION_STARTED,
            {
                "conversation_id": conversation_id
            }
        )
log_event(event)

while True:
    user_input = input("User: ")
    event = create_event(
        EventType.USER_MESSAGE,
        {
            "conversation_id": conversation_id,
            "message": user_input
        }
    )
    log_event(event)

    if user_input.lower() in {"exit", "quit"}:
        print("Exiting the chatbot")
        event = create_event(
                    EventType.CONVERSATION_ENDED,
                    {
                        "conversation_id": conversation_id,
                        "reason": "user exit"
                    }
                )
        log_event(event)
        break

    try:
        result = agent_graph.invoke(
                {
                    "conversation_id": conversation_id,
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                }
            )
        
        print("Agent:", result["messages"][-1].content)

    except Exception as e:
        event = create_event(
                    EventType.ERROR,
                    {
                        "tool": "app",
                        "error": str(e)
                    }
                )
        log_event(event)
        print(f"Error: {e}")