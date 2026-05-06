"""
models/course.py - Course and Module models.
Represents the module pool sourced from Coursera Courses Metadata.
"""

import json
from datetime import datetime
from .database import db


class Course(db.Model):
    """
    Course model representing a full Coursera-like course.
    Maps to the Coursera Courses Metadata dataset.
    """
    __tablename__ = 'courses'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(300), nullable=False)
    provider     = db.Column(db.String(100), default='Coursera')
    category     = db.Column(db.String(100), nullable=False)      # e.g., 'Data Science', 'Cybersecurity'
    subcategory  = db.Column(db.String(100), nullable=True)
    difficulty   = db.Column(db.String(30),  nullable=False)      # beginner, intermediate, advanced
    duration_hrs = db.Column(db.Float,        nullable=True)       # Estimated hours
    format_type  = db.Column(db.String(30),   nullable=False)      # video, lab, project, theory, mixed
    description  = db.Column(db.Text,         nullable=True)
    prerequisites_json = db.Column(db.Text,   nullable=True)       # JSON list of prerequisite IDs
    rating       = db.Column(db.Float,        default=4.0)
    enrolled_count = db.Column(db.Integer,    default=0)
    url          = db.Column(db.String(500),  nullable=True)
    created_at   = db.Column(db.DateTime,     default=datetime.utcnow)

    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True, cascade='all, delete-orphan')

    def get_prerequisites(self) -> list:
        if self.prerequisites_json:
            return json.loads(self.prerequisites_json)
        return []

    def set_prerequisites(self, prereqs: list):
        self.prerequisites_json = json.dumps(prereqs)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'provider': self.provider,
            'category': self.category,
            'subcategory': self.subcategory,
            'difficulty': self.difficulty,
            'duration_hrs': self.duration_hrs,
            'format_type': self.format_type,
            'description': self.description,
            'prerequisites': self.get_prerequisites(),
            'rating': self.rating,
            'url': self.url,
        }

    def __repr__(self):
        return f'<Course {self.title[:50]}>'


class Module(db.Model):
    """
    Module model - a single learning unit within a course.
    These are the building blocks of a learning path.
    """
    __tablename__ = 'modules'

    id           = db.Column(db.Integer, primary_key=True)
    course_id    = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title        = db.Column(db.String(300), nullable=False)
    description  = db.Column(db.Text,        nullable=True)
    module_type  = db.Column(db.String(30),  nullable=False)      # video, lab, project, reading, quiz
    difficulty   = db.Column(db.String(30),  nullable=False)      # beginner, intermediate, advanced
    duration_min = db.Column(db.Integer,      nullable=True)       # Duration in minutes
    domain       = db.Column(db.String(100),  nullable=False)      # Topic domain
    tags_json    = db.Column(db.Text,         nullable=True)       # JSON list of tags
    order_index  = db.Column(db.Integer,      default=0)           # Order within course
    is_active    = db.Column(db.Boolean,      default=True)

    # Assessment questions for this module (JSON)
    assessment_questions_json = db.Column(db.Text, nullable=True)

    def get_tags(self) -> list:
        if self.tags_json:
            return json.loads(self.tags_json)
        return []

    def set_tags(self, tags: list):
        self.tags_json = json.dumps(tags)

    def get_assessment_questions(self) -> list:
        if self.assessment_questions_json:
            return json.loads(self.assessment_questions_json)
        return []

    def set_assessment_questions(self, questions: list):
        self.assessment_questions_json = json.dumps(questions)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'module_type': self.module_type,
            'difficulty': self.difficulty,
            'duration_min': self.duration_min,
            'domain': self.domain,
            'tags': self.get_tags(),
            'order_index': self.order_index,
            'course_title': self.course.title if self.course else '',
        }

    def __repr__(self):
        return f'<Module {self.title[:50]}>'
