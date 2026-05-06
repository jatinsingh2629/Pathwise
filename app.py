"""
app.py - Flask Application Entry Point.

Uses the Application Factory pattern (create_app) for modularity and testability.
Registers all blueprints, initializes extensions, and seeds the database on first run.

Run with:
    python app.py
or:
    flask run
"""

import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# ── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ── Extensions (initialized without app for factory pattern) ─────────────────
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(config_name: str = 'default') -> Flask:
    """
    Application factory function.
    Creates and configures the Flask application.
    """
    app = Flask(__name__, instance_relative_config=True)

    # ── Load Config ──────────────────────────────────────────────────────────
    from config import config
    app.config.from_object(config[config_name])

    # ── Ensure instance and certificate directories exist ────────────────────
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config.get('CERTIFICATE_DIR', 'static/certificates'), exist_ok=True)

    # ── Initialize Extensions ────────────────────────────────────────────────
    from models.database import db
    db.init_app(app)

    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # ── User Loader (Flask-Login) ────────────────────────────────────────────
    from models.user import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    # ── Register Blueprints ──────────────────────────────────────────────────
    from routes.auth import auth_bp
    from routes.profile import profile_bp
    from routes.learning_path import lp_bp
    from routes.dashboard import dashboard_bp
    from routes.comparison import comparison_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(lp_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(comparison_bp)

    # ── Jinja2 globals / filters ─────────────────────────────────────────────
    app.jinja_env.globals['enumerate'] = enumerate
    app.jinja_env.globals['zip'] = zip
    app.jinja_env.globals['len'] = len

    @app.template_filter('title_domain')
    def title_domain(s):
        return s.replace('_', ' ').title() if s else ''

    # ── Database Initialization + Seeding ────────────────────────────────────
    with app.app_context():
        from models import (
            db as _db, User, LearnerProfile, Course, Module,
            LearningPath, LearningPathModule, Progress, ModuleAssessment, CaseBase
        )
        _db.create_all()
        logger.info("✅ Database tables created.")

        # Seed with sample data if empty
        try:
            from data.seed_data import seed_database
            seed_database(app, _db, {
                'Course': Course, 'Module': Module, 'CaseBase': CaseBase
            })
        except Exception as e:
            logger.warning(f"Seeding skipped or failed: {e}")

    logger.info("PathWise Learning Platform ready.")
    return app


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app = create_app('development')
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disable reloader to avoid double BERT load
    )
