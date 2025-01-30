# core/graph_builder.py
from langgraph.graph import StateGraph, START, END
from core.state import State
from agents.agent_a import agent_a
from agents.agent_b import agent_b
from agents.subgraph import compiled_subgraph
from integrations.human_review import human_review
from integrations.streaming import stream_output
from integrations.error_handling import error_handler

def build_graph() -> StateGraph:
    """Build and return the workflow graph."""
    # Initialize graph
    graph_builder = StateGraph(State)
    
    # Register nodes
    graph_builder.add_node('subgraph', compiled_subgraph)
    graph_builder.add_node('agent_a', agent_a)
    graph_builder.add_node('agent_b', agent_b)
    graph_builder.add_node('human_review', human_review)
    graph_builder.add_node('stream_output', stream_output)
    graph_builder.add_node('error_handler', error_handler)
    
    # Define edges
    graph_builder.add_edge(START, 'subgraph')
    graph_builder.add_edge('subgraph', 'agent_a')
    graph_builder.add_edge('agent_a', 'agent_b')
    graph_builder.add_edge('agent_b', 'human_review')
    graph_builder.add_edge('human_review', 'stream_output', condition=lambda s: s['data_store'].get('approved', False))
    graph_builder.add_edge('human_review', 'error_handler', condition=lambda s: not s['data_store'].get('approved', False))
    graph_builder.add_edge('stream_output', END)
    graph_builder.add_edge('error_handler', END)
    
    return graph_builder.compile()

# Create compiled graph instance
compiled_graph = build_graph()