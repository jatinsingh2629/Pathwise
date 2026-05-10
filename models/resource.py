"""
models/resource.py - Resource model for curated learning materials.

Represents external/embedded learning resources (videos, articles, projects,
tutorials, documentation, code examples) attached to a Module, filtered by
learning style so users receive content that matches their preference.
"""

from datetime import datetime
from .database import db


class Resource(db.Model):
    """
    A curated learning resource linked to a specific Module.

    Each resource targets one learning style (video, reading, labs, project)
    and carries enough metadata for the UI to render a rich card with provider
    branding, duration estimate, difficulty badge, and a direct external link.
    """
    __tablename__ = 'resources'

    id             = db.Column(db.Integer, primary_key=True)
    module_id      = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)

    # Content metadata
    title          = db.Column(db.String(300), nullable=False)
    description    = db.Column(db.Text,        nullable=True)

    # Classification
    resource_type  = db.Column(db.String(50),  nullable=False)
    # Allowed values: video | article | project | tutorial | documentation | code_example

    learning_style = db.Column(db.String(30),  nullable=False)
    # Allowed values: video | reading | labs | project

    # Access
    url            = db.Column(db.String(500),  nullable=True)
    is_external    = db.Column(db.Boolean,      default=True)

    # Effort & quality signals
    duration_min   = db.Column(db.Integer,      nullable=True)   # estimated minutes
    difficulty     = db.Column(db.String(30),   nullable=False, default='beginner')
    # Allowed values: beginner | intermediate | advanced

    provider       = db.Column(db.String(100),  nullable=True)   # YouTube, Medium, GitHub …
    rating         = db.Column(db.Float,        default=4.0)     # 1–5 scale

    created_at     = db.Column(db.DateTime,     default=datetime.utcnow)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'id':             self.id,
            'module_id':      self.module_id,
            'title':          self.title,
            'description':    self.description,
            'resource_type':  self.resource_type,
            'learning_style': self.learning_style,
            'url':            self.url,
            'is_external':    self.is_external,
            'duration_min':   self.duration_min,
            'difficulty':     self.difficulty,
            'provider':       self.provider,
            'rating':         self.rating,
            'created_at':     self.created_at.isoformat() if self.created_at else None,
        }

    # Convenience icon mapping used by templates
    @property
    def type_icon(self) -> str:
        icons = {
            'video':         '▶️',
            'article':       '📄',
            'project':       '🚀',
            'tutorial':      '🎓',
            'documentation': '📚',
            'code_example':  '💻',
        }
        return icons.get(self.resource_type, '🔗')

    @property
    def style_icon(self) -> str:
        icons = {
            'video':   '🎬',
            'reading': '📖',
            'labs':    '🔬',
            'project': '🛠️',
        }
        return icons.get(self.learning_style, '📌')

    def __repr__(self):
        return f'<Resource {self.title[:50]} [{self.resource_type}]>'
