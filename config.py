import os

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///placement_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login configuration
    REMEMBER_COOKIE_DURATION = 86400  # 1 day in seconds
