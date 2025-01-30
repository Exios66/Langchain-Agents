# integrations/human_review.py
from core.state import State

def human_review(state: State) -> State:
    """Simulate human review of agent output."""
    state['messages'].append("Human review started.")
    
    # Simulate review decision (in real implementation, this would be interactive)
    processed_result = state['data_store'].get('b_processed', '')
    if processed_result and len(processed_result) > 0:
        state['data_store']['approved'] = True
        state['messages'].append("Human review: Output approved.")
    else:
        state['data_store']['approved'] = False
        state['data_store']['error'] = "Empty or invalid output"
        state['messages'].append("Human review: Output rejected.")
    
    return state