"""
config.py - Application Configuration
Centralized configuration for different environments.
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-2024')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'learning_path.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # ML Configuration
    BERT_MODEL_NAME = 'all-MiniLM-L6-v2'  # Lightweight Sentence-BERT
    CBR_ALPHA = 0.7          # Weight for feature similarity vs BERT similarity
    CBR_TOP_K = 2            # Number of similar cases to retrieve
    CBR_MIN_SIMILARITY = 0.3 # Minimum similarity threshold

    # Quiz Configuration
    QUIZ_PASS_THRESHOLD = 50  # Score >= 50 -> Intermediate path

    # Certificate Storage
    CERTIFICATE_DIR = os.path.join(BASE_DIR, 'static', 'certificates')

    # Data paths
    SAMPLE_DATA_DIR = os.path.join(BASE_DIR, 'data')

    # Feature Weights (persona-based will override per persona)
    DEFAULT_FEATURE_WEIGHTS = {
        'skill_level': 0.25,
        'learning_style': 0.20,
        'background': 0.15,
        'memory_capacity': 0.15,
        'goal_domain': 0.25,
    }

    PERSONA_WEIGHTS = {
        'college_student': {
            'skill_level': 0.20, 'learning_style': 0.25,
            'background': 0.15, 'memory_capacity': 0.15, 'goal_domain': 0.25
        },
        'professional': {
            'skill_level': 0.30, 'learning_style': 0.15,
            'background': 0.20, 'memory_capacity': 0.10, 'goal_domain': 0.25
        },
        'job_seeker': {
            'skill_level': 0.25, 'learning_style': 0.20,
            'background': 0.20, 'memory_capacity': 0.10, 'goal_domain': 0.25
        },
        'explorer': {
            'skill_level': 0.15, 'learning_style': 0.30,
            'background': 0.10, 'memory_capacity': 0.20, 'goal_domain': 0.25
        }
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
