# api/endpoints.py
from fastapi import FastAPI, HTTPException
from core.state import State, save_state, load_state
from core.graph_builder import compiled_graph

app = FastAPI()

@app.post("/workflow/start/")
async def start_workflow(input_data: str):
    """Start a new workflow and return the state ID."""
    initial_state = State(messages=[], data_store={'input_data': input_data})
    final_state = compiled_graph.invoke(initial_state)
    
    state_id = save_state(input_data, final_state)
    return {"message": "Workflow started", "state_id": state_id}

@app.get("/workflow/{state_id}/")
async def get_workflow_state(state_id: int):
    """Retrieve the state of a completed workflow."""
    state = load_state(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return {"state_id": state_id, "messages": state["messages"], "data_store": state["data_store"]}