from app import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Recommendation details
    outfit_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    outfit_items = db.Column(db.JSON)  # List of items with details
    styling_tips = db.Column(db.Text)
    occasion = db.Column(db.String(100))  # e.g., "casual", "business", "formal", "weekend"
    season = db.Column(db.String(50))
    trend_tags = db.Column(db.JSON)  # List of current fashion trends
    
    # Images
    outfit_image_url = db.Column(db.String(255))
    items_images = db.Column(db.JSON)  # URLs for individual items
    
    # Scoring
    confidence_score = db.Column(db.Float)  # AI confidence in recommendation
    user_rating = db.Column(db.Integer)  # 1-5 rating
    user_feedback = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'outfit_name': self.outfit_name,
            'description': self.description,
            'outfit_items': self.outfit_items,
            'styling_tips': self.styling_tips,
            'occasion': self.occasion,
            'season': self.season,
            'trend_tags': self.trend_tags,
            'outfit_image_url': self.outfit_image_url,
            'items_images': self.items_images,
            'confidence_score': self.confidence_score,
            'user_rating': self.user_rating,
            'created_at': self.created_at.isoformat(),
        }
