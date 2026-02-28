from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    profile_image = db.Column(db.String(255))
    
    # User preferences
    style_preferences = db.Column(db.JSON)  # e.g., {"preferred_styles": ["casual", "minimalist"], "colors": ["black", "white"]}
    body_type = db.Column(db.String(50))  # e.g., "pear", "apple", "hourglass"
    climate_preference = db.Column(db.String(50))  # e.g., "tropical", "temperate", "cold"
    budget_range = db.Column(db.String(50))  # e.g., "budget", "mid-range", "luxury"
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='user', lazy=True, cascade='all, delete-orphan')
    style_images = db.relationship('StyleImage', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_outfits = db.relationship('SavedOutfit', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_image': self.profile_image,
            'style_preferences': self.style_preferences,
            'body_type': self.body_type,
            'climate_preference': self.climate_preference,
            'budget_range': self.budget_range,
            'created_at': self.created_at.isoformat(),
        }
