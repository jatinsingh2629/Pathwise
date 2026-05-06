"""
recommender/cbr.py - Case-Based Reasoning Engine.

Implements the CBR cycle:
1. RETRIEVE: Find top-K similar cases from the case base
2. REUSE: Extract module IDs from similar cases
3. REVISE: Merge and deduplicate candidate modules
4. RETAIN: (Done externally when path is completed)

CBR Algorithm:
  For each case c in case_base:
    Sim(u, c) = α * Σ(wf * Sim_f(u,c)) + (1-α) * Sim_BERT(u,c)
  Select Top-K cases with highest similarity
"""

import logging
from typing import List, Dict, Any, Tuple, Optional
from config import Config
from .similarity import similarity_computer

logger = logging.getLogger(__name__)


class CBREngine:
    """
    Case-Based Reasoning engine for learning path recommendation.
    
    Attributes:
        alpha: Balance factor between feature and BERT similarity
        top_k: Number of top similar cases to retrieve
        min_similarity: Minimum similarity threshold for a case to be considered
    """

    def __init__(
        self,
        alpha: float = Config.CBR_ALPHA,
        top_k: int = Config.CBR_TOP_K,
        min_similarity: float = Config.CBR_MIN_SIMILARITY
    ):
        self.alpha = alpha
        self.top_k = top_k
        self.min_similarity = min_similarity
        self.sc = similarity_computer

    def get_feature_weights(self, persona: str) -> Dict[str, float]:
        """
        Get persona-based feature weights from config.
        Different personas prioritize different features.
        """
        weights = Config.PERSONA_WEIGHTS.get(persona, Config.DEFAULT_FEATURE_WEIGHTS)
        logger.debug(f"Using persona '{persona}' weights: {weights}")
        return weights

    def retrieve_similar_cases(
        self,
        user_profile: Dict[str, Any],
        case_base: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        RETRIEVE phase: Find top-K most similar cases.

        Args:
            user_profile: User feature dictionary
            case_base: List of all case feature dictionaries

        Returns:
            List of top-K cases with similarity scores, sorted descending
        """
        if not case_base:
            logger.warning("Case base is empty. No cases to retrieve from.")
            return []

        weights = self.get_feature_weights(user_profile.get('persona', 'explorer'))
        scored_cases = []

        for case in case_base:
            try:
                similarity_result = self.sc.compute_total_similarity(
                    user_profile=user_profile,
                    case_features=case,
                    weights=weights,
                    alpha=self.alpha
                )
                total_sim = similarity_result['total_similarity']

                if total_sim >= self.min_similarity:
                    scored_cases.append({
                        **case,
                        'similarity_score': total_sim,
                        'similarity_details': similarity_result
                    })
            except Exception as e:
                logger.error(f"Error computing similarity for case {case.get('id')}: {e}")
                continue

        # Sort by similarity descending
        scored_cases.sort(key=lambda x: x['similarity_score'], reverse=True)

        # Return top-K
        top_cases = scored_cases[:self.top_k]

        logger.info(
            f"CBR Retrieved {len(top_cases)} cases from {len(case_base)} "
            f"(min_sim={self.min_similarity}, top_k={self.top_k})"
        )
        for i, case in enumerate(top_cases):
            logger.debug(f"  Case {i+1}: id={case.get('id')} sim={case['similarity_score']:.3f}")

        return top_cases

    def extract_candidate_modules(
        self,
        similar_cases: List[Dict[str, Any]],
        all_modules: Dict[int, Any]
    ) -> List[Dict[str, Any]]:
        """
        REUSE phase: Extract and merge module lists from similar cases.

        Uses weighted voting: modules that appear in higher-similarity cases
        get higher priority scores.

        Args:
            similar_cases: Top-K retrieved cases with similarity scores
            all_modules: Dict of {module_id: module_data}

        Returns:
            Ordered list of candidate modules with priority scores
        """
        module_scores: Dict[int, float] = {}

        for case in similar_cases:
            sim_score = case.get('similarity_score', 0.0)
            path_modules = case.get('path_module_ids', [])

            for rank, module_id in enumerate(path_modules):
                module_id = int(module_id)
                if module_id not in all_modules:
                    continue
                # Priority = similarity * (1 / (rank + 1)) for position weighting
                position_weight = 1.0 / (rank + 1)
                priority = sim_score * position_weight
                if module_id in module_scores:
                    module_scores[module_id] += priority
                else:
                    module_scores[module_id] = priority

        # Build candidate list sorted by priority
        candidates = []
        for module_id, priority in sorted(module_scores.items(), key=lambda x: x[1], reverse=True):
            if module_id in all_modules:
                module = dict(all_modules[module_id])
                module['cbr_priority'] = round(priority, 4)
                candidates.append(module)

        logger.info(f"CBR extracted {len(candidates)} candidate modules from {len(similar_cases)} cases")
        return candidates

    def run(
        self,
        user_profile: Dict[str, Any],
        case_base: List[Dict[str, Any]],
        all_modules: Dict[int, Any]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Run complete CBR pipeline: Retrieve → Reuse.

        Returns:
            Tuple of (similar_cases, candidate_modules)
        """
        logger.info(f"Starting CBR for user profile: {user_profile.get('learning_goal', '')[:60]}")

        # Step 1: Retrieve similar cases
        similar_cases = self.retrieve_similar_cases(user_profile, case_base)

        if not similar_cases:
            logger.warning("No similar cases found. Will use RBR-only path generation.")
            return [], []

        # Step 2: Extract candidate modules from cases
        candidate_modules = self.extract_candidate_modules(similar_cases, all_modules)

        return similar_cases, candidate_modules


# Module-level instance
cbr_engine = CBREngine()
