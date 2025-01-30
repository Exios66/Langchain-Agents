# core/state.py
from typing import TypedDict, List, Dict, Optional, Any
from core.database import SessionLocal, WorkflowState
import json

class State(TypedDict):
    """Shared state used in the multi-agent framework."""
    messages: List[str]  # Logs agent communications
    data_store: Dict[str, Any]  # Stores processed data and workflow decisions

def save_state(input_data: str, state: State) -> int:
    """
    Save the current state to the database.
    Returns the state ID.
    """
    try:
        db = SessionLocal()
        db_state = WorkflowState(
            input_data=input_data,
            state_data=json.dumps(state["data_store"]),
            messages=json.dumps(state["messages"])
        )
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
        return db_state.id
    except Exception as e:
        print(f"Error saving state: {e}")
        raise
    finally:
        db.close()

def load_state(state_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a state from the database by its ID.
    Returns None if the state is not found.
    """
    try:
        db = SessionLocal()
        state = db.query(WorkflowState).filter(WorkflowState.id == state_id).first()
        if not state:
            return None
            
        return {
            "messages": json.loads(state.messages),
            "data_store": json.loads(state.state_data)
        }
    except Exception as e:
        print(f"Error loading state: {e}")
        return None
    finally:
        db.close()
