const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const crypto = require('crypto');
const app = express();

// Add this line to parse JSON request bodies
app.use(express.json());

const PORT = 3000;
const SECRET_KEY = ''; // Use environment variables in production
const DB_NAME = ':memory:';

// Initialize database
const db = new sqlite3.Database(DB_NAME);
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS shortened_urls (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      original_uuid TEXT NOT NULL,
      token TEXT NOT NULL UNIQUE,
      expiration INTEGER NOT NULL,
      status TEXT NOT NULL CHECK (status IN ('never_used', 'in_progress', 'expired'))
    )
  `);
});

// Helper: Generate 6-character base64 token
function generateShortToken() {
  const randomBytes = crypto.randomBytes(5); // 5 bytes → ~7 base64 chars
  const base64Token = randomBytes.toString('base64url').replace(/[^a-zA-Z0-9]/g, '');
  return base64Token.slice(0, 6); // Take first 6 characters (e.g., "aB3xR9")
}

// Helper: Generate 3-character HMAC signature
function generateTokenWithSignature(token) {
  const hmac = crypto.createHmac('sha256', SECRET_KEY);
  hmac.update(token);
  const digest = hmac.digest('base64url').replace(/[^a-zA-Z0-9]/g, '');
  const signature = digest.slice(0, 3); // Take first 3 characters (e.g., "s2m")
  return `${token}.${signature}`;
}

// Helper: Base64url encoding
function base64url(buffer) {
  return buffer.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

// Helper: Validate token format and signature
function validateToken(token) {
  const [dataPart, signaturePart] = token.split('.');
  if (!dataPart || !signaturePart || dataPart.length !== 6 || signaturePart.length !== 3) {
    return { valid: false, error: 'Invalid token format' };
  }

  const expectedHmac = crypto.createHmac('sha256', SECRET_KEY);
  expectedHmac.update(dataPart);
  const expectedSignature = base64url(expectedHmac.digest()).slice(0, 3);

  return {
    valid: signaturePart === expectedSignature,
    dataPart,
    signaturePart,
    expectedSignature
  };
}

// Route: Create shortened URL
app.post('/shorten', (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'Missing URL' });

  const uuidPart = url.split('/').pop();
  if (!uuidPart || uuidPart.length !== 32 || !/^[a-fA-F0-9]+$/.test(uuidPart)) {
    return res.status(400).json({ error: 'Invalid UUID format' });
  }

  const shortToken = generateShortToken();
  const signedToken = generateTokenWithSignature(shortToken);
  const expiration = Math.floor(Date.now() / 1000) + 300; // 5 minutes

  db.run(
    'INSERT INTO shortened_urls (original_uuid, token, expiration, status) VALUES (?, ?, ?, ?)',
    [uuidPart, signedToken, expiration, 'never_used'],
    function (err) {
      if (err) {
        if (err.code === 'SQLITE_CONSTRAINT') {
          return res.status(409).json({ error: 'Token already exists' });
        }
        return res.status(500).json({ error: 'Database error' });
      }
      res.json({ shortened_url: `https://foo.url/${signedToken}` });
    }
  );
});

// Route: Access shortened URL
app.get('/shortened/:token', (req, res) => {
  const fullToken = req.params.token;
  const { valid, dataPart, error } = validateToken(fullToken);
  if (!valid) return res.status(401).json({ error: error || 'Invalid signature' });

  db.get('SELECT * FROM shortened_urls WHERE token = ?', [fullToken], (err, row) => {
    if (err) return res.status(500).json({ error: 'Database error' });
    if (!row) return res.status(404).json({ error: 'Token not found' });

    const currentTime = Math.floor(Date.now() / 1000);
    if (currentTime > row.expiration) {
      db.run('UPDATE shortened_urls SET status = "expired" WHERE token = ?', [fullToken]);
      return res.status(410).json({ error: 'URL has expired' });
    }

    if (row.status === 'in_progress') {
      return res.status(409).json({ error: 'URL is already in use' });
    }

    db.run('UPDATE shortened_urls SET status = "in_progress" WHERE token = ?', [fullToken]);
    res.json({ message: 'URL is now in progress', original_url: `https://example.com/${row.original_uuid}` });
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
