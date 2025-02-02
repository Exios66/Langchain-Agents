# core/graph_builder.py
from typing import Dict, Any, List, Annotated, TypedDict, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import BaseTool
import operator
from functools import partial
import logging
from config import settings
from core.langchain_setup import (
    get_llm,
    create_agent_executor,
    create_memory,
    format_chat_history
)

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """Type definition for agent state."""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    data_store: Dict[str, Any]

def create_agent_node(
    name: str,
    tools: List[BaseTool],
    system_prompt: str
) -> Any:
    """Create an agent node for the workflow graph."""
    memory = create_memory()
    agent = create_agent_executor(tools, system_prompt, memory)
    
    def agent_node(state: AgentState) -> AgentState:
        """Agent node function for the graph."""
        messages = state["messages"]
        data_store = state["data_store"]
        
        # Run the agent
        result = agent.invoke({
            "input": messages[-1].content,
            "chat_history": messages[:-1],
            "data_store": data_store
        })
        
        # Update state
        state["messages"].append(result.messages[-1])
        if "data_store" in result:
            state["data_store"].update(result["data_store"])
        
        # Determine next node
        if "next" in result:
            state["next"] = result["next"]
        elif "final_answer" in result:
            state["next"] = END
        
        return state
    
    return agent_node

def create_tool_node(tool: BaseTool) -> Any:
    """Create a tool node for the workflow graph."""
    tool_executor = ToolExecutor(tools=[tool])
    
    def tool_node(state: AgentState) -> AgentState:
        """Tool node function for the graph."""
        messages = state["messages"]
        last_message = messages[-1].content
        
        # Execute tool
        result = tool_executor.invoke({
            "tool_name": tool.name,
            "tool_input": last_message
        })
        
        # Update state
        state["messages"].append(result)
        return state
    
    return tool_node

def build_sequential_graph(
    agents: List[str],
    tools: List[BaseTool]
) -> StateGraph:
    """Build a sequential workflow graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes for each agent
    for i, agent_name in enumerate(agents):
        agent_config = settings.AGENT_CONFIGS[agent_name]
        system_prompt = f"You are {agent_name}. {agent_config.get('description', '')}"
        
        node = create_agent_node(agent_name, tools, system_prompt)
        workflow.add_node(agent_name, node)
        
        # Connect nodes sequentially
        if i > 0:
            workflow.add_edge(agents[i-1], agent_name)
    
    # Add edges from last agent to end
    workflow.add_edge(agents[-1], END)
    
    return workflow.compile()

def build_parallel_graph(
    agents: List[str],
    tools: List[BaseTool]
) -> StateGraph:
    """Build a parallel workflow graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes for each agent
    for agent_name in agents:
        agent_config = settings.AGENT_CONFIGS[agent_name]
        system_prompt = f"You are {agent_name}. {agent_config.get('description', '')}"
        
        node = create_agent_node(agent_name, tools, system_prompt)
        workflow.add_node(agent_name, node)
        
        # Connect each agent directly to end
        workflow.add_edge(agent_name, END)
    
    return workflow.compile()

def build_hybrid_graph(
    agents: List[str],
    tools: List[BaseTool]
) -> StateGraph:
    """Build a hybrid workflow graph with conditional branching."""
    workflow = StateGraph(AgentState)
    
    def router(state: AgentState) -> str:
        """Route to next node based on state."""
        return state.get("next", END)
    
    # Add nodes for each agent
    for agent_name in agents:
        agent_config = settings.AGENT_CONFIGS[agent_name]
        system_prompt = f"You are {agent_name}. {agent_config.get('description', '')}"
        
        node = create_agent_node(agent_name, tools, system_prompt)
        workflow.add_node(agent_name, node)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            agent_name,
            router,
            {agent: agent for agent in agents} | {END: END}
        )
    
    return workflow.compile()

def get_workflow_builder(workflow_type: str):
    """Get the appropriate workflow builder function."""
    builders = {
        "sequential": build_sequential_graph,
        "parallel": build_parallel_graph,
        "hybrid": build_hybrid_graph
    }
    return builders.get(workflow_type)

def create_initial_state(
    input_data: Dict[str, Any],
    agents: List[str],
    workflow_type: str
) -> AgentState:
    """Create initial state for the workflow."""
    return {
        "messages": format_chat_history([{
            "role": "human",
            "content": str(input_data)
        }]),
        "next": agents[0],
        "data_store": {
            "input_data": input_data,
            "agents": agents,
            "workflow_type": workflow_type,
            "status": "running"
        }
    }

# Create tools list
tools: List[BaseTool] = []  # Add your tools here

# Build the graph based on workflow type
def get_compiled_graph(workflow_type: str, agents: List[str]) -> Any:
    """Get compiled workflow graph for specified type and agents."""
    builder = get_workflow_builder(workflow_type)
    if not builder:
        raise ValueError(f"Invalid workflow type: {workflow_type}")
    return builder(agents, tools)

# Compile default graph
compiled_graph = build_sequential_graph(
    settings.AVAILABLE_AGENTS,
    tools
)