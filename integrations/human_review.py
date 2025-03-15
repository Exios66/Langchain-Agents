# integrations/human_review.py
from typing import Dict, Any
from core.state import State

def validate_agent_output(state: State) -> bool:
    """Validate the outputs from all agents that ran."""
    workflow_type = state['data_store'].get('workflow_type', 'sequential')
    requested_agents = state['data_store'].get('agents', [])
    completed_agents = state['data_store'].get('completed_agents', [])
    
    # Ensure all requested agents have completed
    if not completed_agents or set(completed_agents) != set(requested_agents):
        state['data_store']['error'] = "Not all requested agents have completed"
        return False
    
    # Check each agent's analysis
    for agent in requested_agents:
        analysis_key = f"{agent.replace('professor_', '').replace('dr_', '')}_analysis"
        analysis = state['data_store'].get(analysis_key)
        
        if not analysis:
            state['data_store']['error'] = f"Missing analysis from agent: {agent}"
            return False
            
        # Validate analysis has required fields and non-empty recommendations
        if not all(key in analysis for key in ['recommendations']):
            state['data_store']['error'] = f"Incomplete analysis from agent: {agent}"
            return False
            
        if not analysis['recommendations']:
            state['data_store']['error'] = f"No recommendations provided by agent: {agent}"
            return False
    
    # Additional validation for parallel workflows
    if workflow_type == 'parallel':
        # Ensure all parallel executions were independent
        for agent in requested_agents:
            analysis_key = f"{agent.replace('professor_', '').replace('dr_', '')}_analysis"
            analysis = state['data_store'].get(analysis_key)
            if analysis.get('previous_analyses_integrated'):
                state['data_store']['error'] = f"Agent {agent} had dependencies in parallel workflow"
                return False
    
    return True

def human_review(state: State) -> State:
    """Simulate human review of agent output."""
    state['messages'].append("Human review started.")
    
    # Validate agent outputs
    if validate_agent_output(state):
        state['data_store']['approved'] = True
        state['messages'].append("Human review: Output approved.")
    else:
        state['data_store']['approved'] = False
        if 'error' not in state['data_store']:
            state['data_store']['error'] = "Invalid or incomplete agent output"
        state['messages'].append("Human review: Output rejected.")
    
    return state