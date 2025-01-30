# Langchain-Agents Framework

A sophisticated multi-agent framework built with LangChain for orchestrating complex AI agent workflows.

## 🌟 Features

- Multi-agent orchestration with LangChain
- Configurable workflow management
- Built-in error handling and recovery
- Human-in-the-loop review capabilities
- Real-time streaming output
- Modular and extensible architecture

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- SerpAPI key (optional, for web search capabilities)

## 🚀 Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Langchain-Agents.git
   cd Langchain-Agents
   ```

2. **Run the installation script**

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Configure environment variables**
   - Copy `.env.template` to `.env`
   - Update the `.env` file with your API keys and preferences:

     ```env
     OPENAI_API_KEY=your-openai-api-key
     SERPAPI_API_KEY=your-serpapi-api-key
     ```

4. **Activate the virtual environment**

   ```bash
   source venv/bin/activate
   ```

5. **Run the framework**

   ```bash
   python run.py
   ```

## 🏗️ Project Structure

```bash
Langchain-Agents/
├── agents/                 # Agent implementations
│   ├── agent_a.py         # Primary agent
│   ├── agent_b.py         # Secondary agent
│   └── subgraph.py        # Subgraph processing
├── core/                  # Core framework components
│   ├── config.py          # Configuration management
│   ├── graph_builder.py   # Workflow graph construction
│   └── state.py          # State management
├── integrations/         # External integrations
│   ├── error_handling.py  # Error management
│   ├── human_review.py    # Human review interface
│   └── streaming.py       # Output streaming
├── .env                  # Environment configuration
├── install.sh           # Installation script
├── requirements.txt     # Python dependencies
├── run.py              # Main execution script
└── setup.py            # Package setup
```

## 📖 Component Details

### Agents

- **agent_a.py**: Primary agent for initial processing
- **agent_b.py**: Secondary agent for advanced processing
- **subgraph.py**: Handles preprocessing and data normalization

### Core Components

- **config.py**: Manages environment variables and configuration
- **graph_builder.py**: Constructs and manages the workflow graph
- **state.py**: Handles state management across the workflow

### Integrations

- **error_handling.py**: Manages error detection and recovery
- **human_review.py**: Facilitates human review of agent decisions
- **streaming.py**: Handles real-time output streaming

## ⚙️ Configuration

The framework can be configured through the `.env` file:

```env
# Agent Configuration
MAX_ITERATIONS=10        # Maximum workflow iterations
TEMPERATURE=0.7         # Model temperature
MODEL_NAME=gpt-4        # OpenAI model selection

# Vector Store Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
EMBEDDING_MODEL=text-embedding-ada-002

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=agent_execution.log
```

## 🔄 Workflow

1. **Initialization**
   - Configuration loading
   - Environment setup
   - Graph construction

2. **Execution Flow**
   - Subgraph preprocessing
   - Agent A processing
   - Agent B processing
   - Human review (if required)
   - Result streaming

3. **Error Handling**
   - Automatic error detection
   - Recovery procedures
   - Logging and monitoring

## 🛠️ Development

To extend the framework:

1. **Adding New Agents**
   - Create new agent file in `agents/`
   - Implement agent logic
   - Register in `graph_builder.py`

2. **Custom Integrations**
   - Add integration file in `integrations/`
   - Implement integration logic
   - Update workflow in `graph_builder.py`

## 📝 Logging

Logs are stored in `logs/agent_execution.log` with configurable levels:

- INFO: Standard operation logs
- DEBUG: Detailed debugging information
- ERROR: Error messages and stack traces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

Common issues and solutions:

1. **Import Errors**

   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Issues**

   ```bash
   source venv/bin/activate
   ```

3. **API Key Errors**
   - Verify `.env` file configuration
   - Check API key validity

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
- [SerpAPI Documentation](https://serpapi.com/docs)

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
