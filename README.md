# Multi-Agent Workflow Framework

A powerful framework for managing and executing workflows across multiple AI agents.

## Features

- Multiple agent support (Professor Athena, Dr. Milgrim, YAAT)
- Sequential, parallel, and hybrid workflow execution
- Real-time status updates and monitoring
- Secure API authentication
- Rate limiting and request validation
- Beautiful web interface
- Configurable logging and monitoring

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/multi-agent-workflow.git
cd multi-agent-workflow
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.template .env
```

Edit the `.env` file with your configuration settings.

## Configuration

The framework uses a hierarchical configuration system:

1. Environment Variables (highest priority)
2. `.env` file
3. Default values in `config.py`

### Required Configuration

- `API_KEY`: Your secure API key for authentication
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Optional Configuration

- `CORS_ORIGINS`: Allowed CORS origins (default: *)
- `ALLOWED_HOSTS`: Allowed hosts (default: *)
- `MAX_CONCURRENT_WORKFLOWS`: Maximum concurrent workflows
- `MAX_WORKFLOW_TIME`: Maximum workflow execution time

## Authentication

The API uses API key authentication. Include your API key in requests:

```bash
curl -H "X-API-Key: your_api_key" http://localhost:8003/workflow/start/
```

Or use the web interface and enter your API key in the authentication form.

## Rate Limiting

- 100 requests per minute per client
- Rate limit status available in response headers
- Web interface shows rate limit warnings

## API Endpoints

See [API_ENDPOINTS.md](docs/API_ENDPOINTS.md) for detailed API documentation.

## Web Interface

Access the web interface at `http://localhost:8003`:

1. Enter your API key in the authentication form
2. Create and monitor workflows
3. View real-time status updates
4. Access workflow history and results

## Development

1. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

2. Run tests:

```bash
pytest tests/
```

3. Start the development server:

```bash
python run.py
```

## Security Best Practices

1. Never commit `.env` files
2. Use strong, unique API keys
3. Regularly rotate API keys
4. Monitor API usage and rate limits
5. Keep dependencies updated

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```bash
multi_agent_framework/
│── agents/
│   ├── agent_a.py
│   ├── agent_b.py
│   ├── subgraph.py
│── core/
│   ├── state.py
│   ├── workflow.py
│   ├── graph_builder.py
│── integrations/
│   ├── human_review.py
│   ├── streaming.py
│   ├── error_handling.py
│── run.py
│── requirements.txt
│── README.md
```
