from agent.graph import agent_graph
from langchain_core.messages import HumanMessage

while True:
    user_input = input("User: ")

    if user_input.lower() in {"exit", "quit"}:
        print("Exiting the chatbot")
        break

    try:
        result = agent_graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                }
            )
        
        print("Agent:", result["messages"][-1].content)

    except Exception as e:
        print(f"Error: {e}")