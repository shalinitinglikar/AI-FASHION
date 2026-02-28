from app import db
from datetime import datetime

class SavedOutfit(db.Model):
    __tablename__ = 'saved_outfits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recommendation_id = db.Column(db.Integer, db.ForeignKey('recommendations.id'))
    
    outfit_name = db.Column(db.String(255), nullable=False)
    outfit_items = db.Column(db.JSON)  # List of item details
    outfit_image_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'outfit_name': self.outfit_name,
            'outfit_items': self.outfit_items,
            'outfit_image_url': self.outfit_image_url,
            'notes': self.notes,
            'saved_at': self.saved_at.isoformat(),
        }
