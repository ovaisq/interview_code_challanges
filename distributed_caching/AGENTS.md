# Agent Guidelines for Distributed Caching Service

## Project Overview
Distributed caching service using Redis with Flask endpoint. Implements consistent hashing, client protocol, key expiration, and encryption options.

## Development Setup

### Prerequisites
- Python 3.x
- Redis server (1 master, 3 replicas assumed)
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Running the Service
```bash
python caching_service.py
```
Runs on port 8000 (HTTPS).

### Running Tests
Integration test only:
```bash
python test_app.py
```
Tests full WRITE/READ/DELETE cycle. Cannot run individual functions separately.

## Code Style Guidelines

### Imports
1. Standard library imports
2. Third-party imports  
3. Local application imports
- Use absolute imports for local modules
Example:
```python
import requests
import json
from config import get_config
```

### Formatting
- PEP 8 compliant
- Max line length: 79 chars
- 4 spaces per indent
- No trailing whitespace
- Blank lines:
  - 2 between top-level definitions
  - 1 between method definitions in class
  - Sparingly inside functions for logic sections

### Types
- No type hints currently used
- If adding: follow PEP 484, Python 3.6+ syntax
- Document complex types in docstrings when no type hints

### Naming Conventions
- Modules: lowercase_with_underscores
- Classes: CapWords
- Functions: lowercase_with_underscores
- Constants: UPPERCASE_WITH_UNDERSCORES
- Instance variables: lowercase_with_underscores
- Method names: lowercase_with_underscores
- Prefer descriptive names over abbreviations

### Error Handling
- Use try/except for specific exceptions
- Avoid bare except clauses
- Log errors (currently print statements, consider logging module)
- Raise exceptions with meaningful messages
- Flask endpoints: return appropriate HTTP status codes

### Comments and Docstrings
- Docstrings for all public modules, functions, classes, methods
- Format (from test_app.py):
  ```python
  def function_name(param):
      """Brief description.
      
      More detailed description if needed.
      """
  ```
- Comments explain why, not what
- Keep comments updated when code changes
- Remove commented-out code

### Security Considerations
- Never hardcode secrets or API keys
- Use environment variables or config files for sensitive data
- Validate and sanitize all inputs
- Use HTTPS in production (self-signed certs for development)
- SSL verification disabled in tests (development only)

## Build and Deployment

### Docker
- Build: `python build_docker.py`
- Deploy: `build_n_deploy.sh`
- Dockerfile in root

### Kubernetes
- Deployment: `deployment.yaml`
- Service: `service.yaml`

### Configuration
- Template: `setup.config.template`
- Actual config: `setup.config` (not in repo)
- Format: INI-style

## Testing Practices

### Running Tests
- Integration test: `python test_app.py`
- Requires running service on port 8000
- Uses HTTPS endpoints with self-signed certs
- Flow: Authentication → WRITE → READ → DELETE

### Test Structure
test_app.py shows:
1. Authentication (get JWT token)
2. WRITE operation
3. READ operation
4. DELETE operation
- Sequential test requiring full completion

### Writing New Tests
- Follow test_app.py pattern
- Use proper error handling
- Clean up test data appropriately
- Consider edge cases (missing keys, invalid tokens, etc.)

## Linting and Formatting
No automated tools configured. Recommend:
- Install flake8 for linting
- Install black for formatting
- Consider pre-commit hooks

Example implementations:
```bash
# Linting
flake8 .

# Formatting
black .
```

## Git Practices
- Commit early and often
- Clear, descriptive commit messages
- Reference issues in commit messages
- Keep feature branches short-lived
- PR process:
  1. Create feature branch
  2. Make changes
  3. Push branch
  4. Open pull request
  5. Address review comments
  6. Merge after approval

## Common Operations

### Starting Redis Server
```bash
# Start Redis with replication (1 master, 3 replicas)
redis-server --port 6379 --slaveof 127.0.0.1 6379 &
redis-server --port 6380 --slaveof 127.0.0.1 6379 &
redis-server --port 6381 --slaveof 127.0.0.1 6379 &
redis-server --port 6382 --slaveof 127.0.0.1 6379 &
```

### Generating SSL Certificates
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 3650
```

### Environment Variables
Test script uses:
- SRVC_SHARED_SECRET from config for auth
- Configure in setup.config:
  ```
  [service]
  SRVC_SHARED_SECRET=your_secret_here
  ```

### Debugging
- Check Flask logs when running caching_service.py
- Verify Redis connectivity
- Check SSL certificate validity
- Monitor network connectivity between services