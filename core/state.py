# core/state.py
from typing import TypedDict, List, Dict, Any, Optional
from core.database import SessionLocal, WorkflowState
import json

class State(TypedDict):
    """Shared state used in the multi-agent framework."""
    messages: List[str]
    data_store: Dict[str, Any]

def save_state(input_data: Dict[str, Any], state: State, workflow_type: str) -> int:
    """
    Save the current state to the database.
    Returns the state ID.
    """
    try:
        db = SessionLocal()
        db_state = WorkflowState(
            input_data=json.dumps(input_data),
            state_data=json.dumps(state["data_store"]),
            messages=json.dumps(state["messages"]),
            workflow_type=workflow_type,
            status="completed"
        )
        db.add(db_state)
        db.commit()
        db.refresh(db_state)
        return db_state.id
    except Exception as e:
        print(f"Error saving state: {e}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
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
            
        state_dict = state.to_dict()
        return {
            "messages": state_dict["messages"],
            "data_store": state_dict["state_data"],
            "workflow_type": state_dict["workflow_type"],
            "status": state_dict["status"]
        }
    except Exception as e:
        print(f"Error loading state: {e}")
        return None
    finally:
        db.close()

def create_initial_state(input_data: Dict[str, Any], agents: List[str], workflow_type: str) -> State:
    """
    Create an initial state for a new workflow.
    """
    return State(
        messages=[],
        data_store={
            'input_data': input_data,
            'agents': agents,
            'workflow_type': workflow_type,
            'status': 'pending'
        }
    )
