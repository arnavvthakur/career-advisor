import functools
import uuid
import datetime
from flask import (
    Blueprint, request, jsonify, g, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import models

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# --- Token Management ---

def create_token(db, user_id):
    """Creates a new unique token for a user and stores it in the database."""
    token = str(uuid.uuid4())
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(days=current_app.config['TOKEN_TTL_DAYS'])
    
    models.execute_db(
        'INSERT INTO user_tokens (user_id, token, created_at, expires_at) VALUES (?, ?, ?, ?)',
        (user_id, token, now.isoformat(), expires.isoformat())
    )
    return token

def get_user_by_token(token):
    """Fetches a user from the database based on a valid token."""
    if not token:
        return None
    return models.query_db(
        'SELECT u.* FROM users u JOIN user_tokens t ON u.id = t.user_id WHERE t.token = ? AND t.expires_at > ?',
        [token, datetime.datetime.utcnow().isoformat()],
        one=True
    )

# --- Security Decorator ---

def auth_required(view):
    """Decorator to protect API routes, requiring a valid token."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.replace('Bearer ', '', 1)
        
        g.current_user = get_user_by_token(token)

        if g.current_user is None:
            return jsonify({'error': 'Unauthorized: Invalid or missing token'}), 401
            
        return view(**kwargs)
    return wrapped_view

# --- Authentication API Routes ---

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Missing name, email, or password'}), 400

    if models.query_db('SELECT id FROM users WHERE email = ?', [email], one=True):
        return jsonify({'error': f'User with email {email} is already registered.'}), 409

    db = models.get_db()
    pw_hash = generate_password_hash(password)
    now = datetime.datetime.utcnow().isoformat()
    
    user_id = models.execute_db(
        'INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
        (name, email, pw_hash, now)
    )
    
    # --- NEW: Seed the default timeline for the new user ---
    # This ensures every new user gets the important exam dates.
    models.seed_default_timeline_for_user(db, user_id)
    
    token = create_token(db, user_id)
    return jsonify({'message': 'User created successfully.', 'token': token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400

    db = models.get_db()
    user = models.query_db('SELECT * FROM users WHERE email = ?', [email], one=True)

    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(db, user['id'])
    return jsonify({'message': 'Logged in successfully.', 'token': token})

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    if not all([email, new_password]):
        return jsonify({'error': 'Email and new password are required'}), 400

    user = models.query_db('SELECT id FROM users WHERE email = ?', [email], one=True)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    pw_hash = generate_password_hash(new_password)
    models.execute_db('UPDATE users SET password_hash = ? WHERE id = ?', (pw_hash, user['id']))
    
    return jsonify({'message': 'Password has been reset successfully.'})
