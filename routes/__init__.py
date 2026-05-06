"""routes/__init__.py"""
from .auth import auth_bp
from .profile import profile_bp
from .learning_path import lp_bp
from .dashboard import dashboard_bp
from .comparison import comparison_bp

__all__ = ['auth_bp', 'profile_bp', 'lp_bp', 'dashboard_bp', 'comparison_bp']
