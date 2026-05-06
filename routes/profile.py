"""
routes/profile.py - Profile creation and quiz routes.
"""

import json
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from models import db, LearnerProfile
from recommender.bert_model import bert_model
from utils.quiz import get_quiz_questions, calculate_quiz_score

logger = logging.getLogger(__name__)
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

VALID_PERSONAS   = ['college_student', 'professional', 'job_seeker', 'explorer']
VALID_SKILLS     = ['beginner', 'intermediate', 'expert']
VALID_BACKGROUND = ['tech', 'non_tech']
VALID_MEMORY     = ['short', 'medium', 'long']
VALID_STYLES     = ['theory', 'video', 'labs', 'project', 'mixed']


@profile_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    existing = current_user.profile

    if request.method == 'POST':
        data = {
            'persona':          request.form.get('persona', ''),
            'learning_goal':    request.form.get('learning_goal', '').strip(),
            'skill_level':      request.form.get('skill_level', ''),
            'background':       request.form.get('background', ''),
            'memory_capacity':  request.form.get('memory_capacity', ''),
            'learning_style':   request.form.get('learning_style', ''),
        }

        errors = []
        if data['persona'] not in VALID_PERSONAS:
            errors.append('Please select a valid persona.')
        if not data['learning_goal'] or len(data['learning_goal']) < 10:
            errors.append('Please describe your learning goal (min 10 characters).')
        if data['skill_level'] not in VALID_SKILLS:
            errors.append('Please select a valid skill level.')
        if data['background'] not in VALID_BACKGROUND:
            errors.append('Please select your background.')
        if data['memory_capacity'] not in VALID_MEMORY:
            errors.append('Please select your memory capacity.')
        if data['learning_style'] not in VALID_STYLES:
            errors.append('Please select a learning style.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('profile/create.html', data=data)

        # ── BERT: Encode goal + classify domain ───────────────────────────
        try:
            embedding = bert_model.encode_single(data['learning_goal'])
            domain = bert_model.classify_domain(data['learning_goal'])
        except Exception as e:
            logger.warning(f"BERT processing failed: {e}")
            embedding = []
            domain = 'programming'

        # Re-fetch inside the save block to avoid race conditions
        existing = LearnerProfile.query.filter_by(user_id=current_user.id).first()

        if existing:
            for key, val in data.items():
                setattr(existing, key, val)
            existing.goal_domain = domain
            existing.set_goal_embedding(embedding)
            existing.quiz_score = None
            existing.prior_knowledge = None
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                flash('Profile already saved. Continuing...', 'info')
            profile = existing
        else:
            try:
                profile = LearnerProfile(**data, goal_domain=domain)
                profile.set_goal_embedding(embedding)
                profile.user_id = current_user.id
                db.session.add(profile)
                db.session.commit()
            except Exception:
                db.session.rollback()
                # Profile was created by a duplicate request — just fetch it
                profile = LearnerProfile.query.filter_by(user_id=current_user.id).first()
                if not profile:
                    flash('Error saving profile. Please try again.', 'error')
                    return render_template('profile/create.html', data=data)

        flash(f'Profile saved! Domain detected: {domain.replace("_", " ").title()}', 'success')
        return redirect(url_for('profile.quiz'))

    return render_template('profile/create.html', data=existing.to_dict() if existing else {})


@profile_bp.route('/quiz', methods=['GET'])
@login_required
def quiz():
    profile = current_user.profile
    if not profile:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.create_profile'))

    domain = profile.goal_domain or 'programming'
    questions = get_quiz_questions(domain, n_domain=4, n_computer=3)

    # Store questions in session for scoring
    session['quiz_questions'] = questions
    session['quiz_domain'] = domain

    return render_template('profile/quiz.html', questions=questions, domain=domain,
                           total=len(questions))


@profile_bp.route('/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    profile = current_user.profile
    if not profile:
        return jsonify({'error': 'No profile found'}), 400

    questions = session.get('quiz_questions', [])
    if not questions:
        flash('Quiz session expired. Please retake the quiz.', 'warning')
        return redirect(url_for('profile.quiz'))

    # Collect answers from form
    answers = {}
    for q in questions:
        answer = request.form.get(f"q_{q['id']}")
        if answer is not None:
            answers[q['id']] = int(answer)

    result = calculate_quiz_score(questions, answers)

    # Save to profile
    profile.quiz_score = result['score']
    profile.prior_knowledge = result['classification']
    db.session.commit()

    # Clear quiz from session
    session.pop('quiz_questions', None)

    flash(
        f"Quiz complete! Score: {result['score']:.0f}% ({result['correct']}/{result['total']}) — "
        f"Path level: {result['classification'].title()}",
        'success'
    )
    return redirect(url_for('profile.view_profile'))


@profile_bp.route('/view', methods=['GET'])
@login_required
def view_profile():
    """Display learner's complete profile (after onboarding)."""
    profile = current_user.profile
    if not profile:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.create_profile'))

    # If profile not complete, redirect to create/quiz flow
    if not profile.is_complete():
        flash('Please complete the quiz to finalize your profile.', 'info')
        return redirect(url_for('profile.quiz'))

    persona_display = {
        'college_student': ('🎓', 'College Student', 'Pursuing a degree'),
        'professional': ('💼', 'Professional', 'Working in a field'),
        'job_seeker': ('🔍', 'Job Seeker', 'Seeking employment'),
        'explorer': ('🌎', 'Explorer', 'Learning for fun'),
    }

    skill_display = {
        'beginner': '🌱 Beginner',
        'intermediate': '⚡ Intermediate',
        'expert': '🔥 Expert',
    }

    background_display = {
        'tech': 'Technical Background',
        'non_tech': 'Non-Technical Background',
    }

    memory_display = {
        'short': 'Short (1-2 hours/week)',
        'medium': 'Medium (3-5 hours/week)',
        'long': 'Long (6+ hours/week)',
    }

    style_display = {
        'theory': '📚 Theory & Concepts',
        'video': '🎥 Video Tutorials',
        'labs': '🧪 Hands-on Labs',
        'project': '🚀 Project-Based',
        'mixed': '🎯 Mixed Approach',
    }

    profile_data = {
        'persona': persona_display.get(profile.persona, (profile.persona, profile.persona, '')),
        'learning_goal': profile.learning_goal,
        'goal_domain': profile.goal_domain.replace('_', ' ').title() if profile.goal_domain else 'General',
        'skill_level': skill_display.get(profile.skill_level, profile.skill_level),
        'background': background_display.get(profile.background, profile.background),
        'memory_capacity': memory_display.get(profile.memory_capacity, profile.memory_capacity),
        'learning_style': style_display.get(profile.learning_style, profile.learning_style),
        'quiz_score': f"{profile.quiz_score:.0f}%",
        'path_level': profile.prior_knowledge.title() if profile.prior_knowledge else 'Unknown',
        'created_at': profile.created_at.strftime('%B %d, %Y') if profile.created_at else 'Unknown',
        'updated_at': profile.updated_at.strftime('%B %d, %Y') if profile.updated_at else 'Unknown',
    }

    return render_template('profile/view.html', profile=profile_data, profile_obj=profile)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit learner's profile (after onboarding complete)."""
    profile = current_user.profile
    if not profile:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.create_profile'))

    if not profile.is_complete():
        flash('Please complete the quiz before editing your profile.', 'info')
        return redirect(url_for('profile.quiz'))

    if request.method == 'POST':
        data = {
            'persona':          request.form.get('persona', ''),
            'learning_goal':    request.form.get('learning_goal', '').strip(),
            'skill_level':      request.form.get('skill_level', ''),
            'background':       request.form.get('background', ''),
            'memory_capacity':  request.form.get('memory_capacity', ''),
            'learning_style':   request.form.get('learning_style', ''),
        }

        errors = []
        if data['persona'] not in VALID_PERSONAS:
            errors.append('Please select a valid persona.')
        if not data['learning_goal'] or len(data['learning_goal']) < 10:
            errors.append('Please describe your learning goal (min 10 characters).')
        if data['skill_level'] not in VALID_SKILLS:
            errors.append('Please select a valid skill level.')
        if data['background'] not in VALID_BACKGROUND:
            errors.append('Please select your background.')
        if data['memory_capacity'] not in VALID_MEMORY:
            errors.append('Please select your memory capacity.')
        if data['learning_style'] not in VALID_STYLES:
            errors.append('Please select a learning style.')

        if errors:
            for e in errors:
                flash(e, 'error')
            return render_template('profile/create.html', data=data, mode='edit')

        # ── BERT: Encode goal + classify domain ───────────────────────────
        try:
            embedding = bert_model.encode_single(data['learning_goal'])
            domain = bert_model.classify_domain(data['learning_goal'])
        except Exception as e:
            logger.warning(f"BERT processing failed: {e}")
            embedding = []
            domain = profile.goal_domain or 'programming'

        # Update existing profile
        for key, val in data.items():
            setattr(profile, key, val)
        profile.goal_domain = domain
        profile.set_goal_embedding(embedding)

        try:
            db.session.commit()
            flash(f'Profile updated! Domain: {domain.replace("_", " ").title()}', 'success')
        except Exception:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')

        return redirect(url_for('profile.view_profile'))

    return render_template('profile/create.html', data=profile.to_dict(), mode='edit')
