# integrations/human_review.py
from core.state import State

def human_review(state: State) -> State:
    """Human approval required before proceeding."""
    state['messages'].append("Awaiting human review...")
    user_input = input("Approve the processed data? (yes/no): ").strip().lower()
    
    if user_input != "yes":
        state['messages'].append("Human review rejected the process.")
        state['data_store']['approved'] = False
        return state
    
    state['messages'].append("Human review approved the process.")
    state['data_store']['approved'] = True
    return state