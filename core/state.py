# core/state.py
from typing import TypedDict, List, Dict

class State(TypedDict):
    """Shared state used in the multi-agent framework."""
    messages: List[str]  # Logs agent communications
    data_store: Dict[str, str]  # Stores processed data and workflow decisions