from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ai_fashion.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_routes, recommendation_routes, user_routes, image_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(recommendation_routes.bp)
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(image_routes.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
