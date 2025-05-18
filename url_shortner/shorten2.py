#!/usr/bin/env python3
"""URL shortner with state management
"""

import sqlite3
import base64
import hmac
import hashlib
import time
import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = b''  # Use environment variables in production

def get_db_connection():
	"""DB Connection"""

    conn = sqlite3.connect('file::memory:?cache=shared', uri=True)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database schema
with app.app_context():
    db = get_db_connection()
    db.execute('''CREATE TABLE IF NOT EXISTS shortened_urls
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   original_uuid TEXT NOT NULL,
                   token TEXT NOT NULL UNIQUE,
                   expiration INTEGER NOT NULL,
                   status TEXT NOT NULL CHECK(status IN ('never_used', 'in_progress', 'expired')))''')
    db.commit()

def generate_short_token():
    """Generate a 6-character base64 random token."""

    random_bytes = random.randbytes(5)  # 5 bytes → ~7 base64 characters
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8').rstrip('=')
    return token[:6]  # Take first 6 characters (e.g., "aB3xR9")

def generate_token_with_signature(token):
    """Generate a 3-character HMAC signature for the token."""

    data = token.encode('utf-8')
    signature = hmac.new(SECRET_KEY, data, hashlib.sha256).digest()[:2]  # 2 bytes → 3 base64 characters
    return f"{token}.{base64.urlsafe_b64encode(signature).decode('utf-8')[:-1]}"  # e.g., "aB3xR9.s2m"

@app.route('/shorten', methods=['POST'])
def shorten_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    # Extract UUID from URL
    uuid_part = url.split('/')[-1]

    # Validate UUID format (32 hex characters)
    if len(uuid_part) != 32 or not all(c in '0123456789abcdef' for c in uuid_part):
        return jsonify({'error': 'Invalid UUID format'}), 400

    # Generate short token and signed version
    short_token = generate_short_token()
    signed_token = generate_token_with_signature(short_token)

    # Store in database
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO shortened_urls (original_uuid, token, expiration, status) VALUES (?, ?, ?, ?)',
                     (uuid_part, signed_token, int(time.time()) + 300, 'never_used'))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Token already exists'}), 500
    finally:
        conn.close()

    return jsonify({'shortened_url': f'https://foo.url/{signed_token}'})

@app.route('/shortened/<token>', methods=['GET'])
def use_shortened_url(token):
    try:
        data_part, signature_part = token.split('.', 1)
    except ValueError:
        return jsonify({'error': 'Invalid token format'}), 400

    # Verify signature
    expected_signature = hmac.new(SECRET_KEY, data_part.encode('utf-8'), hashlib.sha256).digest()[:2]
    actual_signature = base64.urlsafe_b64decode(signature_part + '==')[:2]

    if not hmac.compare_digest(expected_signature, actual_signature):
        return jsonify({'error': 'Invalid signature'}), 401

    # Check token in database
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM shortened_urls WHERE token = ?', (token,)).fetchone()
    conn.close()

    if not row:
        return jsonify({'error': 'Token not found'}), 404

    current_time = time.time()
    if current_time > row['expiration']:
        conn = get_db_connection()
        conn.execute('UPDATE shortened_urls SET status = "expired" WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        return jsonify({'error': 'URL has expired'}), 410

    if row['status'] == 'in_progress':
        return jsonify({'error': 'URL is already in use'}), 409

    # Update status to in_progress
    conn = get_db_connection()
    conn.execute('UPDATE shortened_urls SET status = "in_progress" WHERE token = ?', (token,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'URL is now in progress'}), 200

if __name__ == '__main__':
    app.run(debug=True)
