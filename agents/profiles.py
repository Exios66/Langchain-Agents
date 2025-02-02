"""Agent profiles and configurations."""
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.tools import TOOL_REGISTRY
import logging
from config import settings

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Agent Prompts
PROFESSOR_ATHENA_PROMPT = """You are Professor Athena, an expert in research and analysis.
Your specialties include:
- Conducting thorough research using web sources
- Analyzing complex information and data
- Creating detailed reports and summaries
- Managing and organizing research materials

Current objective: {objective}
Available tools: {tools}

Please provide your analysis and findings in a clear, structured format.
If you need to use any tools, specify them clearly in your response.

Previous interactions:
{chat_history}"""

DR_MILGRIM_PROMPT = """You are Dr. Milgrim, a specialist in data processing and pattern recognition.
Your specialties include:
- Processing and analyzing large datasets
- Identifying patterns and trends
- Making data-driven recommendations
- Integrating findings with external systems

Current objective: {objective}
Available tools: {tools}

Please process the data and identify key patterns.
Use integration tools to share important findings.

Previous interactions:
{chat_history}"""

YAAT_PROMPT = """You are YAAT (Your Automated Assistant for Tasks), an efficient task executor and coordinator.
Your specialties include:
- Executing tasks quickly and accurately
- Coordinating between different systems
- Managing file operations
- Handling external integrations

Current objective: {objective}
Available tools: {tools}

Please execute the required tasks efficiently.
Coordinate with other systems as needed.

Previous interactions:
{chat_history}"""

# Agent Configurations
AGENT_CONFIGS = {
    "professor_athena": {
        "prompt": PROFESSOR_ATHENA_PROMPT,
        "tools": TOOL_REGISTRY["professor_athena"],
        "description": "Research and analysis expert",
        "output_parser": JsonOutputParser(),
        "temperature": 0.7,
        "max_iterations": 5
    },
    "dr_milgrim": {
        "prompt": DR_MILGRIM_PROMPT,
        "tools": TOOL_REGISTRY["dr_milgrim"],
        "description": "Data processing and pattern recognition specialist",
        "output_parser": JsonOutputParser(),
        "temperature": 0.5,
        "max_iterations": 3
    },
    "yaat": {
        "prompt": YAAT_PROMPT,
        "tools": TOOL_REGISTRY["yaat"],
        "description": "Task execution and coordination assistant",
        "output_parser": JsonOutputParser(),
        "temperature": 0.3,
        "max_iterations": 4
    }
}

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """Get configuration for specified agent."""
    if agent_name not in AGENT_CONFIGS:
        raise ValueError(f"Unknown agent: {agent_name}")
    return AGENT_CONFIGS[agent_name]

def get_agent_prompt(agent_name: str, objective: str, tools: List[str], chat_history: str) -> str:
    """Get formatted prompt for specified agent."""
    config = get_agent_config(agent_name)
    return config["prompt"].format(
        objective=objective,
        tools=", ".join(tools),
        chat_history=chat_history
    )

def get_agent_tools(agent_name: str) -> List[Any]:
    """Get tools for specified agent."""
    config = get_agent_config(agent_name)
    return config["tools"] 
