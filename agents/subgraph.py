# agents/subgraph.py
from core.state import State
from langgraph.graph import StateGraph, START, END

def sub_agent(state: State) -> State:
    """Sub-agent processes and normalizes input data."""
    state['messages'].append("Sub-agent preprocessing started.")
    state['data_store']['sub_processed'] = state['data_store'].get('input_data', '').lower()
    state['messages'].append("Sub-agent preprocessing complete.")
    return state

def build_subgraph() -> StateGraph:
    """Build and return the subgraph."""
    # Initialize subgraph
    subgraph_builder = StateGraph(State)
    
    # Add nodes
    subgraph_builder.add_node('sub_agent', sub_agent)
    
    # Add edges with START and END
    subgraph_builder.add_edge(START, 'sub_agent')
    subgraph_builder.add_edge('sub_agent', END)
    
    return subgraph_builder.compile()

# Create compiled subgraph instance
compiled_subgraph = build_subgraph()