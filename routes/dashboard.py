"""
routes/dashboard.py - Main dashboard showing user's learning overview.
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import LearningPath, Progress, ModuleAssessment

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    return redirect(url_for('auth.login'))


@dashboard_bp.route('/dashboard')
@login_required
def home():
    profile = current_user.profile
    active_path = LearningPath.query.filter_by(
        user_id=current_user.id, is_current=True
    ).first()

    all_paths = LearningPath.query.filter_by(user_id=current_user.id).order_by(
        LearningPath.created_at.desc()
    ).all()

    progress = None
    if active_path:
        progress = Progress.query.filter_by(
            user_id=current_user.id,
            learning_path_id=active_path.id
        ).first()

    # Recent assessments
    recent_assessments = ModuleAssessment.query.filter_by(
        user_id=current_user.id
    ).order_by(ModuleAssessment.completed_at.desc()).limit(5).all()

    stats = {
        'paths_started': len(all_paths),
        'paths_completed': sum(1 for p in all_paths if p.status == 'completed'),
        'avg_score': 0,
        'total_modules_done': sum(p.modules_completed for p in
                                  [Progress.query.filter_by(user_id=current_user.id,
                                   learning_path_id=p.id).first()
                                   for p in all_paths] if p),
    }
    if recent_assessments:
        stats['avg_score'] = round(
            sum(a.score for a in recent_assessments) / len(recent_assessments), 1
        )

    return render_template('dashboard/home.html',
                           profile=profile,
                           active_path=active_path,
                           all_paths=all_paths,
                           progress=progress,
                           stats=stats,
                           recent_assessments=recent_assessments)
