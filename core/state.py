# core/state.py
from typing import TypedDict, List, Dict
from core.database import SessionLocal, WorkflowState
import json

class State(TypedDict):
    """Shared state used in the multi-agent framework."""
    messages: List[str]  # Logs agent communications
    data_store: Dict[str, str]  # Stores processed data and workflow decisions

def save_state(state: State, input_data: str) -> WorkflowState:
    """Save the current state to the database."""
    db_state = WorkflowState(
        input_data=input_data,
        state_data=json.dumps(state["data_store"]),
        messages=json.dumps(state["messages"])
    )
    return db_state
