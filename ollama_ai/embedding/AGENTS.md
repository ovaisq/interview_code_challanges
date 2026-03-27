# AGENTS.md - Coding Guidelines for AI Agents

This document provides guidelines for AI coding agents working in this repository.

## Project Overview

Chat Ollama is a web-based RAG (Retrieval Augmented Generation) application using:
- **Gradio**: Web UI framework
- **LangChain**: LLM orchestration (Ollama integration)
- **PostgreSQL + pgvector**: Vector database for embeddings
- **DuckDuckGo**: Web search integration

## Build/Lint/Test Commands

### Testing
```bash
# Run all tests with pytest (if tests exist)
python -m pytest

# Run a single test file
python -m pytest test_file.py

# Run a single test function
python -m pytest test_file.py::test_function_name

# Run with verbose output
python -m pytest -v
```

### Code Quality
```bash
# Format with black (preferred)
black .

# Lint with flake8
flake8 .

# Type check with mypy
mypy .
```

### Running the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web UI
python ui.py

# Build Docker image
docker build -t ollama-assistant .
```

## Code Style Guidelines

### Python Style
- **Indentation**: 4 spaces (no tabs)
- **Line length**: 88 characters (Black default)
- **Quotes**: Use double quotes for strings, single quotes for dict keys

### Imports
```python
# Standard library imports (group 1)
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# Third-party imports (group 2)
import gradio as gr
import psycopg2
from langchain.schema import Document
from langchain_ollama import ChatOllama

# Local application imports (group 3)
from config import get_config
from websearch import create_dict_list_from_text
```

### Naming Conventions
- **Functions**: `snake_case` (e.g., `process_input`, `get_config`)
- **Variables**: `snake_case` (e.g., `pg_conn_params`, `user_agents`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `EMBED_MODEL`, `CONFIG_FILE`)
- **Classes**: `PascalCase` (e.g., `DocumentLoader`)

### Function Documentation
Use docstrings with triple double quotes:
```python
def function_name(param: str) -> return_type:
    """Brief description of what the function does.
    
    Args:
        param: Description of the parameter
        
    Returns:
        Description of the return value
        
    Raises:
        FileNotFoundError: When file doesn't exist
    """
    pass
```

### Error Handling
```python
try:
    # Risky operation
    result = dangerous_operation()
except Exception as e:
    # Log error with traceback for debugging
    import traceback
    print(f"Error occurred: {e}\n{traceback.format_exc()}")
    return False
```

### Database Operations
```python
# Use context managers for connections
with psycopg2.connect(**PG_CONN_PARAMS) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM table")
        results = cur.fetchall()
```

### Configuration
- Store configuration in `config.py`
- Use `setup.config` for environment-specific settings
- Access config via `CONFIG.get('section', 'key')`

### Type Hints
```python
from typing import List, Dict, Optional

def load_documents(url_list: List[str]) -> List[Document]:
    """Loads documents from a list of URLs."""
    pass
```

### Regex Patterns
```python
# Use raw strings for regex patterns
pattern = r"(\*?\*?Topic-Relevant Keywords:\*?\*?\s*(?:.*\n){3})"
match = re.search(pattern, text, re.DOTALL)
```

## Project Structure

```
ollama_ai/embedding/
├── ui.py              # Main Gradio web interface
├── config.py          # Configuration loader
├── websearch.py       # DuckDuckGo search utilities
├── ra.py             # Random user agent utilities
├── requirements.txt   # Python dependencies
├── setup.config       # Runtime configuration (not in git)
├── setup.config.template  # Template for setup.config
├── Dockerfile         # Container build instructions
├── deployment.yaml    # Kubernetes deployment config
└── service.yaml       # Kubernetes service config
```

## Environment Requirements

### Required Environment Variables
- Database connection details (loaded from setup.config)
- `OLLAMA_HOST`: Ollama server URL
- `USER_AGENT`: Set automatically via `set_random_user_agent()`

### Dependencies
See `requirements.txt` for full list. Key dependencies:
- gradio==5.11.0
- psycopg2-binary
- langchain_ollama
- duckduckgo_search

## Docker Build

```bash
# Build image
docker build -t ollama-assistant:latest .

# Run container
docker run -p 7860:7860 ollama-assistant:latest
```

## Security Notes

- Never commit `setup.config` (contains credentials)
- Use `setup.config.template` as a reference
- Database credentials should be managed via environment variables or secrets
