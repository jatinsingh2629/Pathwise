"""
models/progress.py - Progress tracking and module assessments.
"""

import json
from datetime import datetime
from .database import db


class Progress(db.Model):
    """Tracks overall progress of a learner on a learning path."""
    __tablename__ = 'progress'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=False)
    current_module_index = db.Column(db.Integer, default=0)
    modules_completed    = db.Column(db.Integer, default=0)
    total_time_spent_min = db.Column(db.Integer, default=0)
    average_score    = db.Column(db.Float,   nullable=True)
    streak_days      = db.Column(db.Integer, default=0)
    last_activity_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_path_id': self.learning_path_id,
            'current_module_index': self.current_module_index,
            'modules_completed': self.modules_completed,
            'total_time_spent_min': self.total_time_spent_min,
            'average_score': self.average_score,
            'streak_days': self.streak_days,
            'last_activity_at': self.last_activity_at.isoformat() if self.last_activity_at else None,
        }


class ModuleAssessment(db.Model):
    """Stores results of post-module quiz/assessment."""
    __tablename__ = 'module_assessments'

    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id            = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    learning_path_id     = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=False)
    score                = db.Column(db.Float, nullable=False)         # 0–100
    answers_json         = db.Column(db.Text, nullable=True)           # User's answers
    time_taken_sec       = db.Column(db.Integer, nullable=True)
    passed               = db.Column(db.Boolean, default=False)
    attempt_number       = db.Column(db.Integer, default=1)
    completed_at         = db.Column(db.DateTime, default=datetime.utcnow)

    def get_answers(self) -> dict:
        if self.answers_json:
            return json.loads(self.answers_json)
        return {}

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'learning_path_id': self.learning_path_id,
            'score': self.score,
            'passed': self.passed,
            'attempt_number': self.attempt_number,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
