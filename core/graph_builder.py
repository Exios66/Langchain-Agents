# core/graph_builder.py
from langgraph.graph import StateGraph, START, END
from core.state import State
from agents.profiles.professor_athena import create_athena_agent
from agents.profiles.dr_milgrim import create_milgrim_agent
from agents.profiles.yaat import create_yaat_agent
from integrations.human_review import human_review
from integrations.streaming import stream_output
from integrations.error_handling import error_handler

def build_graph() -> StateGraph:
    """Build and return the workflow graph."""
    # Initialize graph
    graph_builder = StateGraph(State)
    
    # Create agent instances
    athena_agent = create_athena_agent()
    milgrim_agent = create_milgrim_agent()
    yaat_agent = create_yaat_agent()
    
    # Register nodes
    graph_builder.add_node('athena', athena_agent)
    graph_builder.add_node('milgrim', milgrim_agent)
    graph_builder.add_node('yaat', yaat_agent)
    graph_builder.add_node('human_review', human_review)
    graph_builder.add_node('stream_output', stream_output)
    graph_builder.add_node('error_handler', error_handler)
    
    # Define edges
    graph_builder.add_edge(START, 'athena')
    graph_builder.add_edge('athena', 'milgrim')
    graph_builder.add_edge('milgrim', 'yaat')
    graph_builder.add_edge('yaat', 'human_review')
    
    # Add conditional edges using 'when'
    graph_builder.add_edge(
        'human_review',
        'stream_output',
        when=lambda s: s['data_store'].get('approved', False)
    )
    graph_builder.add_edge(
        'human_review',
        'error_handler',
        when=lambda s: not s['data_store'].get('approved', False)
    )
    
    # Final edges
    graph_builder.add_edge('stream_output', END)
    graph_builder.add_edge('error_handler', END)
    
    return graph_builder.compile()

# Create compiled graph instance
compiled_graph = build_graph()