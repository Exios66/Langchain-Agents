from typing import Dict, Any
from core.state import State
from core.graph_builder import compiled_graph

class WorkflowManager:
    """Manages the execution of the agent workflow."""
    
    def __init__(self):
        self.graph = compiled_graph
    
    def execute(self, initial_state: Dict[str, Any]) -> State:
        """Execute the workflow with the given initial state."""
        try:
            state = State(**initial_state)
            return self.graph.invoke(state)
        except Exception as e:
            return State(
                messages=[f"Workflow error: {str(e)}"],
                data_store={'error': str(e)}
            ) 