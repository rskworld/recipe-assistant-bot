"""
Recipe Assistant Bot - Main Flask Application
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
Description: Cooking chatbot for recipe suggestions, ingredient substitutions, and cooking tips.
"""

from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'recipe-assistant-bot-2026-rskworld')
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
