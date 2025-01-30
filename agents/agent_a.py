# agents/agent_a.py
from core.state import State

def agent_a(state: State) -> State:
    """Primary agent for initial processing."""
    state['messages'].append("Agent A processing started.")
    # Process the subgraph output
    sub_processed = state['data_store'].get('sub_processed', '')
    state['data_store']['a_processed'] = f"Agent A processed: {sub_processed}"
    state['messages'].append("Agent A processing complete.")
    return state