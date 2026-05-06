"""
recommender/__init__.py - Main Recommendation Orchestrator.

Ties together CBR + RBR to produce a final learning path.
"""

import logging
from typing import Dict, Any, List, Tuple, Optional

logger = logging.getLogger(__name__)


class LearningPathRecommender:
    """
    Orchestrates the full recommendation pipeline:
    1. Encode user goal with BERT
    2. Run CBR to retrieve similar cases + candidate modules
    3. Run RBR to refine and reorder modules
    4. Return final learning path
    """

    def __init__(self):
        from .bert_model import bert_model
        from .cbr import cbr_engine
        from .rbr import rbr_engine
        self.bert = bert_model
        self.cbr = cbr_engine
        self.rbr = rbr_engine

    def recommend(
        self,
        user_profile: Dict[str, Any],
        case_base: List[Dict[str, Any]],
        module_pool: List[Dict[str, Any]],
        encode_goal: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning path recommendation.

        Args:
            user_profile: User's feature dictionary
            case_base: List of all historical cases
            module_pool: All available modules as dicts
            encode_goal: Whether to encode the goal (False if already encoded)

        Returns:
            Dict containing:
                - modules: Ordered list of recommended modules
                - similar_cases: Cases used for CBR
                - rules_applied: RBR rules that fired
                - metadata: Stats about the recommendation
        """
        logger.info(f"🚀 Starting recommendation for: {user_profile.get('learning_goal', '')[:60]}")

        # Step 1: Encode learning goal if not already done
        if encode_goal or not user_profile.get('goal_embedding'):
            goal_text = user_profile.get('learning_goal', '')
            if goal_text:
                try:
                    embedding = self.bert.encode_single(goal_text)
                    user_profile = {**user_profile, 'goal_embedding': embedding}
                    logger.info(f"✅ BERT encoded goal ({len(embedding)}D)")
                except Exception as e:
                    logger.warning(f"BERT encoding failed: {e}")

        # Classify domain if not set
        if not user_profile.get('goal_domain'):
            goal_text = user_profile.get('learning_goal', '')
            domain = self.bert.classify_domain(goal_text)
            user_profile = {**user_profile, 'goal_domain': domain}
            logger.info(f"✅ Domain classified: {domain}")

        # Step 2: Build module lookup dict
        module_lookup = {m['id']: m for m in module_pool if m.get('id')}

        # Step 3: CBR Phase
        similar_cases, cbr_candidates = self.cbr.run(
            user_profile=user_profile,
            case_base=case_base,
            all_modules=module_lookup
        )

        # If CBR returns nothing, use full module pool as candidates
        if not cbr_candidates:
            logger.warning("CBR returned no candidates. Using domain-filtered module pool.")
            domain = user_profile.get('goal_domain', '')
            cbr_candidates = [
                m for m in module_pool
                if m.get('domain') == domain or domain == ''
            ]
            # Add fallback priority score
            for m in cbr_candidates:
                m.setdefault('cbr_priority', 0.1)

        # Step 4: RBR Phase
        final_modules, rules_applied = self.rbr.apply_rules(
            candidate_modules=cbr_candidates,
            user_profile=user_profile,
            module_pool=module_pool
        )

        # Step 5: Compute metadata
        total_hours = sum(
            m.get('duration_min', 60) / 60.0 for m in final_modules
        )
        domains_in_path = list({m.get('domain') for m in final_modules if m.get('domain')})
        difficulties = [m.get('difficulty') for m in final_modules if m.get('difficulty')]
        dominant_difficulty = max(set(difficulties), key=difficulties.count) if difficulties else 'intermediate'

        # Assign order indices
        for i, module in enumerate(final_modules):
            module['path_order'] = i + 1

        # Case IDs used
        case_ids = [c.get('id') for c in similar_cases]
        case_sims = {c.get('id'): c.get('similarity_score') for c in similar_cases}

        result = {
            'modules': final_modules,
            'similar_cases': similar_cases,
            'case_ids_used': case_ids,
            'case_similarities': case_sims,
            'rules_applied': rules_applied,
            'goal_domain': user_profile.get('goal_domain'),
            'metadata': {
                'total_modules': len(final_modules),
                'total_hours': round(total_hours, 1),
                'dominant_difficulty': dominant_difficulty,
                'domains': domains_in_path,
                'cbr_cases_used': len(similar_cases),
                'rbr_rules_applied': len(rules_applied),
            }
        }

        logger.info(
            f"✅ Recommendation complete: {len(final_modules)} modules, "
            f"{total_hours:.1f}h, {len(similar_cases)} CBR cases, "
            f"{len(rules_applied)} RBR rules"
        )
        return result


# Module-level singleton
recommender = LearningPathRecommender()
