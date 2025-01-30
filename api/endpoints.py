# api/endpoints.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from core.state import State, save_state, load_state, create_initial_state
from core.graph_builder import compiled_graph

app = FastAPI(title="Workflow API",
             description="API for managing multi-agent workflows",
             version="1.0.0")

class WorkflowInput(BaseModel):
    input_data: Dict[str, Any]
    agents: List[str]
    workflow_type: str

class WorkflowResponse(BaseModel):
    state_id: int
    message: str
    status: str

class StateResponse(BaseModel):
    messages: List[str]
    data_store: Dict[str, Any]
    status: str

@app.post("/workflow/start/", response_model=WorkflowResponse)
async def start_workflow(workflow_input: WorkflowInput):
    """Start a new workflow and return the state ID."""
    try:
        # Create initial state
        initial_state = create_initial_state(
            input_data=workflow_input.input_data,
            agents=workflow_input.agents,
            workflow_type=workflow_input.workflow_type
        )
        
        # Execute workflow
        try:
            final_state = compiled_graph.invoke(initial_state)
        except Exception as e:
            print(f"Error executing workflow: {e}")
            final_state = initial_state
            final_state["messages"].append(f"Workflow execution failed: {str(e)}")
            final_state["data_store"]["status"] = "failed"
        
        # Save state
        state_id = save_state(
            input_data=workflow_input.input_data,
            state=final_state,
            workflow_type=workflow_input.workflow_type
        )
        
        return WorkflowResponse(
            state_id=state_id,
            message="Workflow started successfully",
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing workflow: {str(e)}"
        )

@app.get("/workflow/{state_id}/", response_model=StateResponse)
async def get_workflow_state(state_id: int):
    """Retrieve the state of a workflow."""
    try:
        state = load_state(state_id)
        if not state:
            raise HTTPException(
                status_code=404,
                detail=f"Workflow state {state_id} not found"
            )
        
        return StateResponse(
            messages=state["messages"],
            data_store=state["data_store"],
            status=state.get("status", "unknown")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving workflow state: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running."""
    return {"status": "healthy"}