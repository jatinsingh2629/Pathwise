"""
recommender/rbr.py - Rule-Based Reasoning Engine.

Applies predefined rules to filter, reorder, and augment learning paths.
Rules are applied AFTER CBR candidate modules are retrieved.

Rules are structured as:
  condition: lambda(profile) -> bool
  action: lambda(modules, profile, pool) -> modules
  name: str (for logging/display)
  priority: int (lower = applied first)
"""

import logging
from typing import List, Dict, Any, Callable, Tuple
import copy

logger = logging.getLogger(__name__)


class Rule:
    """
    Represents a single RBR rule with condition and action.
    """
    def __init__(
        self,
        name: str,
        description: str,
        condition: Callable,
        action: Callable,
        priority: int = 5
    ):
        self.name = name
        self.description = description
        self.condition = condition  # (profile) -> bool
        self.action = action        # (modules, profile, module_pool) -> modules
        self.priority = priority

    def applies(self, profile: Dict[str, Any]) -> bool:
        """Check if this rule's condition is satisfied."""
        try:
            return bool(self.condition(profile))
        except Exception as e:
            logger.error(f"Rule '{self.name}' condition error: {e}")
            return False

    def apply(
        self,
        modules: List[Dict[str, Any]],
        profile: Dict[str, Any],
        module_pool: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], str]:
        """Apply rule action and return (modified_modules, message)."""
        try:
            result = self.action(modules, profile, module_pool)
            return result, f"Applied: {self.description}"
        except Exception as e:
            logger.error(f"Rule '{self.name}' action error: {e}")
            return modules, f"Failed: {self.name}"

    def __repr__(self):
        return f'<Rule name={self.name} priority={self.priority}>'


def _get_modules_by(modules: List[Dict], key: str, value) -> List[Dict]:
    """Helper: Filter modules by a key-value pair."""
    return [m for m in modules if m.get(key) == value]


def _remove_modules_by(modules: List[Dict], key: str, value) -> List[Dict]:
    """Helper: Remove modules matching key-value."""
    return [m for m in modules if m.get(key) != value]


def _get_modules_from_pool(pool: List[Dict], domain: str, difficulty: str, style: str = None, max_n: int = 3) -> List[Dict]:
    """Helper: Find modules from pool matching criteria."""
    results = []
    for m in pool:
        if m.get('domain') != domain:
            continue
        if m.get('difficulty') != difficulty:
            continue
        if style and m.get('module_type') not in [style, 'mixed']:
            continue
        results.append(m)
        if len(results) >= max_n:
            break
    return results


