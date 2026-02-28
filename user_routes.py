from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, SavedOutfit
from datetime import datetime

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.profile_image = data.get('profile_image', user.profile_image)
    user.style_preferences = data.get('style_preferences', user.style_preferences)
    user.body_type = data.get('body_type', user.body_type)
    user.climate_preference = data.get('climate_preference', user.climate_preference)
    user.budget_range = data.get('budget_range', user.budget_range)
    user.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200

@bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Update style preferences"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    user.style_preferences = data.get('style_preferences', user.style_preferences)
    user.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'message': 'Preferences updated successfully',
        'user': user.to_dict()
    }), 200

@bp.route('/outfits', methods=['GET'])
@jwt_required()
def get_saved_outfits():
    """Get user's saved outfits"""
    user_id = get_jwt_identity()
    outfits = SavedOutfit.query.filter_by(user_id=user_id).order_by(
        SavedOutfit.saved_at.desc()
    ).all()
    
    return jsonify({
        'outfits': [outfit.to_dict() for outfit in outfits],
        'count': len(outfits)
    }), 200

@bp.route('/outfits', methods=['POST'])
@jwt_required()
def save_outfit():
    """Save an outfit"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    outfit = SavedOutfit(
        user_id=user_id,
        outfit_name=data.get('outfit_name'),
        outfit_items=data.get('outfit_items', []),
        outfit_image_url=data.get('outfit_image_url'),
        occasion=data.get('occasion'),
        season=data.get('season'),
        notes=data.get('notes', '')
    )
    
    db.session.add(outfit)
    db.session.commit()
    
    return jsonify({
        'message': 'Outfit saved successfully',
        'outfit': outfit.to_dict()
    }), 201

@bp.route('/outfits/<int:outfit_id>', methods=['DELETE'])
@jwt_required()
def delete_saved_outfit(outfit_id):
    """Delete a saved outfit"""
    user_id = get_jwt_identity()
    outfit = SavedOutfit.query.get(outfit_id)
    
    if not outfit:
        return jsonify({'error': 'Outfit not found'}), 404
    
    if outfit.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(outfit)
    db.session.commit()
    
    return jsonify({'message': 'Outfit deleted successfully'}), 200
