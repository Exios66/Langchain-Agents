# API Endpoints Documentation

This document provides detailed information about the available API endpoints, their usage, and example requests/responses.

## Base URL

```
http://localhost:8001
```

## Endpoints

### 1. Start Workflow

- **URL:** `/workflow/start/`
- **Method:** `POST`
- **Description:** Initiates a new workflow with specified input data and configuration.

#### Request Body Schema

```json
{
    "input_data": {
        "query": string,
        "parameters": object
    },
    "agents": string[],
    "workflow_type": "sequential" | "parallel" | "hybrid"
}
```

#### Example Requests

##### 1. Market Analysis Workflow

```json
{
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
```

##### 2. Real-time Monitoring

```json
{
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
```

#### Success Response

```json
{
    "state_id": integer,
    "message": "Workflow started successfully",
    "status": "success"
}
```

#### Error Response

```json
{
    "detail": "Error message",
    "status": "error"
}
```

### 2. Get Workflow State

- **URL:** `/workflow/{state_id}/`
- **Method:** `GET`
- **Description:** Retrieves the current state of a workflow by its ID.

#### URL Parameters

- `state_id` (integer, required): The unique identifier of the workflow state

#### Success Response

```json
{
    "messages": string[],
    "data_store": {
        "input_data": object,
        "agent_results": object,
        "workflow_status": string
    },
    "status": "success"
}
```

#### Error Response

```json
{
    "detail": "State not found",
    "status": "error"
}
```

## Use Cases

### 1. Market Analysis

Use this workflow to analyze market trends and generate insights:

- Sequential processing through multiple agents
- Comprehensive analysis from different perspectives
- Structured output with market insights

### 2. Real-time Monitoring

Monitor system metrics and get alerts:

- Parallel processing for real-time data
- Multiple agents working simultaneously
- Quick response time for critical metrics

### 3. Research Analysis

Analyze research papers and academic content:

- Single agent specialized processing
- Focus on academic content
- Detailed analysis with citations

### 4. Error Handling

Test system robustness:

- Invalid input handling
- Error reporting
- System recovery

## Testing

1. Start the server:

```bash
python run.py
```

2. Run the test script:

```bash
python tests/test_endpoints.py
```

The test script will run through all example workflows and display the results.

## Notes

- Ensure all required environment variables are set
- The server must be running before executing tests
- Response times may vary based on workflow complexity
- Some workflows may trigger webhooks if configured
