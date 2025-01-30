# core/graph_builder.py
from typing import Annotated, Sequence
from langgraph.graph import StateGraph, START, END
from core.state import State
from agents.profiles.professor_athena import create_athena_agent
from agents.profiles.dr_milgrim import create_milgrim_agent
from agents.profiles.yaat import create_yaat_agent
from integrations.human_review import human_review
from integrations.streaming import stream_output
from integrations.error_handling import error_handler

def should_stream(state: State) -> Sequence[str]:
    """Determine if output should be streamed."""
    return ["stream_output"] if state['data_store'].get('approved', False) else ["error_handler"]

def build_graph() -> StateGraph:
    """Build and return the workflow graph."""
    # Initialize graph
    graph = StateGraph(State)
    
    # Create agent instances
    athena_agent = create_athena_agent()
    milgrim_agent = create_milgrim_agent()
    yaat_agent = create_yaat_agent()
    
    # Register nodes
    graph.add_node("athena", athena_agent)
    graph.add_node("milgrim", milgrim_agent)
    graph.add_node("yaat", yaat_agent)
    graph.add_node("human_review", human_review)
    graph.add_node("stream_output", stream_output)
    graph.add_node("error_handler", error_handler)
    
    # Define the flow
    graph.add_edge(START, "athena")
    graph.add_edge("athena", "milgrim")
    graph.add_edge("milgrim", "yaat")
    graph.add_edge("yaat", "human_review")
    
    # Conditional branching
    graph.add_edge("human_review", should_stream)
    graph.add_edge("stream_output", END)
    graph.add_edge("error_handler", END)
    
    return graph.compile()

# Create compiled graph instance
compiled_graph = build_graph()