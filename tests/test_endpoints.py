#!/usr/bin/env python3
import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8004"  # Update this if your server is running on a different port

def test_workflow_start(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Test the workflow start endpoint with the given input data."""
    url = f"{BASE_URL}/workflow/start/"
    
    print("\n=== Testing Workflow Start Endpoint ===")
    print(f"POST {url}")
    print("Request Body:")
    print(json.dumps(input_data, indent=2))
    
    try:
        response = requests.post(url, json=input_data)
        response.raise_for_status()
        result = response.json()
        
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError: {str(e)}")
        return {}

def test_workflow_state(state_id: int) -> Dict[str, Any]:
    """Test the workflow state endpoint for the given state ID."""
    url = f"{BASE_URL}/workflow/{state_id}/"
    
    print(f"\n=== Testing Workflow State Endpoint ===")
    print(f"GET {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"\nError: {str(e)}")
        return {}

def run_example_workflows():
    """Run example workflows to demonstrate different use cases."""
    
    # Example 1: Market Analysis Workflow
    print("\n=== Example 1: Market Analysis Workflow ===")
    market_analysis = {
        "input_data": {
            "query": "Analyze market trends for electric vehicles in 2024",
            "parameters": {
                "timeframe": "1y",
                "regions": ["North America", "Europe", "Asia"],
                "segments": ["consumer", "commercial"]
            }
        },
        "agents": ["professor_athena", "dr_milgrim", "yaat"],
        "workflow_type": "sequential"
    }
    result1 = test_workflow_start(market_analysis)
    if "state_id" in result1:
        time.sleep(2)  # Wait for processing
        test_workflow_state(result1["state_id"])

    # Example 2: Real-time Monitoring Workflow
    print("\n=== Example 2: Real-time Monitoring Workflow ===")
    monitoring = {
        "input_data": {
            "query": "Monitor system performance metrics",
            "parameters": {
                "metrics": ["cpu", "memory", "network"],
                "threshold": 0.8,
                "interval": "5m"
            }
        },
        "agents": ["dr_milgrim", "yaat"],
        "workflow_type": "parallel"
    }
    result2 = test_workflow_start(monitoring)
    if "state_id" in result2:
        time.sleep(2)  # Wait for processing
        test_workflow_state(result2["state_id"])

    # Example 3: Research Analysis Workflow
    print("\n=== Example 3: Research Analysis Workflow ===")
    research = {
        "input_data": {
            "query": "Analyze recent research papers on quantum computing",
            "parameters": {
                "timeframe": "6m",
                "topics": ["algorithms", "hardware", "applications"],
                "min_citations": 10
            }
        },
        "agents": ["professor_athena"],
        "workflow_type": "sequential"
    }
    result3 = test_workflow_start(research)
    if "state_id" in result3:
        time.sleep(2)  # Wait for processing
        test_workflow_state(result3["state_id"])

    # Example 4: Hybrid Workflow with Error Handling
    print("\n=== Example 4: Hybrid Workflow with Error Handling ===")
    hybrid = {
        "input_data": {
            "query": "Invalid query to test error handling",
            "parameters": {
                "invalid": True
            }
        },
        "agents": ["professor_athena", "dr_milgrim", "yaat"],
        "workflow_type": "hybrid"
    }
    result4 = test_workflow_start(hybrid)
    if "state_id" in result4:
        time.sleep(2)  # Wait for processing
        test_workflow_state(result4["state_id"])

if __name__ == "__main__":
    run_example_workflows() 