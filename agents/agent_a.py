# agents/agent_a.py
from core.state import State

def agent_a(state: State) -> State:
    """Agent A processes data and updates the state."""
    input_data = state['data_store'].get('input_data', '')
    processed_data = input_data.upper()  # Example transformation
    state['data_store']['agent_a_output'] = processed_data
    state['messages'].append("Agent A processed the data.")
    return state