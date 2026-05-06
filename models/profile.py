"""
models/profile.py - Learner Profile model.
Stores all profile attributes used for CBR similarity computation.
"""

import json
from datetime import datetime
from .database import db


class LearnerProfile(db.Model):
    """
    Learner profile containing all attributes for recommendation.
    Linked 1-to-1 with User.
    """
    __tablename__ = 'learner_profiles'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # --- Core Profile Attributes ---
    persona         = db.Column(db.String(50),  nullable=False)   # college_student, professional, job_seeker, explorer
    learning_goal   = db.Column(db.Text,         nullable=False)   # Free-text goal
    goal_domain     = db.Column(db.String(100),  nullable=True)    # Classified domain (e.g., cybersecurity)
    skill_level     = db.Column(db.String(30),   nullable=False)   # beginner, intermediate, expert
    background      = db.Column(db.String(30),   nullable=False)   # tech, non_tech
    memory_capacity = db.Column(db.String(20),   nullable=False)   # short, medium, long
    learning_style  = db.Column(db.String(30),   nullable=False)   # theory, video, labs, project, mixed

    # --- Computed Attributes ---
    goal_embedding_json = db.Column(db.Text, nullable=True)        # BERT embedding stored as JSON
    quiz_score          = db.Column(db.Float, nullable=True)       # 0–100 score from quiz
    prior_knowledge     = db.Column(db.String(20), nullable=True)  # beginner/intermediate (from quiz)

    # --- Metadata ---
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Ordinal Maps for Similarity Calculation ---
    SKILL_ORDINAL   = {'beginner': 0, 'intermediate': 1, 'expert': 2}
    MEMORY_ORDINAL  = {'short': 0, 'medium': 1, 'long': 2}
    STYLE_ORDINAL   = {'theory': 0, 'video': 1, 'labs': 2, 'project': 3, 'mixed': 4}
    PERSONA_ORDINAL = {'explorer': 0, 'college_student': 1, 'job_seeker': 2, 'professional': 3}

    def set_goal_embedding(self, embedding: list):
        """Store BERT embedding as JSON string."""
        self.goal_embedding_json = json.dumps(embedding)

    def get_goal_embedding(self) -> list:
        """Retrieve BERT embedding from JSON."""
        if self.goal_embedding_json:
            return json.loads(self.goal_embedding_json)
        return []

    def get_skill_index(self) -> int:
        return self.SKILL_ORDINAL.get(self.skill_level, 0)

    def get_memory_index(self) -> int:
        return self.MEMORY_ORDINAL.get(self.memory_capacity, 0)

    def get_style_index(self) -> int:
        return self.STYLE_ORDINAL.get(self.learning_style, 0)

    def is_complete(self) -> bool:
        """Check if profile is complete (profile created + quiz taken)."""
        return self.quiz_score is not None and self.prior_knowledge is not None

    def to_dict(self) -> dict:
        """Serialize profile to dictionary for CBR processing."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'persona': self.persona,
            'learning_goal': self.learning_goal,
            'goal_domain': self.goal_domain,
            'skill_level': self.skill_level,
            'skill_index': self.get_skill_index(),
            'background': self.background,
            'memory_capacity': self.memory_capacity,
            'memory_index': self.get_memory_index(),
            'learning_style': self.learning_style,
            'style_index': self.get_style_index(),
            'quiz_score': self.quiz_score or 0,
            'prior_knowledge': self.prior_knowledge or 'beginner',
            'goal_embedding': self.get_goal_embedding(),
        }

    def __repr__(self):
        return f'<LearnerProfile user={self.user_id} goal={self.learning_goal[:40]}>'
