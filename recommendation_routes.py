from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Recommendation
from app.ai_modules.recommendation_engine import RecommendationEngine
from app.ai_modules.color_analyzer import ColorAnalyzer
from datetime import datetime

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@bp.route('', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Get personalized outfit recommendations"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    occasion = request.args.get('occasion', 'casual')
    season = request.args.get('season', 'all')
    
    # Prepare user profile
    user_profile = {
        'style_preferences': user.style_preferences or [],
        'body_type': user.body_type,
        'climate_preference': user.climate_preference,
        'occasion': occasion,
        'season': season
    }
    
    # Get recommendations from AI engine
    engine = RecommendationEngine()
    outfit_recommendations = engine.get_recommendations(user_profile, num_recommendations=4)
    
    return jsonify({
        'recommendations': outfit_recommendations,
        'count': len(outfit_recommendations),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_recommendations():
    """Generate new AI recommendations"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json() or {}
    
    user_profile = {
        'style_preferences': user.style_preferences or [],
        'body_type': user.body_type,
        'climate_preference': user.climate_preference,
        'occasion': data.get('occasion', 'casual'),
        'season': data.get('season', 'all')
    }
    
    engine = RecommendationEngine()
    ai_recommendations = engine.get_ai_recommendations(user_profile)
    
    return jsonify({
        'recommendations': ai_recommendations,
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@bp.route('/trends', methods=['GET'])
def get_trends():
    """Get current fashion trends"""
    engine = RecommendationEngine()
    trends = engine.get_trend_insights()
    
    return jsonify({
        'trends': trends,
        'timestamp': datetime.utcnow().isoformat()
    }), 200
