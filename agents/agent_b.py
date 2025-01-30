# agents/agent_b.py
from core.state import State
from core.commands import Command

def agent_b(state: State) -> State:
    """Secondary agent for advanced processing."""
    state['messages'].append("Agent B processing started.")
    state['data_store']['b_processed'] = state['data_store'].get('a_processed', '').upper()
    state['messages'].append("Agent B processing complete.")
    return state