# integrations/error_handling.py
from typing import Dict, Any
from core.state import State

def validate_workflow_input(input_data: Dict[str, Any]) -> str:
    """Validate the workflow input data."""
    if not input_data.get('query'):
        return "Missing required field: query"
    if not isinstance(input_data.get('parameters', {}), dict):
        return "Invalid parameters: must be a dictionary"
    return ""

def validate_workflow_config(state: State) -> str:
    """Validate the workflow configuration."""
    if not state['data_store'].get('agents'):
        return "No agents specified for workflow"
    if not state['data_store'].get('workflow_type') in ['sequential', 'parallel', 'hybrid']:
        return "Invalid workflow type"
    return ""

def error_handler(state: State) -> State:
    """Handle errors in the workflow."""
    state['messages'].append("Error handler invoked.")
    
    # Check for input validation errors
    if input_error := validate_workflow_input(state['data_store'].get('input_data', {})):
        state['data_store']['error'] = f"Input validation error: {input_error}"
        state['messages'].append(f"Error handled: {input_error}")
        return state
        
    # Check for workflow configuration errors
    if config_error := validate_workflow_config(state):
        state['data_store']['error'] = f"Configuration error: {config_error}"
        state['messages'].append(f"Error handled: {config_error}")
        return state
        
    # Check for agent execution errors
    if 'error' in state['data_store']:
        error_msg = state['data_store']['error']
        state['messages'].append(f"Error handled: {error_msg}")
        return state
        
    # Handle unknown errors
    state['data_store']['error'] = "Unknown error occurred"
    state['messages'].append("Error handled: Unknown error occurred")
    return state