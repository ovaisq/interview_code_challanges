# Agent Guidelines for JSON Key Replacer

## Project Overview
This Python script allows you to replace specific keys in a JSON document with new values. It recursively searches through the JSON structure (both dictionaries and lists) to locate all occurrences of the target key, presents them to the user, and allows for an interactive selection of which occurrence to update.

## Build/Lint/Test Commands

### Build Process
No build process required (interpreted Python script).

### Linting
No existing lint configuration. Recommended tools:
```bash
# Install flake8 for linting
pip install flake8

# Run flake8 linting
flake8 replace_json_key_values.py

# Install black for formatting
pip install black

# Run black formatting
black replace_json_key_values.py

# Install pylint for deeper analysis
pip install pylint

# Run pylint
pylint replace_json_key_values.py
```

### Testing
No existing test suite. To run a single test manually:
```bash
# Test with sample data
python replace_json_key_values.py data.json name

# Test with different JSON files
python replace_json_key_values.py 1.json some_key
python replace_json_key_values.py 2.json another_key
python replace_json_key_values.py new_data.json test_value
```

To create automated tests:
1. Create a test file (test_replace_json_key_values.py)
2. Use unittest or pytest framework
3. Test functions: replace_json_key, main, and edge cases
4. Run tests with: python -m unittest test_replace_json_key_values.py

## Code Style Guidelines

### Imports
Follow PEP 8 import ordering:
1. Standard library imports
2. Related third-party imports
3. Local application/library specific imports

Example from code:
```python
import json
import os
import sys
```

### Formatting
- PEP 8 compliant
- Max line length: 79 chars
- 4 spaces per indent
- No trailing whitespace
- Blank lines:
  - 2 between top-level definitions (function/class)
  - 1 between method definitions in class (not applicable here)
  - Sparingly inside functions for logic sections

### Types
- No type hints currently used (Python 2/3 compatible)
- If adding type hints: follow PEP 484, Python 3.6+ syntax
- Document complex types in docstrings when no type hints

### Naming Conventions
- Modules: lowercase_with_underscores (replace_json_key_values.py)
- Functions: lowercase_with_underscores (replace_json_key, main)
- Constants: UPPERCASE_WITH_UNDERSCORES (none in this code)
- Instance variables: lowercase_with_underscores
- Prefer descriptive names over abbreviations

### Error Handling
- Use try/except for specific exceptions
- Avoid bare except clauses
- Handle JSON decode errors specifically
- Provide meaningful error messages to users
- Exit with appropriate status codes (sys.exit(1) for errors)

### Comments and Docstrings
- Module docstring describing purpose and copyright
- Function docstrings with:
  - Brief description
  - Args section with parameter descriptions
  - Returns section with return value description
  - Raises section for exceptions (when applicable)
- Format docstrings as shown in the code:
  ```python
  def function_name(param):
      """Brief description.
      
      More detailed description if needed.
      """
  ```
- Comments explain why, not what
- Keep comments updated when code changes
- Remove commented-out code

## Testing Practices

### Running Tests Manually
Since there's no automated test suite:
1. Test with provided JSON files (data.json, 1.json, 2.json, etc.)
2. Test edge cases:
   - Empty JSON objects/arrays
   - Nested structures
   - Arrays containing objects
   - Keys that don't exist
   - Invalid JSON input
   - Non-JSON replacement values
3. Verify output files are created correctly
4. Check that original files remain unchanged

### Writing Automated Tests
When creating a test suite:
1. Test replace_json_key function with various inputs:
   - Simple key replacement
   - Nested object key replacement
   - Array element key replacement
   - Multiple occurrences of same key
   - Non-existent key handling
2. Test error conditions:
   - Invalid JSON input
   - File not found
   - Invalid replacement value
3. Test main function with mocked sys.argv and input
4. Test interactive selection logic

## Common Operations

### Running the Script
```bash
# Basic usage
python replace_json_key_values.py <filename> <key_to_replace>

# Example with data.json
python replace_json_key_values.py data.json name
```

### Interactive Usage
When running the script:
1. Enter new value when prompted (must be valid JSON)
2. See numbered list of key instances found
3. Select which instance to replace (or 0 to cancel)
4. Modified JSON saved to new_<filename>

### File Operations
- Script reads input file specified as first argument
- Script writes output to new file with "new_" prefix
- Original file remains unchanged
- Output file created in same directory as script

## Best Practices for Agents
1. Maintain existing code style when making changes
2. Keep PEP 8 compliance for formatting
3. Preserve interactive nature of the tool
4. Ensure error handling remains robust
5. Keep docstrings updated with any functional changes
6. Test changes with various JSON structures
7. Validate that output is valid JSON
8. Ensure file handling properly closes resources