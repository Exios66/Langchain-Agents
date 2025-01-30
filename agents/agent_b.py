# agents/agent_b.py
from core.state import State
from core.graph_builder import Command
from typing import Literal

def agent_b(state: State) -> Command[Literal['human_review', 'error_handler']]:
    """Agent B decides whether to pass data for human review or handle an error."""
    decision = state['data_store'].get('decision', 'human_review')
    state['messages'].append(f"Agent B decided to call {decision}.")
    return Command(goto=decision, update=state)