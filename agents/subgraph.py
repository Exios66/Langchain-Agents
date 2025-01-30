# agents/subgraph.py
from core.state import State
from core.graph_builder import StateGraph

def sub_agent(state: State) -> State:
    """Sub-agent processes and normalizes input data."""
    state['messages'].append("Sub-agent preprocessing started.")
    state['data_store']['sub_processed'] = state['data_store'].get('input_data', '').lower()
    state['messages'].append("Sub-agent preprocessing complete.")
    return state

# Build the subgraph
subgraph_builder = StateGraph(State)
subgraph_builder.add_node('sub_agent', sub_agent)
subgraph_builder.add_edge('sub_agent', 'agent_a')
compiled_subgraph = subgraph_builder.compile()