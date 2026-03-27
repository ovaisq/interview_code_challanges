# Agent Instructions for interview_code_challanges Repository

## Repository Overview
Multi-project repository containing coding challenges across different tech stacks:
- **pomodoro_timer**: Vanilla HTML/CSS/JS (no build tooling)
- **time_zone_converter**: Python Gradio + HTML/JS with Playwright tests
- **distributed_caching**: Python Flask with Redis and JWT
- **url_shortner**: Node.js Express + SQLite + Python Flask variant
- **code_review_python3_kitties**: Python with pipenv
- **ollama_ai/embedding**: Python (Gradio, LangChain, pgvector)
- **json**: Python JSON manipulation scripts

## Build/Lint/Test Commands

### Python Projects
```bash
# Run app
python3 <script.py>

# Install dependencies
pip install -r requirements.txt
pipenv install && pipenv run python -m <module>  # For pipenv projects

# Testing
python -m pytest                           # Run all tests
python -m pytest test_file.py              # Run single test file
python -m pytest test_file.py::test_func   # Run single test function
python -m pytest -v                        # Verbose output

# Code quality
black .                    # Format (88 char line length)
flake8 .                   # Lint
mypy .                     # Type check
```

### Node.js Projects
```bash
# Install
npm install

# Run tests (Playwright)
npx playwright test                        # All tests
npx playwright test tests/file.spec.js   # Single file
npx playwright test --grep "test name"    # Specific test
npx playwright test --ui                  # UI mode

# Custom test runners
npm test                    # Run twinny-quick-test.js
npm run test:interactive    # Interactive mode
npm run test:full          # Full test suite

# Serve HTML
npm run serve              # python3 -m http.server 8000
```

### HTML/CSS/JS (No Build Tooling)
- Open HTML files directly in browser
- Manual testing via browser DevTools
- Use Chrome DevTools Device Mode for mobile

## Code Style Guidelines

### Python
- **Indentation**: 4 spaces
- **Line length**: 88 chars (Black default)
- **Imports**: Standard lib → Third-party → Local
- **Type hints**: PEP 484, Python 3.6+ syntax
- **Docstrings**: Triple double quotes with Args/Returns/Raises

```python
def function_name(param: str) -> bool:
    """Brief description.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

### JavaScript/Node.js
- **Indentation**: 2 spaces
- **Line length**: 100 chars max
- **Imports**: `require()` for CommonJS (this codebase), `import` for ES6
- **Quotes**: Double quotes preferred
- **Semicolons**: Required
- **Modules**: Uses CommonJS (module.exports)

### HTML/CSS
- **Indentation**: 4 spaces
- **Naming**: IDs camelCase, classes kebab-case
- **Responsive**: Mobile-first with @media breakpoints
- **CSS**: Use CSS custom properties for theming

## Naming Conventions

| Language | Functions | Variables | Constants | Classes | Files |
|----------|-----------|-----------|-----------|---------|-------|
| Python | snake_case | snake_case | UPPER_SNAKE | PascalCase | lowercase.py |
| JavaScript | camelCase | camelCase | UPPER_SNAKE | PascalCase | camelCase.js |
| HTML/CSS | camelCase IDs | - | - | - | kebab-case.html |

## Error Handling

### Python
```python
try:
    result = risky_operation()
except SpecificException as e:
    import traceback
    print(f"Error: {e}\n{traceback.format_exc()}")
    return False
```

### JavaScript/Node.js
```javascript
try {
    const result = riskyOperation();
} catch (error) {
    console.error('Error:', error);
    return res.status(500).json({ error: error.message });
}
```

## Project-Specific Commands

### time_zone_converter
```bash
# Python app (port 7860)
python3 time_zone_converter.py

# HTML app (serve on port 8000)
npm run serve
npx playwright test        # Requires running server
```

### distributed_caching
```bash
python caching_service.py    # Runs on port 8000 (HTTPS)
python test_app.py           # Integration test
```

### url_shortner
```bash
# Node.js version
node app.js                  # Runs on port 3000

# Python version
python3 shorten2.py
```

### code_review_python3_kitties
```bash
make setup-env               # pipenv setup
make run                     # Run with flags
make test tests=tests.test_specific
make clean                   # Remove .pyc files
```

### ollama_ai/embedding
```bash
python ui.py                 # Run Gradio UI
python -m pytest             # Run tests
black . && flake8 .        # Format and lint
docker build -t ollama-assistant .
```

## Testing Best Practices

1. **Run tests after changes** using appropriate test runner
2. **Run single tests** when debugging specific functionality
3. **Check console errors** for HTML/JS projects
4. **Verify mobile responsiveness** for web projects
5. **Use browser DevTools** for HTML/JS debugging
6. **Test requires running server** for Playwright tests

## Security Guidelines

- Never hardcode secrets (use environment variables)
- Use HTTPS in production
- Validate and sanitize all inputs
- Use parameterized queries for SQL
- Use HMAC/constant-time comparison for crypto
- Store credentials in setup.config (not in git)

## Git Practices

- Commit early with clear messages
- Keep feature branches short-lived
- Test before submitting PRs
- No breaking changes without approval
- Reference issues in commit messages
