"""
routes/comparison.py - Comparison, Metrics & Transparency routes.
"""

import json
import logging
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models import Module, CaseBase

logger = logging.getLogger(__name__)
comparison_bp = Blueprint('comparison', __name__, url_prefix='/compare')


def _get_profile_and_data():
    """Helper: fetch current user's profile dict, case base, and module pool."""
    profile = current_user.profile
    if not profile:
        return None, [], []
    profile_dict = profile.to_dict()
    cases = [c.to_feature_dict() for c in CaseBase.query.filter_by(outcome_success=True).all()]
    modules = [m.to_dict() for m in Module.query.filter_by(is_active=True).all()]
    return profile_dict, cases, modules


@comparison_bp.route('/')
@login_required
def index():
    """Main comparison page — renders the three-tab interface."""
    profile = current_user.profile
    has_profile = profile is not None and profile.quiz_score is not None
    return render_template('comparison/index.html',
                           has_profile=has_profile,
                           profile=profile)


@comparison_bp.route('/api/run')
@login_required
def api_run():
    """
    API: Run all three pipelines and return comparison JSON.
    Called by the frontend via fetch().
    """
    profile_dict, cases, modules = _get_profile_and_data()
    if not profile_dict:
        return jsonify({'error': 'No profile found. Please complete your profile first.'}), 400

    try:
        from recommender.evaluator import evaluator
        results = evaluator.run_comparison(profile_dict, cases, modules)

        # Serialise for JSON (remove non-serialisable objects)
        out = {'winner': results.get('winner', 'cbr_rbr'), 'systems': {}}
        for key in ('cbr_rbr', 'rbr_cbr', 'parallel'):
            sys_data = results.get(key, {})
            out['systems'][key] = {
                'label':   sys_data.get('label', key),
                'metrics': sys_data.get('metrics', {}),
                'modules': [
                    {
                        'title':       m.get('title', '')[:60],
                        'difficulty':  m.get('difficulty', ''),
                        'module_type': m.get('module_type', ''),
                        'duration_min': m.get('duration_min', 0),
                        'domain':      m.get('domain', ''),
                    }
                    for m in sys_data.get('modules', [])[:6]
                ],
                'meta': {
                    'pipeline':      sys_data.get('meta', {}).get('pipeline', ''),
                    'rules_applied': sys_data.get('meta', {}).get('rules_applied', [])[:6],
                    'cbr_cases': [
                        {
                            'id':    c.get('id'),
                            'goal':  c.get('learning_goal', '')[:50],
                            'sim':   round(c.get('similarity_score', 0) * 100, 1),
                            'skill': c.get('skill_level', ''),
                        }
                        for c in sys_data.get('meta', {}).get('similar_cases', [])[:3]
                    ],
                },
            }
        return jsonify(out)

    except Exception as e:
        logger.error(f"Comparison API error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@comparison_bp.route('/api/transparency')
@login_required
def api_transparency():
    """
    API: Return step-by-step intermediate results of the CBR→RBR pipeline
    for the Transparency tab.
    """
    profile_dict, cases, modules = _get_profile_and_data()
    if not profile_dict:
        return jsonify({'error': 'No profile found'}), 400

    try:
        from recommender.bert_model import bert_model
        from recommender.cbr import CBREngine
        from recommender.rbr import RBREngine
        from recommender.similarity import SimilarityComputer

        cbr = CBREngine()
        rbr = RBREngine()
        sc  = SimilarityComputer()

        # Ensure embedding
        if not profile_dict.get('goal_embedding'):
            profile_dict['goal_embedding'] = bert_model.encode_single(
                profile_dict.get('learning_goal', ''))
        if not profile_dict.get('goal_domain'):
            profile_dict['goal_domain'] = bert_model.classify_domain(
                profile_dict.get('learning_goal', ''))

        module_lookup = {m['id']: m for m in modules if m.get('id')}
        weights = cbr.get_feature_weights(profile_dict.get('persona', 'explorer'))

        # Step 1: BERT encoding
        step1 = {
            'step': 1,
            'name': 'BERT Goal Encoding',
            'description': 'Your learning goal is converted into a 384-dimensional semantic embedding using Sentence-BERT (all-MiniLM-L6-v2).',
            'input':  profile_dict.get('learning_goal', ''),
            'output': {
                'domain_classified': profile_dict.get('goal_domain', ''),
                'embedding_dims': 384,
                'embedding_preview': profile_dict.get('goal_embedding', [])[:6],
            }
        }

        # Step 2: Similarity computation (show top 5 cases with breakdown)
        step2_cases = []
        for case in cases[:10]:
            sim_result = sc.compute_total_similarity(
                profile_dict, case, weights, alpha=0.7)
            step2_cases.append({
                'case_id':   case.get('id'),
                'goal':      case.get('learning_goal', '')[:55],
                'persona':   case.get('persona', ''),
                'skill':     case.get('skill_level', ''),
                'domain':    case.get('goal_domain', ''),
                'total_sim': round(sim_result['total_similarity'] * 100, 1),
                'feat_sim':  round(sim_result['feature_similarity'] * 100, 1),
                'bert_sim':  round(sim_result['bert_similarity'] * 100, 1),
                'breakdown': {k: round(v * 100, 1)
                              for k, v in sim_result['feature_details'].items()},
            })
        step2_cases.sort(key=lambda x: x['total_sim'], reverse=True)

        step2 = {
            'step': 2,
            'name': 'CBR Similarity Computation',
            'description': f'Each case in the case base is scored using: Sim = α·Σ(wf·Simf) + (1-α)·SimBERT where α=0.7. Feature weights are persona-based ({profile_dict.get("persona","")}).',
            'formula': 'Sim_total = 0.7 × Σ(wf × Sim_feature) + 0.3 × Sim_BERT',
            'weights': weights,
            'cases_evaluated': len(cases),
            'top_cases': step2_cases[:5],
        }

        # Step 3: CBR Retrieval
        similar_cases, cbr_candidates = cbr.run(profile_dict, cases, module_lookup)
        step3 = {
            'step': 3,
            'name': 'CBR Top-K Retrieval',
            'description': f'Top-{cbr.top_k} most similar cases are retrieved (similarity ≥ {cbr.min_similarity}). Their module paths are merged using position-weighted voting.',
            'top_k': cbr.top_k,
            'retrieved_cases': [
                {
                    'id':    c.get('id'),
                    'goal':  c.get('learning_goal', '')[:55],
                    'sim':   round(c.get('similarity_score', 0) * 100, 1),
                    'skill': c.get('skill_level', ''),
                    'style': c.get('learning_style', ''),
                }
                for c in similar_cases
            ],
            'candidate_modules_count': len(cbr_candidates),
            'candidate_modules': [
                {
                    'title':      m.get('title', '')[:50],
                    'difficulty': m.get('difficulty', ''),
                    'type':       m.get('module_type', ''),
                    'priority':   round(m.get('cbr_priority', 0), 3),
                }
                for m in cbr_candidates[:8]
            ],
        }

        # Step 4: RBR rule application
        rules_fired = []
        for rule in rbr.rules:
            fired = rule.applies(profile_dict)
            rules_fired.append({
                'name':        rule.name,
                'description': rule.description,
                'priority':    rule.priority,
                'fired':       fired,
            })

        final_modules, rules_applied = rbr.apply_rules(
            cbr_candidates, profile_dict, modules)

        step4 = {
            'step': 4,
            'name': 'RBR Rule Application',
            'description': 'Rules are applied in priority order to filter, reorder, and augment the CBR candidate modules. Each rule checks a condition against your profile.',
            'rules_evaluated': len(rules_fired),
            'rules_fired':     [r for r in rules_fired if r['fired']],
            'rules_not_fired': [r for r in rules_fired if not r['fired']],
            'modules_before':  len(cbr_candidates),
            'modules_after':   len(final_modules),
        }

        # Step 5: Final path
        step5 = {
            'step': 5,
            'name': 'Final Learning Path',
            'description': 'Modules are sorted by difficulty progression (beginner→advanced), deduplicated, and capped at 12.',
            'final_modules': [
                {
                    'order':      i + 1,
                    'title':      m.get('title', '')[:55],
                    'difficulty': m.get('difficulty', ''),
                    'type':       m.get('module_type', ''),
                    'duration':   m.get('duration_min', 0),
                    'domain':     m.get('domain', ''),
                }
                for i, m in enumerate(final_modules)
            ],
            'total_modules':  len(final_modules),
            'total_hours':    round(sum(m.get('duration_min', 60) for m in final_modules) / 60, 1),
        }

        return jsonify({
            'profile': {
                'goal':        profile_dict.get('learning_goal', ''),
                'domain':      profile_dict.get('goal_domain', ''),
                'persona':     profile_dict.get('persona', ''),
                'skill':       profile_dict.get('skill_level', ''),
                'style':       profile_dict.get('learning_style', ''),
                'memory':      profile_dict.get('memory_capacity', ''),
                'background':  profile_dict.get('background', ''),
                'quiz_score':  profile_dict.get('quiz_score', 0),
            },
            'steps': [step1, step2, step3, step4, step5],
        })

    except Exception as e:
        logger.error(f"Transparency API error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500
