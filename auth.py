"""
OPB Sistema - Authentication Module
SQLite-based user management with JWT-like tokens
Production-ready, secure, multi-tenant ready
"""

import sqlite3
import hashlib
import secrets
import os
import json
import time
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g

# Configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'opb_users.db')
TOKEN_EXPIRY_HOURS = 24
SALT_ROUNDS = 16

def get_db():
    """Get database connection for current request"""
    if 'db' not in g:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database tables"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL COLLATE NOCASE,
            username TEXT UNIQUE NOT NULL COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT,
            plan TEXT DEFAULT 'free',
            is_active INTEGER DEFAULT 1,
            onboarding_complete INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS user_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            theme TEXT DEFAULT 'dark',
            language TEXT DEFAULT 'pt-BR',
            notifications_enabled INTEGER DEFAULT 1,
            telegram_connected INTEGER DEFAULT 0,
            telegram_chat_id TEXT,
            api_url TEXT DEFAULT 'http://localhost:5000',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS usage_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            agent_name TEXT,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON usage_analytics(user_id);
        CREATE INDEX IF NOT EXISTS idx_analytics_created_at ON usage_analytics(created_at);
    """)
    conn.commit()
    conn.close()

def hash_password(password, salt=None):
    """Hash password with salt using SHA-256"""
    if salt is None:
        salt = secrets.token_hex(SALT_ROUNDS)
    password_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return password_hash, salt

def verify_password(password, salt, password_hash):
    """Verify password against stored hash"""
    computed_hash, _ = hash_password(password, salt)
    return computed_hash == password_hash

def generate_token():
    """Generate secure session token"""
    return secrets.token_urlsafe(48)

def create_user(email, username, password, full_name=None, plan='free'):
    """Create new user account"""
    db = get_db()
    try:
        password_hash, salt = hash_password(password)
        cursor = db.execute(
            "INSERT INTO users (email, username, password_hash, salt, full_name, plan) VALUES (?, ?, ?, ?, ?, ?)",
            (email.lower(), username.lower(), password_hash, salt, full_name, plan)
        )
        db.commit()
        user_id = cursor.lastrowid

        # Create default settings
        db.execute(
            "INSERT INTO user_settings (user_id) VALUES (?)",
            (user_id,)
        )
        db.commit()

        return {"success": True, "user_id": user_id, "message": "User created successfully"}
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            return {"success": False, "message": "Email já está em uso"}
        elif "username" in str(e):
            return {"success": False, "message": "Nome de usuário já está em uso"}
        return {"success": False, "message": "Erro ao criar usuário"}

def authenticate_user(email_or_username, password):
    """Authenticate user and create session"""
    db = get_db()

    # Find user by email or username
    cursor = db.execute(
        "SELECT * FROM users WHERE email = ? OR username = ?",
        (email_or_username.lower(), email_or_username.lower())
    )
    user = cursor.fetchone()

    if not user:
        return {"success": False, "message": "Usuário não encontrado"}

    if not user['is_active']:
        return {"success": False, "message": "Conta desativada. Contate o suporte"}

    if not verify_password(password, user['salt'], user['password_hash']):
        return {"success": False, "message": "Senha incorreta"}

    # Update last login
    db.execute(
        "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
        (user['id'],)
    )
    db.commit()

    # Create session
    token = generate_token()
    expires_at = datetime.now() + timedelta(hours=TOKEN_EXPIRY_HOURS)

    db.execute(
        "INSERT INTO sessions (user_id, token, expires_at, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)",
        (user['id'], token, expires_at, request.remote_addr, request.headers.get('User-Agent', ''))
    )
    db.commit()

    # Track analytics
    db.execute(
        "INSERT INTO usage_analytics (user_id, action) VALUES (?, ?)",
        (user['id'], 'login')
    )
    db.commit()

    return {
        "success": True,
        "message": "Login realizado com sucesso",
        "token": token,
        "user": {
            "id": user['id'],
            "email": user['email'],
            "username": user['username'],
            "full_name": user['full_name'],
            "plan": user['plan'],
            "onboarding_complete": bool(user['onboarding_complete']),
            "created_at": user['created_at']
        }
    }

def validate_token(token):
    """Validate session token and return user data"""
    db = get_db()

    cursor = db.execute(
        """SELECT u.*, s.expires_at
           FROM sessions s
           JOIN users u ON s.user_id = u.id
           WHERE s.token = ? AND s.expires_at > CURRENT_TIMESTAMP AND u.is_active = 1""",
        (token,)
    )
    result = cursor.fetchone()

    if not result:
        return {"success": False, "message": "Token inválido ou expirado"}

    return {
        "success": True,
        "user": {
            "id": result['id'],
            "email": result['email'],
            "username": result['username'],
            "full_name": result['full_name'],
            "plan": result['plan'],
            "onboarding_complete": bool(result['onboarding_complete']),
            "created_at": result['created_at']
        }
    }

def logout_user(token):
    """Invalidate session token"""
    db = get_db()
    db.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()
    return {"success": True, "message": "Logout realizado com sucesso"}

def get_user_settings(user_id):
    """Get user settings"""
    db = get_db()
    cursor = db.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
    settings = cursor.fetchone()

    if not settings:
        # Create default settings
        db.execute("INSERT INTO user_settings (user_id) VALUES (?)", (user_id,))
        db.commit()
        cursor = db.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
        settings = cursor.fetchone()

    return dict(settings)

def update_user_settings(user_id, settings):
    """Update user settings"""
    db = get_db()
    allowed_fields = ['theme', 'language', 'notifications_enabled', 'telegram_connected', 'telegram_chat_id', 'api_url']

    for field in allowed_fields:
        if field in settings:
            db.execute(
                f"UPDATE user_settings SET {field} = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (settings[field], user_id)
            )

    db.commit()
    return {"success": True, "message": "Settings updated"}

def complete_onboarding(user_id):
    """Mark onboarding as complete"""
    db = get_db()
    db.execute(
        "UPDATE users SET onboarding_complete = 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (user_id,)
    )
    db.commit()
    return {"success": True, "message": "Onboarding complete"}

def track_usage(user_id, action, agent_name=None, details=None):
    """Track user action for analytics"""
    db = get_db()
    db.execute(
        "INSERT INTO usage_analytics (user_id, action, agent_name, details) VALUES (?, ?, ?, ?)",
        (user_id, action, agent_name, json.dumps(details) if details else None)
    )
    db.commit()

def get_usage_stats(user_id, days=30):
    """Get usage statistics for user"""
    db = get_db()
    cursor = db.execute(
        """SELECT action, agent_name, COUNT(*) as count
           FROM usage_analytics
           WHERE user_id = ? AND created_at >= datetime('now', '-' || ? || ' days')
           GROUP BY action, agent_name
           ORDER BY count DESC""",
        (user_id, days)
    )
    return [dict(row) for row in cursor.fetchall()]

def get_user_data_dir(user_id):
    """Get user-specific data directory path"""
    base_dir = os.path.join(os.path.dirname(__file__), 'data', 'users', str(user_id))
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_user_acervo_dir(user_id):
    """Get user-specific acervo directory"""
    acervo_dir = os.path.join(get_user_data_dir(user_id), 'acervo')
    for subdir in ['ideias', 'transcricoes', 'carrossel', 'conhecimento', 'capas']:
        os.makedirs(os.path.join(acervo_dir, subdir), exist_ok=True)
    return acervo_dir

def get_user_cerebro_dir(user_id):
    """Get user-specific cerebro directory"""
    cerebro_dir = os.path.join(get_user_data_dir(user_id), 'cerebro')
    os.makedirs(cerebro_dir, exist_ok=True)
    return cerebro_dir

def get_user_output_dir(user_id):
    """Get user-specific output directory"""
    output_dir = os.path.join(get_user_data_dir(user_id), 'output', 'text_posts')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
            else:
                token = auth_header

        # Check cookie
        if not token:
            token = request.cookies.get('opb_token')

        # Check query parameter (for PWA)
        if not token:
            token = request.args.get('token')

        if not token:
            return jsonify({"error": "Authentication required", "code": "AUTH_REQUIRED"}), 401

        result = validate_token(token)
        if not result['success']:
            return jsonify({"error": result['message'], "code": "INVALID_TOKEN"}), 401

        request.user = result['user']
        request.token = token
        return f(*args, **kwargs)
    return decorated

def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            token = request.cookies.get('opb_token')
        if not token:
            token = request.args.get('token')

        if token:
            result = validate_token(token)
            if result['success']:
                request.user = result['user']
                request.token = token

        return f(*args, **kwargs)
    return decorated
