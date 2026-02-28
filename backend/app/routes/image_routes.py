from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import StyleImage
from app.ai_modules.image_analyzer import ImageAnalyzer
from app.ai_modules.color_analyzer import ColorAnalyzer
from datetime import datetime
import base64
import io

bp = Blueprint('images', __name__, url_prefix='/api/images')

@bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze_image():
    """Analyze uploaded image"""
    user_id = get_jwt_identity()
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    image_type = request.form.get('image_type', 'outfit')  # outfit, inspiration, wardrobe
    
    # Read image bytes
    image_bytes = file.read()
    
    # Analyze image
    image_analyzer = ImageAnalyzer()
    color_analyzer = ColorAnalyzer()
    
    try:
        detected_items = image_analyzer.detect_clothing_items(image_bytes)
        color_analysis = color_analyzer.extract_dominant_colors(image_bytes)
        style_profile = image_analyzer.extract_style_profile(image_bytes)
        
        # Store image analysis in database
        style_image = StyleImage(
            user_id=user_id,
            image_type=image_type,
            detected_items=detected_items.get('detected_items', []),
            color_analysis=color_analysis,
            style_classification=style_profile.get('style_tags', [])
        )
        
        db.session.add(style_image)
        db.session.commit()
        
        return jsonify({
            'message': 'Image analyzed successfully',
            'image_id': style_image.id,
            'analysis': {
                'detected_items': detected_items,
                'color_analysis': color_analysis,
                'style_profile': style_profile
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/upload-style', methods=['POST'])
@jwt_required()
def upload_style_image():
    """Upload style reference image"""
    user_id = get_jwt_identity()
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    # Read image bytes
    image_bytes = file.read()
    
    # Analyze image
    image_analyzer = ImageAnalyzer()
    color_analyzer = ColorAnalyzer()
    
    try:
        color_analysis = color_analyzer.extract_dominant_colors(image_bytes)
        style_profile = image_analyzer.extract_style_profile(image_bytes)
        
        # Store style image reference
        style_image = StyleImage(
            user_id=user_id,
            image_type='style_reference',
            color_analysis=color_analysis,
            style_classification=style_profile.get('style_tags', [])
        )
        
        db.session.add(style_image)
        db.session.commit()
        
        return jsonify({
            'message': 'Style image uploaded successfully',
            'image_id': style_image.id,
            'analysis': {
                'color_analysis': color_analysis,
                'style_profile': style_profile
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/history', methods=['GET'])
@jwt_required()
def get_image_history():
    """Get user's uploaded images"""
    user_id = get_jwt_identity()
    images = StyleImage.query.filter_by(user_id=user_id).order_by(
        StyleImage.uploaded_at.desc()
    ).all()
    
    return jsonify({
        'images': [img.to_dict() for img in images],
        'count': len(images)
    }), 200
