"""
Recipe Assistant Bot - Configuration
Author: RSK World (https://rskworld.in)
Founder: Molla Samser
Designer & Tester: Rima Khatun
Contact: help@rskworld.in, +91 93305 39277
Year: 2026
"""

import os
from datetime import datetime

class Config:
    """Base configuration class."""
    
    # Basic Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'recipe-assistant-bot-2026-rskworld-secret'
    
    # RSK World Information
    PROJECT_NAME = 'Recipe Assistant Bot'
    PROJECT_VERSION = '1.0.0'
    PROJECT_AUTHOR = 'RSK World'
    PROJECT_FOUNDER = 'Molla Samser'
    PROJECT_DESIGNER = 'Rima Khatun'
    PROJECT_CONTACT_EMAIL = 'help@rskworld.in'
    PROJECT_CONTACT_PHONE = '+91 93305 39277'
    PROJECT_WEBSITE = 'https://rskworld.in'
    PROJECT_YEAR = '2026'
    
    # Project Description
    PROJECT_DESCRIPTION = 'Cooking chatbot for recipe suggestions, ingredient substitutions, and cooking tips'
    PROJECT_CATEGORY = 'Custom Chatbots'
    PROJECT_DIFFICULTY = 'Beginner'
    
    # Technologies Used
    TECHNOLOGIES = ['Python', 'Recipe APIs', 'OpenAI API', 'Database']
    
    # Features
    FEATURES = [
        'Recipe suggestions',
        'Ingredient substitutions', 
        'Cooking tips',
        'Meal planning',
        'Dietary restrictions'
    ]
    
    # API Configuration
    SPOONACULAR_API_KEY = os.environ.get('SPOONACULAR_API_KEY') or None
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or None
    
    # Database Configuration (if using external database)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///recipe_bot.db'
    
    # File Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    
    # Chat Configuration
    MAX_MESSAGE_LENGTH = 500
    MAX_CHAT_HISTORY = 50
    RESPONSE_TIMEOUT = 30
    
    # Recipe Configuration
    DEFAULT_SERVING_SIZE = 4
    SUPPORTED_DIETARY_RESTRICTIONS = [
        'vegetarian', 'vegan', 'gluten-free', 
        'dairy-free', 'keto', 'paleo', 'low-carb'
    ]
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'recipe_bot.log')
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # Debug and Development
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = os.environ.get('TESTING', 'False').lower() == 'true'
    
    # Security
    SSL_DISABLE = os.environ.get('SSL_DISABLE', 'True').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application with this configuration."""
        pass

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = False
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SSL_DISABLE = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific initialization
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                cls.LOG_FILE, 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Recipe Assistant Bot startup')

# Configuration Dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment."""
    return config[os.getenv('FLASK_CONFIG', 'default')]
