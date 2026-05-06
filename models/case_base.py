"""
models/case_base.py - CBR Case Base model.
Stores historical learner cases used for Case-Based Reasoning.
Each case represents a past learner + their successful learning path.
"""

import json
from datetime import datetime
from .database import db


class CaseBase(db.Model):
    """
    CBR Case Base: each row is a solved case (past learner with outcome).
    New learner cases are added upon path completion.
    """
    __tablename__ = 'case_base'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NULL for synthetic cases
    learning_path_id = db.Column(db.Integer, db.ForeignKey('learning_paths.id'), nullable=True)

    # --- Case Features (mirrors LearnerProfile) ---
    persona         = db.Column(db.String(50),  nullable=False)
    learning_goal   = db.Column(db.Text,         nullable=False)
    goal_domain     = db.Column(db.String(100),  nullable=True)
    skill_level     = db.Column(db.String(30),   nullable=False)
    background      = db.Column(db.String(30),   nullable=False)
    memory_capacity = db.Column(db.String(20),   nullable=False)
    learning_style  = db.Column(db.String(30),   nullable=False)
    quiz_score      = db.Column(db.Float,         nullable=True)
    prior_knowledge = db.Column(db.String(20),   nullable=True)

    # BERT embedding of learning goal
    goal_embedding_json = db.Column(db.Text, nullable=True)

    # --- Outcome (the solution) ---
    # Ordered list of module IDs that formed the successful path
    path_module_ids_json = db.Column(db.Text, nullable=False)

    # Outcome quality metrics
    completion_rate  = db.Column(db.Float,   default=1.0)     # 0–1
    avg_assessment_score = db.Column(db.Float, default=75.0)  # 0–100
    learner_rating   = db.Column(db.Float,   nullable=True)   # 1–5
    outcome_success  = db.Column(db.Boolean, default=True)

    # Metadata
    is_synthetic = db.Column(db.Boolean, default=False)    # True = seed data
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    # Ordinal maps (same as LearnerProfile)
    SKILL_ORDINAL   = {'beginner': 0, 'intermediate': 1, 'expert': 2}
    MEMORY_ORDINAL  = {'short': 0, 'medium': 1, 'long': 2}
    STYLE_ORDINAL   = {'theory': 0, 'video': 1, 'labs': 2, 'project': 3, 'mixed': 4}

    def get_goal_embedding(self) -> list:
        if self.goal_embedding_json:
            return json.loads(self.goal_embedding_json)
        return []

    def set_goal_embedding(self, embedding: list):
        self.goal_embedding_json = json.dumps(embedding)

    def get_path_module_ids(self) -> list:
        if self.path_module_ids_json:
            return json.loads(self.path_module_ids_json)
        return []

    def set_path_module_ids(self, ids: list):
        self.path_module_ids_json = json.dumps(ids)

    def to_feature_dict(self) -> dict:
        """Return feature dictionary for CBR similarity computation."""
        return {
            'id': self.id,
            'persona': self.persona,
            'learning_goal': self.learning_goal,
            'goal_domain': self.goal_domain,
            'skill_level': self.skill_level,
            'skill_index': self.SKILL_ORDINAL.get(self.skill_level, 0),
            'background': self.background,
            'memory_capacity': self.memory_capacity,
            'memory_index': self.MEMORY_ORDINAL.get(self.memory_capacity, 0),
            'learning_style': self.learning_style,
            'style_index': self.STYLE_ORDINAL.get(self.learning_style, 0),
            'quiz_score': self.quiz_score or 0,
            'prior_knowledge': self.prior_knowledge or 'beginner',
            'goal_embedding': self.get_goal_embedding(),
            'path_module_ids': self.get_path_module_ids(),
            'completion_rate': self.completion_rate,
            'avg_assessment_score': self.avg_assessment_score,
        }

    @classmethod
    def create_from_learner(cls, profile, path, module_ids: list) -> 'CaseBase':
        """Factory method: create a new case from a completed learner path."""
        case = cls(
            user_id=profile.user_id,
            learning_path_id=path.id,
            persona=profile.persona,
            learning_goal=profile.learning_goal,
            goal_domain=profile.goal_domain,
            skill_level=profile.skill_level,
            background=profile.background,
            memory_capacity=profile.memory_capacity,
            learning_style=profile.learning_style,
            quiz_score=profile.quiz_score,
            prior_knowledge=profile.prior_knowledge,
            goal_embedding_json=profile.goal_embedding_json,
            completion_rate=1.0,
            avg_assessment_score=path.get_completion_percentage(),
            outcome_success=True,
            is_synthetic=False,
        )
        case.set_path_module_ids(module_ids)
        return case

    def __repr__(self):
        return f'<CaseBase id={self.id} goal={self.learning_goal[:40]}>'
