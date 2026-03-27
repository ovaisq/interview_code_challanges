# Agent Guidelines for URL Shortener Codebase

## Overview
This codebase contains two implementations of a URL shortener service:
1. Node.js/Express implementation (`app.js`)
2. Python/Flask implementation (`shorten2.py`)

Both implement token-based URL shortening with HMAC signatures for security, status tracking, and expiration.

## Build/Lint/Test Commands

### Node.js Implementation
- No build process required (interpreted JavaScript)
- Linting: No existing lint configuration
- Testing: No existing test suite

### Python Implementation
- No build process required (interpreted Python)
- Linting: No existing lint configuration
- Testing: No existing test suite

### Running Single Tests
Since there are no existing test frameworks configured:
1. Manual testing via curl commands (see README.md)
2. To create a test suite:
   - For Node.js: Consider Jest or Mocha
   - For Python: Consider pytest

## Code Style Guidelines

### Import Conventions
**Node.js (`app.js`):**
- Use CommonJS `require()` syntax
- Group imports: core modules first, then third-party, then local
- Example:
  ```javascript
  const express = require('express');
  const sqlite3 = require('sqlite3').verbose();
  const crypto = require('crypto');
  ```

**Python (`shorten2.py`):**
- Use PEP 8 import ordering:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Example:
  ```python
  import sqlite3
  import base64
  import hmac
  import hashlib
  import time
  import random
  import string
  from flask import Flask, request, jsonify
  ```

### Formatting
**Node.js:**
- 2-space indentation
- Semicolons required
- Opening braces on same line as statement
- Maximum line length: 100 characters
- Constants in UPPER_SNAKE_CASE
- Variables and functions in camelCase

**Python:**
- 4-space indentation (PEP 8)
- No semicolons
- Maximum line length: 79 characters (PEP 8)
- Constants in UPPER_SNAKE_CASE
- Variables and functions in snake_case
- Classes in PascalCase

### Type Guidelines
**Node.js:**
- Use JSDoc comments for complex functions when types aren't obvious
- Example:
  ```javascript
  /**
   * Generate 6-character base64 token
   * @returns {string} 6-character token
   */
  function generateShortToken() {
    // implementation
  }
  ```

**Python:**
- Use type hints for function signatures (Python 3.6+)
- Example:
  ```python
  def generate_short_token() -> str:
      """Generate a 6-character base64 random token."""
      # implementation
      return token
  ```

### Naming Conventions
**Node.js:**
- Files: camelCase or lowercase_with_underscores
- Functions: camelCase
- Variables: camelCase
- Constants: UPPER_SNAKE_CASE
- Classes: PascalCase (though none in this codebase)

**Python:**
- Files: lowercase_with_underscores
- Functions: snake_case
- Variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Classes: PascalCase

### Error Handling
**Node.js:**
- Use try/catch for synchronous code
- For asynchronous callbacks, check error parameter first
- Return appropriate HTTP status codes:
  - 400 for client errors (bad request)
  - 401 for unauthorized
  - 404 for not found
  - 409 for conflicts
  - 410 for expired resources
  - 500 for server errors

**Python:**
- Use try/except blocks for error handling
- Check for specific exception types when possible
- Return appropriate HTTP status codes using Flask's jsonify and status codes
- Follow same HTTP status code conventions as Node.js implementation

### Security Practices
- Store secrets in environment variables (currently hardcoded as empty strings)
- Use HMAC for token signing to prevent tampering
- Validate input format and length
- Use constant-time comparison for cryptographic signatures (`hmac.compare_digest`)
- Set appropriate HTTP status codes for security-related errors

### Database Practices
- Use parameterized queries to prevent SQL injection
- Handle database constraints (like UNIQUE violations) gracefully
- Close database connections properly (especially in Python implementation)
- Use transactions when appropriate

### Comments and Documentation
- Comment complex logic, not obvious code
- Keep comments up-to-date when code changes
- Use docstrings/functions comments to explain purpose
- README.md contains good usage examples - maintain consistency with code

## Cursor/Copilot Rules
No existing Cursor rules (.cursor/rules/ or .cursorrules) or Copilot rules (.github/copilot-instructions.md) found in this repository.

## Best Practices for Agents
1. When modifying either implementation, maintain feature parity where appropriate
2. Follow existing code patterns in the file you're modifying
3. Ensure security practices are maintained (HMAC validation, input validation)
4. Handle edge cases (token collisions, expiration, invalid formats)
5. Keep responses consistent between implementations
6. Update both implementations when making feature changes unless intentionally diverging