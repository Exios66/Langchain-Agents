"""Test authentication and endpoint validation."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import json
from datetime import datetime
from config import settings

from api.endpoints import app

client = TestClient(app)

# Test data
VALID_API_KEY = settings.API_KEY
INVALID_API_KEY = "invalid_key"
VALID_WORKFLOW_INPUT = {
    "input_data": {
        "query": "test query",
        "parameters": {"param1": "value1"}
    },
    "agents": settings.AVAILABLE_AGENTS[:2],  # Use first two agents
    "workflow_type": settings.WORKFLOW_TYPES[0]  # Use first workflow type
}
INVALID_WORKFLOW_INPUT = {
    "input_data": {},
    "agents": ["invalid_agent"],
    "workflow_type": "invalid_type"
}

@pytest.fixture(autouse=True)
def setup_environment():
    """Setup test environment variables."""
    with patch.dict(os.environ, {"API_KEY": VALID_API_KEY}):
        yield

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == settings.API_VERSION

def test_missing_api_key():
    """Test request without API key."""
    response = client.post("/workflow/start/", json=VALID_WORKFLOW_INPUT)
    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]

def test_invalid_api_key():
    """Test request with invalid API key."""
    headers = {"X-API-Key": INVALID_API_KEY}
    response = client.post("/workflow/start/", headers=headers, json=VALID_WORKFLOW_INPUT)
    assert response.status_code == 403
    assert "Invalid API key" in response.json()["detail"]

def test_valid_api_key():
    """Test request with valid API key."""
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/workflow/start/", headers=headers, json=VALID_WORKFLOW_INPUT)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "state_id" in data
    assert data["message"] == "Workflow started successfully"

def test_invalid_workflow_input():
    """Test request with invalid workflow input."""
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.post("/workflow/start/", headers=headers, json=INVALID_WORKFLOW_INPUT)
    assert response.status_code == 422  # Validation error
    errors = response.json()["detail"]
    assert any("agents" in e["msg"].lower() for e in errors)
    assert any("workflow_type" in e["msg"].lower() for e in errors)

def test_rate_limiting():
    """Test rate limiting."""
    headers = {"X-API-Key": VALID_API_KEY}
    # Make more requests than allowed
    for _ in range(settings.MAX_REQUESTS + 5):
        response = client.post("/workflow/start/", headers=headers, json=VALID_WORKFLOW_INPUT)
        if response.status_code == 429:
            assert "Rate limit exceeded" in response.json()["detail"]
            break
    else:
        pytest.fail("Rate limiting did not trigger")

def test_workflow_state_retrieval():
    """Test workflow state retrieval."""
    # First create a workflow
    headers = {"X-API-Key": VALID_API_KEY}
    create_response = client.post("/workflow/start/", headers=headers, json=VALID_WORKFLOW_INPUT)
    assert create_response.status_code in [200, 201]
    state_id = create_response.json()["state_id"]
    
    # Then retrieve its state
    get_response = client.get(f"/workflow/{state_id}/", headers=headers)
    assert get_response.status_code == 200
    state_data = get_response.json()
    assert "messages" in state_data
    assert "data_store" in state_data
    assert "status" in state_data

def test_nonexistent_workflow_state():
    """Test retrieval of non-existent workflow state."""
    headers = {"X-API-Key": VALID_API_KEY}
    response = client.get("/workflow/99999/", headers=headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_concurrent_requests():
    """Test handling of concurrent requests."""
    import concurrent.futures
    
    headers = {"X-API-Key": VALID_API_KEY}
    num_requests = min(10, settings.MAX_CONCURRENT_WORKFLOWS)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [
            executor.submit(
                client.post,
                "/workflow/start/",
                headers=headers,
                json=VALID_WORKFLOW_INPUT
            )
            for _ in range(num_requests)
        ]
        
        responses = [f.result() for f in futures]
        
        # Check that all requests were handled
        success_count = sum(1 for r in responses if r.status_code in [200, 201])
        assert success_count > 0, "No concurrent requests succeeded"
        
        # Check that no duplicate state IDs were issued
        state_ids = [r.json()["state_id"] for r in responses if r.status_code in [200, 201]]
        assert len(set(state_ids)) == len(state_ids), "Duplicate state IDs detected"

def test_error_handling():
    """Test error handling in workflows."""
    headers = {"X-API-Key": VALID_API_KEY}
    error_input = {
        **VALID_WORKFLOW_INPUT,
        "input_data": {"query": "trigger_error"}  # Special query to trigger error
    }
    
    response = client.post("/workflow/start/", headers=headers, json=error_input)
    assert response.status_code in [200, 201]  # Should still return success
    data = response.json()
    
    # Get the workflow state
    state_response = client.get(f"/workflow/{data['state_id']}/", headers=headers)
    assert state_response.status_code == 200
    state_data = state_response.json()
    
    # Check error handling
    assert state_data["status"] in ["failed", "error"]
    assert any("error" in msg.lower() for msg in state_data["messages"])

def test_workflow_validation():
    """Test workflow input validation."""
    headers = {"X-API-Key": VALID_API_KEY}
    test_cases = [
        # Empty input data
        {
            "input": {"input_data": {}, "agents": [settings.AVAILABLE_AGENTS[0]], "workflow_type": settings.WORKFLOW_TYPES[0]},
            "should_fail": True
        },
        # Invalid agent name
        {
            "input": {**VALID_WORKFLOW_INPUT, "agents": ["invalid_agent"]},
            "should_fail": True
        },
        # Invalid workflow type
        {
            "input": {**VALID_WORKFLOW_INPUT, "workflow_type": "invalid"},
            "should_fail": True
        },
        # Empty agents list
        {
            "input": {**VALID_WORKFLOW_INPUT, "agents": []},
            "should_fail": True
        },
        # Valid minimal input
        {
            "input": {
                "input_data": {"query": "test"},
                "agents": [settings.AVAILABLE_AGENTS[0]],
                "workflow_type": settings.WORKFLOW_TYPES[0]
            },
            "should_fail": False
        }
    ]
    
    for case in test_cases:
        response = client.post("/workflow/start/", headers=headers, json=case["input"])
        if case["should_fail"]:
            assert response.status_code == 422, f"Expected validation failure for input: {case['input']}"
        else:
            assert response.status_code in [200, 201], f"Expected success for input: {case['input']}" 