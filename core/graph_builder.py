# core/graph_builder.py
from typing import Annotated, Sequence, TypedDict, Union
from langgraph.graph import StateGraph, START, END
from core.state import State
from agents.profiles.professor_athena import create_athena_agent
from agents.profiles.dr_milgrim import create_milgrim_agent
from agents.profiles.yaat import create_yaat_agent
from integrations.human_review import human_review
from integrations.streaming import stream_output
from integrations.error_handling import error_handler

class AgentState(TypedDict):
    next: str

def route_review(state: State) -> AgentState:
    """Route based on review outcome."""
    next_step = "stream_output" if state['data_store'].get('approved', False) else "error_handler"
    return {"next": next_step}

def build_graph() -> StateGraph:
    """Build and return the workflow graph."""
    # Initialize graph
    graph = StateGraph(State)
    
    # Create agent instances
    agents = {
        "professor_athena": create_athena_agent(),
        "dr_milgrim": create_milgrim_agent(),
        "yaat": create_yaat_agent()
    }
    
    # Register all possible nodes
    for agent_name, agent in agents.items():
        graph.add_node(agent_name, agent)
    graph.add_node("human_review", human_review)
    graph.add_node("stream_output", stream_output)
    graph.add_node("error_handler", error_handler)
    
    def get_next_agent(state: State) -> AgentState:
        """Determine the next agent based on workflow type and current state."""
        workflow_type = state['data_store'].get('workflow_type', 'sequential')
        requested_agents = state['data_store'].get('agents', [])
        current_agent = state['data_store'].get('current_agent', None)
        
        if not requested_agents:
            return {"next": "error_handler"}
            
        if workflow_type == "parallel":
            # In parallel mode, all agents run independently
            # This is a simplified version - in reality, you'd want to spawn parallel tasks
            remaining_agents = [a for a in requested_agents if a not in state['data_store'].get('completed_agents', [])]
            if remaining_agents:
                next_agent = remaining_agents[0]
                if 'completed_agents' not in state['data_store']:
                    state['data_store']['completed_agents'] = []
                state['data_store']['completed_agents'].append(next_agent)
                return {"next": next_agent}
            return {"next": "human_review"}
            
        elif workflow_type == "sequential":
            # In sequential mode, agents run one after another
            if current_agent is None:
                if requested_agents:
                    state['data_store']['current_agent'] = requested_agents[0]
                    return {"next": requested_agents[0]}
            else:
                current_idx = requested_agents.index(current_agent)
                if current_idx + 1 < len(requested_agents):
                    next_agent = requested_agents[current_idx + 1]
                    state['data_store']['current_agent'] = next_agent
                    return {"next": next_agent}
            return {"next": "human_review"}
            
        elif workflow_type == "hybrid":
            # In hybrid mode, some agents run in parallel and others sequentially
            # This is a simplified version that treats it as sequential
            return get_next_agent(state)  # Reuse sequential logic for now
            
        return {"next": "error_handler"}
    
    # Add dynamic routing
    graph.add_node("route_agents", get_next_agent)
    
    # Define the flow
    graph.add_edge(START, "route_agents")
    
    # Connect each agent to the router
    for agent_name in agents:
        graph.add_edge("route_agents", agent_name)
        graph.add_edge(agent_name, "route_agents")
    
    # Add review routing
    graph.add_node("route_review", route_review)
    graph.add_edge("human_review", "route_review")
    graph.add_conditional_edges(
        "route_review",
        lambda x: x["next"],
        {
            "stream_output": "stream_output",
            "error_handler": "error_handler"
        }
    )
    
    # Final edges
    graph.add_edge("stream_output", END)
    graph.add_edge("error_handler", END)
    
    return graph.compile()

# Create compiled graph instance
compiled_graph = build_graph()