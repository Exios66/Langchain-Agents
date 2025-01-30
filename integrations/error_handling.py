# integrations/error_handling.py
import logging
from core.state import State

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def error_handler(state: State) -> State:
    """Handles errors in the workflow and logs them."""
    try:
        state['messages'].append("Executing critical task...")
        raise ValueError("Simulated error for testing.")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        state['messages'].append(f"Error logged: {str(e)}")
        state['data_store']['error'] = str(e)
    
    return state