class RBREngine:
    """
    Rule-Based Reasoning engine.
    Maintains a list of rules and applies them to refine module lists.
    """

    def __init__(self):
        self.rules: List[Rule] = []
        self._register_default_rules()

    def _register_default_rules(self):
        """Register all predefined learning path rules."""

        # ── RULE 1: Beginner → Remove advanced modules ──────────────────────
        self.add_rule(Rule(
            name='remove_advanced_for_beginner',
            description='Removed advanced modules (beginner skill level)',
            priority=1,
            condition=lambda p: p.get('skill_level') == 'beginner',
            action=lambda modules, p, pool: [
                m for m in modules if m.get('difficulty') != 'advanced'
            ]
        ))

        # ── RULE 2: Expert → Remove beginner modules ────────────────────────
        self.add_rule(Rule(
            name='remove_beginner_for_expert',
            description='Removed beginner modules (expert skill level)',
            priority=1,
            condition=lambda p: p.get('skill_level') == 'expert',
            action=lambda modules, p, pool: [
                m for m in modules if m.get('difficulty') != 'beginner'
            ]
        ))

        # ── RULE 3: Quiz pass → Skip beginner modules ───────────────────────
        self.add_rule(Rule(
            name='skip_beginner_if_quiz_passed',
            description='Skipped beginner modules (quiz score ≥ 50)',
            priority=2,
            condition=lambda p: float(p.get('quiz_score', 0)) >= 50,
            action=lambda modules, p, pool: [
                m for m in modules if m.get('difficulty') != 'beginner'
            ]
        ))

        # ── RULE 4: Short memory → Add revision modules ──────────────────────
        self.add_rule(Rule(
            name='add_revision_for_short_memory',
            description='Added revision/summary modules (short memory capacity)',
            priority=3,
            condition=lambda p: p.get('memory_capacity') == 'short',
            action=self._action_add_revision_modules
        ))

        # ── RULE 5: Video style → Prioritize video modules ──────────────────
        self.add_rule(Rule(
            name='prioritize_video_modules',
            description='Prioritized video-format modules (video learning style)',
            priority=3,
            condition=lambda p: p.get('learning_style') == 'video',
            action=lambda modules, p, pool: sorted(
                modules,
                key=lambda m: (0 if m.get('module_type') == 'video' else 1)
            )
        ))

        # ── RULE 6: Labs style → Prioritize lab/hands-on ───────────────────
        self.add_rule(Rule(
            name='prioritize_lab_modules',
            description='Prioritized lab/hands-on modules (labs learning style)',
            priority=3,
            condition=lambda p: p.get('learning_style') == 'labs',
            action=lambda modules, p, pool: sorted(
                modules,
                key=lambda m: (0 if m.get('module_type') in ['lab', 'labs', 'project'] else 1)
            )
        ))

        # ── RULE 7: Theory style → Prioritize reading/theory modules ───────
        self.add_rule(Rule(
            name='prioritize_theory_modules',
            description='Prioritized theory/reading modules (theory learning style)',
            priority=3,
            condition=lambda p: p.get('learning_style') == 'theory',
            action=lambda modules, p, pool: sorted(
                modules,
                key=lambda m: (0 if m.get('module_type') in ['reading', 'theory', 'text'] else 1)
            )
        ))

        # ── RULE 8: Non-tech background → Add fundamentals first ────────────
        self.add_rule(Rule(
            name='add_fundamentals_for_non_tech',
            description='Added fundamentals modules at start (non-tech background)',
            priority=2,
            condition=lambda p: p.get('background') == 'non_tech',
            action=self._action_add_fundamentals
        ))

        # ── RULE 9: Job seeker → Focus on practical/project modules ─────────
        self.add_rule(Rule(
            name='focus_practical_for_job_seeker',
            description='Prioritized practical/project modules (job seeker persona)',
            priority=4,
            condition=lambda p: p.get('persona') == 'job_seeker',
            action=lambda modules, p, pool: sorted(
                modules,
                key=lambda m: (0 if m.get('module_type') in ['project', 'lab', 'labs'] else 1)
            )
        ))

        # ── RULE 10: Professional → Limit path length to high-value modules ─
        self.add_rule(Rule(
            name='limit_for_professional',
            description='Limited path to top 8 highest-value modules (professional persona)',
            priority=5,
            condition=lambda p: p.get('persona') == 'professional',
            action=lambda modules, p, pool: sorted(
                modules,
                key=lambda m: -m.get('cbr_priority', 0)
            )[:8]
        ))

        # ── RULE 11: Long memory → Add capstone project ──────────────────────
        self.add_rule(Rule(
            name='add_capstone_for_long_memory',
            description='Added capstone project module (long memory capacity)',
            priority=6,
            condition=lambda p: p.get('memory_capacity') == 'long',
            action=self._action_add_capstone
        ))

        # ── RULE 12: Sort path by difficulty progression ─────────────────────
        self.add_rule(Rule(
            name='sort_by_difficulty_progression',
            description='Sorted modules by difficulty progression (beginner → advanced)',
            priority=10,  # Always applied last
            condition=lambda p: True,  # Always applies
            action=self._action_sort_by_difficulty
        ))

        # Sort rules by priority
        self.rules.sort(key=lambda r: r.priority)

    # ── Complex Rule Actions ────────────────────────────────────────────────

    def _action_add_revision_modules(
        self,
        modules: List[Dict],
        profile: Dict,
        module_pool: List[Dict]
    ) -> List[Dict]:
        """Add revision/summary modules after every N modules."""
        if not modules:
            return modules
        result = []
        for i, module in enumerate(modules):
            result.append(module)
            # Insert a revision module every 3 modules
            if (i + 1) % 3 == 0 and (i + 1) < len(modules):
                domain = profile.get('goal_domain', '')
                revision_candidates = [
                    m for m in module_pool
                    if 'revision' in m.get('title', '').lower() or
                       'summary' in m.get('title', '').lower() or
                       'review' in m.get('title', '').lower()
                ]
                if revision_candidates and not any(
                    m.get('id') == revision_candidates[0].get('id') for m in result
                ):
                    rev = dict(revision_candidates[0])
                    rev['is_revision'] = True
                    result.append(rev)
        return result

    def _action_add_fundamentals(
        self,
        modules: List[Dict],
        profile: Dict,
        module_pool: List[Dict]
    ) -> List[Dict]:
        """Prepend fundamental/intro modules for non-tech learners."""
        fundamentals = []
        for m in module_pool:
            title_lower = m.get('title', '').lower()
            if any(kw in title_lower for kw in
                   ['introduction', 'intro', 'fundamentals', 'basics', 'getting started', '101']):
                if m.get('difficulty') == 'beginner':
                    if not any(existing.get('id') == m.get('id') for existing in modules):
                        fundamentals.append(dict(m))
                        if len(fundamentals) >= 2:
                            break
        return fundamentals + modules

    def _action_add_capstone(
        self,
        modules: List[Dict],
        profile: Dict,
        module_pool: List[Dict]
    ) -> List[Dict]:
        """Append a capstone project at the end for long-memory learners."""
        capstone_candidates = [
            m for m in module_pool
            if 'capstone' in m.get('title', '').lower() or
               'final project' in m.get('title', '').lower() or
               (m.get('module_type') == 'project' and m.get('difficulty') == 'advanced')
        ]
        if capstone_candidates:
            capstone = dict(capstone_candidates[0])
            capstone['is_capstone'] = True
            if not any(m.get('id') == capstone.get('id') for m in modules):
                return modules + [capstone]
        return modules

    def _action_sort_by_difficulty(
        self,
        modules: List[Dict],
        profile: Dict,
        module_pool: List[Dict]
    ) -> List[Dict]:
        """Sort modules by difficulty: beginner → intermediate → advanced."""
        difficulty_order = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        # Stable sort: preserve relative order within same difficulty
        return sorted(modules, key=lambda m: difficulty_order.get(m.get('difficulty', 'intermediate'), 1))

    # ── Public Interface ────────────────────────────────────────────────────

    def add_rule(self, rule: Rule):
        """Register a new rule."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority)

    def apply_rules(
        self,
        candidate_modules: List[Dict[str, Any]],
        user_profile: Dict[str, Any],
        module_pool: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """
        Apply all applicable rules to the candidate module list.

        Args:
            candidate_modules: Modules from CBR phase
            user_profile: User feature dictionary
            module_pool: Full module pool (for adding new modules)

        Returns:
            Tuple of (refined_modules, list_of_applied_rule_descriptions)
        """
        modules = copy.deepcopy(candidate_modules)
        applied_rules = []

        logger.info(f"Starting RBR with {len(modules)} candidate modules")

        for rule in self.rules:
            if rule.applies(user_profile):
                before_count = len(modules)
                modules, message = rule.apply(modules, user_profile, module_pool)
                after_count = len(modules)
                applied_rules.append({
                    'rule': rule.name,
                    'description': message,
                    'modules_before': before_count,
                    'modules_after': after_count,
                })
                logger.info(f"  Rule '{rule.name}': {before_count} → {after_count} modules. {message}")

        # Ensure no duplicates (by module id)
        seen_ids = set()
        unique_modules = []
        for m in modules:
            mid = m.get('id')
            if mid not in seen_ids:
                seen_ids.add(mid)
                unique_modules.append(m)

        # Ensure minimum path length (at least 3 modules)
        if len(unique_modules) < 3:
            logger.warning(f"Path too short ({len(unique_modules)} modules). Adding fallback modules.")
            unique_modules = self._fill_path_with_fallback(
                unique_modules, user_profile, module_pool
            )

        # Cap maximum path length at 12 modules
        if len(unique_modules) > 12:
            unique_modules = unique_modules[:12]

        logger.info(f"RBR completed: {len(unique_modules)} final modules, {len(applied_rules)} rules applied")
        return unique_modules, [r['description'] for r in applied_rules]

    def _fill_path_with_fallback(
        self,
        modules: List[Dict],
        profile: Dict,
        module_pool: List[Dict]
    ) -> List[Dict]:
        """Add fallback modules if path is too short."""
        existing_ids = {m.get('id') for m in modules}
        domain = profile.get('goal_domain', '')
        skill = profile.get('skill_level', 'beginner')

        fallbacks = []
        for m in module_pool:
            if m.get('id') not in existing_ids:
                if m.get('domain') == domain or m.get('difficulty') == skill:
                    fallbacks.append(m)
                    existing_ids.add(m.get('id'))
                    if len(modules) + len(fallbacks) >= 5:
                        break

        return modules + fallbacks


# Module-level instance
rbr_engine = RBREngine()
