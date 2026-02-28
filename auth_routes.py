from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import hashlib
from datetime import datetime
import jwt
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Hash password
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user = User(
        email=data['email'],
        username=data['username'],
        password_hash=password_hash,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        style_preferences=data.get('style_preferences', {}),
        body_type=data.get('body_type', ''),
        climate_preference=data.get('climate_preference', ''),
        budget_range=data.get('budget_range', '')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    if user.password_hash != password_hash:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Generate JWT token
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow().timestamp() + 86400},
        os.getenv('JWT_SECRET_KEY', 'dev-secret-key'),
        algorithm='HS256'
    )
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    return jsonify({'message': 'Logout successful'}), 200
