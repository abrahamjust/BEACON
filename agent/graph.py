from agent.llm import get_llm
from langgraph.graph import StateGraph
from agent.state import AgentState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import END, START

from agent.tools.calculator import calculator
from agent.tools.pdf_reader import pdf_reader
from agent.tools.search import search_web

llm = get_llm()
tools = [
    calculator,
    search_web,
    pdf_reader
]

llm_with_tools = llm.bind_tools(tools)
graph_builder = StateGraph(AgentState)
tool_node = ToolNode(tools)

def chatbot(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])

    return {
        "messages": [response]
    }

graph_builder.add_node(
    "chatbot", chatbot
)
graph_builder.add_node(
    "tools", tool_node
)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)

graph_builder.add_edge("tools", "chatbot")

agent_graph = graph_builder.compile()
print("Graph compiled successfully.")