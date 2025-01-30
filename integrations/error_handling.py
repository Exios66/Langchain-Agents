# integrations/error_handling.py
from core.state import State

def error_handler(state: State) -> State:
    """Handle errors in the workflow."""
    state['messages'].append("Error handler invoked.")
    error_msg = state['data_store'].get('error', 'Unknown error occurred')
    state['messages'].append(f"Error handled: {error_msg}")
    return state