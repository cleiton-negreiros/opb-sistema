"""
OPB Sistema - Input Validation & Error Handling
Production-ready validation decorators and error handlers
"""

from functools import wraps
from flask import request, jsonify
import re

# Validation patterns
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_]{3,30}$')
URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')

def validate_email(email):
    """Validate email format"""
    return bool(EMAIL_REGEX.match(email))

def validate_username(username):
    """Validate username format"""
    return bool(USERNAME_REGEX.match(username))

def validate_url(url):
    """Validate URL format"""
    return bool(URL_REGEX.match(url))

def sanitize_string(s, max_length=1000):
    """Sanitize string input"""
    if not isinstance(s, str):
        return ""
    s = s.strip()
    s = s[:max_length]
    # Remove potential XSS
    s = s.replace('<script', '&lt;script')
    s = s.replace('<iframe', '&lt;iframe')
    s = s.replace('javascript:', '')
    return s

def required_fields(*fields):
    """Decorator to validate required fields in JSON body"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json(silent=True)
            if not data:
                return jsonify({"error": "JSON body required", "code": "INVALID_JSON"}), 400

            missing = [field for field in fields if field not in data or not str(data[field]).strip()]
            if missing:
                return jsonify({
                    "error": f"Campos obrigatórios: {', '.join(missing)}",
                    "code": "MISSING_FIELDS",
                    "missing": missing
                }), 400

            return f(*args, **kwargs)
        return decorated
    return decorator

def validate_field(field_name, validator, error_message):
    """Decorator to validate a specific field"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json(silent=True)
            if data and field_name in data:
                if not validator(data[field_name]):
                    return jsonify({
                        "error": error_message,
                        "code": "INVALID_FIELD",
                        "field": field_name
                    }), 400
            return f(*args, **kwargs)
        return decorated
    return decorator

def max_length(field_name, max_len):
    """Decorator to validate max length of a field"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            data = request.get_json(silent=True)
            if data and field_name in data:
                if len(str(data[field_name])) > max_len:
                    return jsonify({
                        "error": f"Campo '{field_name}' deve ter no máximo {max_len} caracteres",
                        "code": "MAX_LENGTH_EXCEEDED",
                        "field": field_name
                    }), 400
            return f(*args, **kwargs)
        return decorated
    return decorator

def rate_limit(max_requests=60, window=60):
    """Simple rate limiting decorator (in-memory)"""
    from collections import defaultdict
    import time

    requests = defaultdict(list)

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            client_ip = request.remote_addr
            now = time.time()

            # Clean old requests
            requests[client_ip] = [t for t in requests[client_ip] if now - t < window]

            if len(requests[client_ip]) >= max_requests:
                return jsonify({
                    "error": "Muitas requisições. Tente novamente em alguns segundos.",
                    "code": "RATE_LIMITED"
                }), 429

            requests[client_ip].append(now)
            return f(*args, **kwargs)
        return decorated
    return decorator

def handle_errors(f):
    """Decorator to catch and format errors"""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"error": str(e), "code": "VALIDATION_ERROR"}), 400
        except PermissionError as e:
            return jsonify({"error": str(e), "code": "PERMISSION_DENIED"}), 403
        except FileNotFoundError as e:
            return jsonify({"error": str(e), "code": "NOT_FOUND"}), 404
        except Exception as e:
            return jsonify({
                "error": "Erro interno do servidor",
                "code": "INTERNAL_ERROR",
                "detail": str(e) if request.args.get('debug') else None
            }), 500
    return decorated
