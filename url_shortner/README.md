# Secure Token Shortening Service

A lightweight Flask-based service for generating and securely validating short-lived access tokens using HMAC signatures. Useful for one-time access links, session initiation, or short URLs.

## Features

- Generates short, 6-character tokens
- Adds a 3-character HMAC signature for tamper resistance
- Stores token metadata in an in-memory SQLite database
- Tracks status (`never_used`, `in_progress`, `expired`)
- Expiry control via timestamps
- REST API for integration

## Requirements

- Python 3.9+
- Flask

**NodeJS**
- Node 18+

Install dependencies:

**Python**
```bash
pip install Flask
```
**NodeJS**
```bash
npm install express sqlite3 crypto
```

### NodeJS Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant ExpressApp
    participant DB
    participant Crypto

    Note over Client, ExpressApp: Token Generation Flow
    Client->>ExpressApp: POST /generate-token
    ExpressApp->>Crypto: generateShortToken()
    Crypto-->>ExpressApp: base64 token
    ExpressApp->>Crypto: generateTokenWithSignature(token)
    Crypto-->>ExpressApp: token.signature
    ExpressApp->>DB: INSERT INTO shortened_urls
    DB-->>ExpressApp: Insert Result
    ExpressApp-->>Client: Return token.signature

    Note over Client, ExpressApp: Token Usage Flow
    Client->>ExpressApp: GET /use-token/:token
    ExpressApp->>DB: SELECT token, status
    DB-->>ExpressApp: Token data
    ExpressApp->>ExpressApp: Validate status and expiration
    alt Valid token
        ExpressApp->>DB: UPDATE status to 'in_progress'
        ExpressApp-->>Client: Access granted
    else Invalid or expired
        ExpressApp-->>Client: Error response
    end
```

### Python (Flask) Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant FlaskApp
    participant DB
    participant Crypto

    Note over Client, FlaskApp: Token Generation Flow
    Client->>FlaskApp: POST /generate
    FlaskApp->>Crypto: generate_short_token()
    Crypto-->>FlaskApp: token
    FlaskApp->>Crypto: generate_token_with_signature(token)
    Crypto-->>FlaskApp: token.signature
    FlaskApp->>DB: INSERT token, uuid, expiration, status='never_used'
    DB-->>FlaskApp: Insert result
    FlaskApp-->>Client: Return token.signature

    Note over Client, FlaskApp: Token Usage Flow
    Client->>FlaskApp: GET /use-token/:token
    FlaskApp->>DB: SELECT token, status, expiration
    DB-->>FlaskApp: Token record
    FlaskApp->>FlaskApp: Validate status and expiration
    alt Valid token
        FlaskApp->>DB: UPDATE status to 'in_progress'
        FlaskApp-->>Client: Allow access
    else Invalid or expired
        FlaskApp-->>Client: Error response
    end
```
