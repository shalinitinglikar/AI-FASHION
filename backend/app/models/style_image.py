from app import db
from datetime import datetime

class StyleImage(db.Model):
    __tablename__ = 'style_images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Image details
    image_url = db.Column(db.String(255), nullable=False)
    image_type = db.Column(db.String(50))  # "outfit", "inspiration", "current_wardrobe"
    analysis_result = db.Column(db.JSON)  # Color palette, style analysis, items detected
    
    # AI Analysis
    detected_items = db.Column(db.JSON)  # Items identified by computer vision
    color_analysis = db.Column(db.JSON)  # Dominant colors, color harmonies
    style_classification = db.Column(db.JSON)  # Style tags and classifications
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'image_type': self.image_type,
            'detected_items': self.detected_items,
            'color_analysis': self.color_analysis,
            'style_classification': self.style_classification,
            'uploaded_at': self.uploaded_at.isoformat(),
        }
