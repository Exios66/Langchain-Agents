# api/endpoints.py
from fastapi import FastAPI, HTTPException, Depends, Header, Request, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator, constr
from typing import List, Dict, Any, Optional
from datetime import datetime
import time
import jwt
import os

from core.state import State, create_initial_state
from core.graph_builder import compiled_graph
from core.database import (
    save_workflow_state,
    get_workflow_state,
    update_workflow_status,
    get_db
)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Workflow API",
    description="API for managing and executing multi-agent workflows",
    version="1.0.0"
)

# Authentication setup
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Rate limiting setup
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS = 100  # requests per window
request_history: Dict[str, List[float]] = {}

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input validation models
class WorkflowInput(BaseModel):
    input_data: Dict[str, Any]
    agents: List[constr(regex='^(professor_athena|dr_milgrim|yaat)$')]
    workflow_type: constr(regex='^(sequential|parallel|hybrid)$')

    @validator('agents')
    def validate_agents(cls, v):
        if not v:
            raise ValueError("At least one agent must be specified")
        return v

class WorkflowResponse(BaseModel):
    state_id: int
    message: str
    status: str

class StateResponse(BaseModel):
    messages: List[str]
    data_store: Dict[str, Any]
    status: str

# Authentication middleware
async def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify API key."""
    if not api_key or api_key != os.getenv("API_KEY", "default_key"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    return api_key

# Rate limiting middleware
async def check_rate_limit(request: Request):
    """Check rate limiting."""
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
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    request_history[client_ip].append(now)
    return True

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url)
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.post("/workflow/start/", response_model=WorkflowResponse)
async def start_workflow(
    workflow_input: WorkflowInput,
    api_key: str = Depends(verify_api_key),
    _: bool = Depends(check_rate_limit)
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
            final_state = initial_state
            final_state["messages"].append(f"Workflow execution failed: {str(e)}")
            final_state["data_store"]["status"] = "failed"
            final_state["data_store"]["error"] = str(e)
        
        # Save state
        state_id = save_workflow_state(
            input_data=workflow_input.input_data,
            state_data=final_state["data_store"],
            messages=final_state["messages"],
            workflow_type=workflow_input.workflow_type,
            status=final_state["data_store"].get("status", "completed")
        )
        
        return WorkflowResponse(
            state_id=state_id,
            message="Workflow started successfully",
            status=final_state["data_store"].get("status", "completed")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing workflow: {str(e)}"
        )

@app.get("/workflow/{state_id}/", response_model=StateResponse)
async def get_workflow_state(
    state_id: int,
    api_key: str = Depends(verify_api_key),
    _: bool = Depends(check_rate_limit)
):
    """Retrieve the state of a workflow."""
    try:
        state = get_workflow_state(state_id)
        if not state:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow state {state_id} not found"
            )
        
        return StateResponse(
            messages=state["messages"],
            data_store=state["state_data"],
            status=state.get("status", "unknown")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving workflow state: {str(e)}"
        )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Check if the API is running."""
    try:
        # Test database connection
        with get_db() as db:
            db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "database": "connected"
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
                "error": str(e)
            }
        )