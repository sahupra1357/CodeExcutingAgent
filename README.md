# CodeExecutingAgent

A modular AI agent system for data analysis that combines file access and Python code execution capabilities using OpenAI's language models.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different tasks (file access, code execution)
- **Tool-based System**: Extensible tool framework for adding new capabilities
- **OpenAI Integration**: Powered by OpenAI's language models (GPT-4, O3-mini)
- **Interactive Data Analysis**: Chat-based interface for analyzing CSV data
- **Docker Support**: Isolated Python code execution environment
- **Comprehensive Logging**: Debug-level logging for development and troubleshooting

## 🏗️ Architecture

### Core Components

- **BaseAgent**: Abstract base class for all agents
- **ToolManager**: Manages and orchestrates tools for agents
- **LanguageModelInterface**: Abstraction layer for different LLM providers

### Agents

1. **FileAccessAgent**: Handles file reading operations with security measures
2. **PythonCodeExecAgent**: Executes Python code in a sandboxed environment

### Tools

1. **FileAccessTool**: Securely reads CSV files and transfers them to Docker containers
2. **PythonCodeInterpreterTool**: Executes Python code in isolated environments

## 📁 Project Structure

```
CodeExcutingAgent/
├── AgentOrchestration.py          # Main orchestration script
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project configuration
├── data/                         # Data files
│   └── traffic_accidents.csv    # Sample dataset
├── docker/                      # Docker configuration
├── object_orinted_agents/       # Core agent framework
│   ├── core/                   # Core classes
│   │   ├── base_agent.py       # Base agent implementation
│   │   ├── tool_manager.py     # Tool management
│   │   ├── tool_interface.py   # Tool interface definition
│   │   └── chat_message.py     # Message handling
│   ├── services/               # External service integrations
│   │   ├── open_ai_language_model.py
│   │   └── language_model_interface.py
│   └── utils/                  # Utility functions
│       └── logger.py           # Logging configuration
└── registry/                   # Agent and tool registry
    ├── agents/                 # Concrete agent implementations
    │   ├── file_access_agent.py
    │   └── python_code_exec_agent.py
    └── tools/                  # Tool implementations
        ├── file_access_tool.py
        └── python_code_interpreter_tool.py
```

## 🛠️ Installation

### Prerequisites

- Python 3.12+
- Docker (for code execution sandbox)
- OpenAI API key

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sahupra1357/CodeExcutingAgent.git
   cd CodeExcutingAgent
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Start Docker container** (if using code execution features):
   ```bash
   docker run -d --name sandbox -it python:3.11-slim
   ```

## 🚀 Usage

### Basic Usage

Run the main orchestration script:

```bash
python AgentOrchestration.py
```

This will:
1. Initialize both FileAccessAgent and PythonCodeExecAgent
2. Load and analyze the traffic_accidents.csv dataset
3. Start an interactive chat session for data analysis

### Example Session

```
Setting up the agents...
Understanding the content of the file...
File Ingest Agent Output: [File contents displayed]

Type your question related to the data in the file. Type 'exit' to quit.
Your question: What is the correlation between traffic density and accidents?
[Agent analyzes and provides insights]

Your question: Create a visualization of accident trends
[Agent generates Python code and executes it]

Your question: exit
Exiting the program.
```

### Custom Agent Usage

```python
from registry.agents.file_access_agent import FileAccessAgent
from registry.agents.python_code_exec_agent import PythonCodeExecAgent

# Initialize agents
file_agent = FileAccessAgent()
code_agent = PythonCodeExecAgent(model_name="gpt-4o", reasoning_effort="high")

# Use file agent
file_content = file_agent.task("Read traffic_accidents.csv")

# Use code agent for analysis
analysis = code_agent.task("Analyze the correlation between variables X and Y")
```

## 🔧 Configuration

### Model Configuration

Supported OpenAI models:
- `gpt-4o`: Standard GPT-4 model
- `o3-mini`: Optimized for reasoning tasks

### Reasoning Effort Levels

For O3 models, you can set reasoning effort:
- `"low"`: Faster responses
- `"medium"`: Balanced performance
- `"high"`: Deep reasoning (slower but more thorough)

### Logging Levels

Configure logging in your script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # For detailed debugging
logging.basicConfig(level=logging.INFO)   # For standard operation
```

## 🧪 Development

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement the `setup_tools()` method
3. Register your agent in the registry

Example:
```python
from object_orinted_agents.core.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def setup_tools(self):
        # Register your tools here
        pass
```

### Adding New Tools

1. Implement the `ToolInterface`
2. Define tool schema in `get_defination()`
3. Implement the `execute()` method

Example:
```python
from object_orinted_agents.core.tool_interface import ToolInterface

class MyCustomTool(ToolInterface):
    def get_defination(self):
        return {
            "function": {
                "name": "my_tool",
                "description": "Tool description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {"type": "string", "description": "Parameter description"}
                    },
                    "required": ["param1"]
                }
            }
        }
    
    def execute(self, arguments):
        # Tool implementation
        return "Tool result"
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Issues**:
   - Ensure your API key is set in the `.env` file
   - Check API key permissions and quotas

2. **Docker Container Issues**:
   - Ensure Docker is running
   - Check container status: `docker ps`
   - Restart container: `docker restart sandbox`

3. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python path configuration

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Review the debug logs for detailed error information

## 🚀 Future Enhancements

- [ ] Support for additional file formats (JSON, Excel, etc.)
- [ ] Integration with more LLM providers
- [ ] Advanced visualization capabilities
- [ ] Web-based interface
- [ ] API endpoints for remote usage
- [ ] Enhanced security features