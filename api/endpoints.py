# api/endpoints.py
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Optional
from core.state import State, save_state, load_state, create_initial_state
from core.graph_builder import compiled_graph
import time
from datetime import datetime
import jwt
import os

app = FastAPI(title="Workflow API",
             description="API for managing multi-agent workflows",
             version="1.0.0")

# Authentication setup
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Rate limiting setup
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS = 100  # requests per window
request_history: Dict[str, List[float]] = {}

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

class EnhancedWorkflowInput(BaseModel):
    input_data: Dict[str, Any]
    agents: List[str]
    workflow_type: str
    
    @validator('workflow_type')
    def validate_workflow_type(cls, v):
        allowed_types = ['sequential', 'parallel', 'hybrid']
        if v not in allowed_types:
            raise ValueError(f'workflow_type must be one of {allowed_types}')
        return v
    
    @validator('agents')
    def validate_agents(cls, v):
        allowed_agents = ['professor_athena', 'dr_milgrim', 'yaat']
        if not all(agent in allowed_agents for agent in v):
            raise ValueError(f'agents must be from the list: {allowed_agents}')
        return v

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != os.getenv("API_KEY", "default_key"):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

async def rate_limit(request: Request):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in request_history:
        request_history[client_ip] = []
    
    # Clean old requests
    request_history[client_ip] = [
        req_time for req_time in request_history[client_ip]
        if now - req_time < RATE_LIMIT_WINDOW
    ]
    
    if len(request_history[client_ip]) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )
    
    request_history[client_ip].append(now)
    return True

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.post("/workflow/start/", response_model=WorkflowResponse)
async def start_workflow(
    workflow_input: EnhancedWorkflowInput,
    api_key: str = Depends(verify_api_key),
    _: bool = Depends(rate_limit)
):
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
async def get_workflow_state(
    state_id: int,
    api_key: str = Depends(verify_api_key),
    _: bool = Depends(rate_limit)
):
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
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }