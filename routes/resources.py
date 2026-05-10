"""
routes/resources.py - Curated learning resources endpoints.

Provides HTML views and a JSON API for browsing resources attached to a
module, optionally filtered by learning style.
"""

import logging
from flask import Blueprint, render_template, jsonify, abort
from flask_login import login_required
from models import Module
from models.resource import Resource

logger = logging.getLogger(__name__)

resources_bp = Blueprint('resources', __name__, url_prefix='/resources')

# Valid learning styles accepted as URL parameters
VALID_STYLES = {'video', 'reading', 'labs', 'project'}

# Map profile learning_style values → resource learning_style values
STYLE_ALIAS = {'theory': 'reading', 'mixed': None}


@resources_bp.route('/module/<int:module_id>')
@login_required
def module_resources(module_id):
    """
    HTML view: all resources for a given module, grouped by learning style.
    """
    module = Module.query.get_or_404(module_id)
    resources = (
        Resource.query
        .filter_by(module_id=module_id)
        .order_by(Resource.learning_style, Resource.rating.desc())
        .all()
    )

    # Group resources by learning style for the template
    grouped = {}
    for res in resources:
        grouped.setdefault(res.learning_style, []).append(res)

    return render_template(
        'learning_path/resources.html',
        module=module,
        resources=resources,
        grouped=grouped,
        active_style=None,
    )


@resources_bp.route('/module/<int:module_id>/by-style/<style>')
@login_required
def module_resources_by_style(module_id, style):
    """
    HTML view: resources for a module filtered to a single learning style.
    """
    if style not in VALID_STYLES:
        abort(404)

    module = Module.query.get_or_404(module_id)
    resources = (
        Resource.query
        .filter_by(module_id=module_id, learning_style=style)
        .order_by(Resource.rating.desc())
        .all()
    )

    # Still build the full grouped dict so the tab bar can show counts
    all_resources = Resource.query.filter_by(module_id=module_id).all()
    grouped = {}
    for res in all_resources:
        grouped.setdefault(res.learning_style, []).append(res)

    return render_template(
        'learning_path/resources.html',
        module=module,
        resources=resources,
        grouped=grouped,
        active_style=style,
    )


@resources_bp.route('/api/module/<int:module_id>')
@login_required
def api_module_resources(module_id):
    """
    JSON API: return all resources for a module, optionally filtered by
    ?style=<learning_style> query parameter.
    """
    module = Module.query.get_or_404(module_id)

    from flask import request
    style = request.args.get('style')

    query = Resource.query.filter_by(module_id=module_id)
    if style and style in VALID_STYLES:
        query = query.filter_by(learning_style=style)

    resources = query.order_by(Resource.rating.desc()).all()

    return jsonify({
        'module_id':    module_id,
        'module_title': module.title,
        'style_filter': style,
        'count':        len(resources),
        'resources':    [r.to_dict() for r in resources],
    })
