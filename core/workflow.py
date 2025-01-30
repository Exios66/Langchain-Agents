from typing import Dict, Any
from core.state import State
from core.graph_builder import StateGraph
from agents.agent_a import agent_a
from agents.agent_b import agent_b
from agents.subgraph import compiled_subgraph
from integrations.error_handling import handle_errors
from integrations.streaming import stream_results
from integrations.human_review import human_review

class WorkflowManager:
    """Manages the execution flow of the multi-agent system."""
    
    def __init__(self):
        self.graph = StateGraph(State)
        self._build_workflow()
        
    def _build_workflow(self):
        # Add main workflow nodes
        self.graph.add_node('error_handler', handle_errors)
        self.graph.add_node('stream', stream_results)
        self.graph.add_node('review', human_review)
        
        # Integrate subgraph
        self.graph.integrate_subgraph(compiled_subgraph)
        
        # Add edges
        self.graph.add_edge('stream', 'sub_agent')
        self.graph.add_edge('agent_a', 'agent_b')
        self.graph.add_edge('agent_b', 'review')
        
    def execute(self, initial_state: Dict[str, Any]) -> State:
        """Execute the workflow with error handling."""
        try:
            state = State(**initial_state)
            return self.graph.compile().invoke(state)
        except Exception as e:
            return handle_errors(State(messages=[str(e)], data_store={})) 