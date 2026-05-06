"""
models/user.py - User authentication model.
Handles user registration, login, and session management.
"""

from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
from .database import db


class User(UserMixin, db.Model):
    """
    User model for authentication.
    Uses UserMixin from Flask-Login for session management.
    """
    __tablename__ = 'users'

    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(80),  unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name   = db.Column(db.String(150), nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    last_login  = db.Column(db.DateTime, nullable=True)
    is_active   = db.Column(db.Boolean, default=True)

    # Relationships
    profile       = db.relationship('LearnerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    learning_paths = db.relationship('LearningPath', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash and store password securely using bcrypt."""
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self) -> dict:
        """Serialize user to dictionary (excluding sensitive fields)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'has_profile': self.profile is not None,
        }

    def __repr__(self):
        return f'<User {self.username}>'
