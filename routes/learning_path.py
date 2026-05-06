"""
routes/learning_path.py - Learning path generation, viewing, and progress tracking.
"""

import json
import uuid
import logging
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from models import db, LearningPath, LearningPathModule, Module, CaseBase, Progress, ModuleAssessment
from recommender import recommender
from utils.certificate import generate_certificate
import os

logger = logging.getLogger(__name__)
lp_bp = Blueprint('learning_path', __name__, url_prefix='/path')


def _get_module_pool():
    """Fetch all modules as dicts for the recommender."""
    modules = Module.query.filter_by(is_active=True).all()
    return [m.to_dict() for m in modules]


def _get_case_base():
    """Fetch all cases as feature dicts for CBR."""
    cases = CaseBase.query.filter_by(outcome_success=True).all()
    return [c.to_feature_dict() for c in cases]


@lp_bp.route('/generate')
@login_required
def generate():
    """Generate a personalized learning path using CBR + RBR."""
    profile = current_user.profile
    if not profile:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.create_profile'))

    if profile.quiz_score is None:
        flash('Please complete the quiz first.', 'warning')
        return redirect(url_for('profile.quiz'))

    domain = profile.goal_domain or 'general'

    # ── Check if an active path for same domain already exists ──────────────
    existing_path = LearningPath.query.filter_by(
        user_id=current_user.id,
        domain=domain,
        status='active'
    ).first()

    if existing_path:
        # RESET it instead of creating a duplicate
        # Mark all modules incomplete and re-lock
        for i, pm in enumerate(existing_path.path_modules):
            pm.is_completed = False
            pm.completed_at = None
            pm.assessment_score = None
            pm.is_locked = (i > 0)

        # Reset progress
        progress = Progress.query.filter_by(
            user_id=current_user.id,
            learning_path_id=existing_path.id
        ).first()
        if progress:
            progress.modules_completed = 0
            progress.current_module_index = 0
            progress.average_score = None
            progress.last_activity_at = datetime.utcnow()

        # Reset path status
        existing_path.status = 'active'
        existing_path.is_current = True
        existing_path.completed_at = None
        existing_path.certificate_path = None
        existing_path.created_at = datetime.utcnow()

        # Mark all other paths not current
        LearningPath.query.filter(
            LearningPath.user_id == current_user.id,
            LearningPath.id != existing_path.id
        ).update({'is_current': False})

        db.session.commit()
        flash(f'Your learning path has been reset from the beginning!', 'success')
        return redirect(url_for('learning_path.view_path', path_id=existing_path.id))

    # ── No existing path — create a new one ─────────────────────────────────
    # Mark any existing active paths as not current
    LearningPath.query.filter_by(user_id=current_user.id, is_current=True).update({'is_current': False})
    db.session.commit()

    # ── Run Recommendation Pipeline ──────────────────────────────────────────
    user_profile_dict = profile.to_dict()
    case_base = _get_case_base()
    module_pool = _get_module_pool()

    try:
        result = recommender.recommend(
            user_profile=user_profile_dict,
            case_base=case_base,
            module_pool=module_pool,
            encode_goal=False
        )
    except Exception as e:
        logger.error(f"Recommendation failed: {e}", exc_info=True)
        flash('Failed to generate learning path. Please try again.', 'error')
        return redirect(url_for('dashboard.index'))

    if not result['modules']:
        flash('Could not generate a learning path for your profile. Try updating your profile.', 'warning')
        return redirect(url_for('profile.create_profile'))

    # ── Save Learning Path to DB ─────────────────────────────────────────────
    meta = result['metadata']
    path_title = f"{profile.goal_domain.replace('_', ' ').title()} Learning Path"

    path = LearningPath(
        user_id=current_user.id,
        title=path_title,
        domain=result['goal_domain'],
        description=(
            f"Personalized {meta['dominant_difficulty']} path for "
            f"{profile.persona.replace('_', ' ')} — {profile.learning_goal[:80]}"
        ),
        total_modules=meta['total_modules'],
        estimated_hours=meta['total_hours'],
        difficulty=meta['dominant_difficulty'],
        is_current=True,
        status='active',
    )
    path.cbr_cases_used_json = json.dumps(result.get('case_ids_used', []))
    path.cbr_similarity_json = json.dumps(result.get('case_similarities', {}))
    path.rbr_rules_applied_json = json.dumps(result.get('rules_applied', []))
    db.session.add(path)
    db.session.flush()

    for i, mod_dict in enumerate(result['modules']):
        pm = LearningPathModule(
            learning_path_id=path.id,
            module_id=mod_dict['id'],
            order_index=i,
            is_locked=(i > 0),
        )
        db.session.add(pm)

    progress = Progress(
        user_id=current_user.id,
        learning_path_id=path.id,
        current_module_index=0,
        modules_completed=0,
    )
    db.session.add(progress)
    db.session.commit()

    flash(f'Your personalized learning path has been generated: {meta["total_modules"]} modules!', 'success')
    return redirect(url_for('learning_path.view_path', path_id=path.id))


@lp_bp.route('/<int:path_id>')
@login_required
def view_path(path_id):
    """View a learning path with all modules."""
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()
    progress = Progress.query.filter_by(
        user_id=current_user.id, learning_path_id=path_id
    ).first()

    modules_data = [pm.to_dict() for pm in path.path_modules]
    rules = path.get_rbr_rules()

    return render_template('learning_path/view.html',
                           path=path,
                           modules=modules_data,
                           progress=progress,
                           rules_applied=rules,
                           completion=path.get_completion_percentage())


@lp_bp.route('/<int:path_id>/module/<int:path_module_id>')
@login_required
def view_module(path_id, path_module_id):
    """View a single module within a path."""
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()
    pm = LearningPathModule.query.filter_by(
        id=path_module_id, learning_path_id=path_id
    ).first_or_404()

    if pm.is_locked:
        flash('Complete the previous module first.', 'warning')
        return redirect(url_for('learning_path.view_path', path_id=path_id))

    module = pm.module

    # Use topic-relevant questions instead of generic seeded ones
    from utils.assessment_questions import get_questions_for_module
    assessment_questions = get_questions_for_module(
        module_title=module.title,
        module_domain=module.domain,
        n=4
    )

    return render_template('learning_path/module.html',
                           path=path, pm=pm, module=module,
                           questions=assessment_questions)


@lp_bp.route('/<int:path_id>/module/<int:path_module_id>/complete', methods=['POST'])
@login_required
def complete_module(path_id, path_module_id):
    """Mark a module complete and save assessment score."""
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()
    pm = LearningPathModule.query.filter_by(
        id=path_module_id, learning_path_id=path_id
    ).first_or_404()

    module = pm.module
    questions = module.get_assessment_questions()

    # Score the assessment
    correct = 0
    answers = {}
    for i, q in enumerate(questions):
        user_ans = request.form.get(f'q_{i}')
        if user_ans is not None:
            ans_int = int(user_ans)
            answers[str(i)] = ans_int
            if ans_int == q.get('correct', -1):
                correct += 1

    score = (correct / len(questions) * 100) if questions else 80.0

    # Save assessment
    assessment = ModuleAssessment(
        user_id=current_user.id,
        module_id=pm.module_id,
        learning_path_id=path_id,
        score=score,
        answers_json=json.dumps(answers),
        passed=(score >= 50),
    )
    db.session.add(assessment)

    # Mark module complete
    pm.mark_completed(score=score)

    # Unlock next module
    next_pm = LearningPathModule.query.filter_by(
        learning_path_id=path_id,
        order_index=pm.order_index + 1
    ).first()
    if next_pm:
        next_pm.is_locked = False

    # Update progress
    progress = Progress.query.filter_by(
        user_id=current_user.id, learning_path_id=path_id
    ).first()
    if progress:
        progress.modules_completed += 1
        progress.current_module_index = pm.order_index + 1
        progress.last_activity_at = datetime.utcnow()
        # Recalculate average score
        all_assessments = ModuleAssessment.query.filter_by(
            user_id=current_user.id, learning_path_id=path_id
        ).all()
        if all_assessments:
            progress.average_score = sum(a.score for a in all_assessments) / len(all_assessments)

    db.session.commit()

    # Check if all modules completed
    all_completed = all(m.is_completed for m in path.path_modules)
    if all_completed and path.status != 'completed':
        return redirect(url_for('learning_path.complete_path', path_id=path_id))

    flash(f'Module completed! Assessment score: {score:.0f}%', 'success')
    return redirect(url_for('learning_path.view_path', path_id=path_id))


@lp_bp.route('/<int:path_id>/complete')
@login_required
def complete_path(path_id):
    """Handle path completion: generate certificate, store case."""
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()

    if path.status == 'completed' and path.certificate_path:
        return render_template('learning_path/certificate.html', path=path, user=current_user)

    # Mark path complete
    path.status = 'completed'
    path.completed_at = datetime.utcnow()

    # Generate certificate
    cert_dir = current_app.config.get('CERTIFICATE_DIR', 'static/certificates')
    cert_id = str(uuid.uuid4())[:12].upper()
    user_name = current_user.full_name or current_user.username

    cert_path = generate_certificate(
        user_name=user_name,
        course_title=path.title,
        completion_date=datetime.utcnow(),
        output_dir=cert_dir,
        certificate_id=cert_id,
    )
    if cert_path:
        path.certificate_path = os.path.basename(cert_path)

    # ── Store completed case in Case Base ────────────────────────────────────
    profile = current_user.profile
    if profile:
        from models import CaseBase
        module_ids = [pm.module_id for pm in path.path_modules]
        case = CaseBase.create_from_learner(profile, path, module_ids)
        db.session.add(case)

    db.session.commit()
    flash('🎉 Congratulations! You have completed your learning path!', 'success')
    return render_template('learning_path/certificate.html', path=path, user=current_user,
                           cert_id=cert_id)


@lp_bp.route('/api/progress/<int:path_id>')
@login_required
def api_progress(path_id):
    """API endpoint: return progress data as JSON."""
    path = LearningPath.query.filter_by(id=path_id, user_id=current_user.id).first_or_404()
    progress = Progress.query.filter_by(user_id=current_user.id, learning_path_id=path_id).first()
    return jsonify({
        'completion': path.get_completion_percentage(),
        'progress': progress.to_dict() if progress else {},
        'modules': [pm.to_dict() for pm in path.path_modules],
    })
