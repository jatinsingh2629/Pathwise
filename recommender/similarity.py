"""
recommender/similarity.py - CBR Similarity Measures.

Implements all similarity functions defined in the system spec:
1. Ordinal similarity (skill level, memory, style)
2. Categorical/Jaccard similarity (background, persona)
3. Numerical similarity (quiz score)
4. BERT semantic similarity (learning goal text)
5. Weighted aggregate similarity

Formula:
  Sim_total(u,c) = α * Σ(wf * Sim_f(u,c)) + (1-α) * Sim_BERT(u,c)
"""

import logging
from typing import Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


class SimilarityComputer:
    """
    Computes multi-feature similarity between a query learner and a case.
    All similarity scores are normalized to [0, 1].
    """

    # Maximum ordinal distances for normalization
    SKILL_MAX_DIST   = 2   # beginner(0) to expert(2)
    MEMORY_MAX_DIST  = 2   # short(0) to long(2)
    STYLE_MAX_DIST   = 4   # theory(0) to mixed(4)
    SCORE_MAX_DIST   = 100 # Quiz score 0–100

    def ordinal_similarity(self, val_u: int, val_c: int, max_distance: int) -> float:
        """
        Ordinal (ordered categorical) similarity.
        Sim = 1 - |index(u) - index(c)| / max_distance

        Args:
            val_u: Ordinal index of user value
            val_c: Ordinal index of case value
            max_distance: Maximum possible ordinal distance
        Returns:
            float in [0, 1]
        """
        if max_distance == 0:
            return 1.0
        return 1.0 - abs(val_u - val_c) / max_distance

    def jaccard_similarity(self, set_u: set, set_c: set) -> float:
        """
        Jaccard similarity for categorical/set features.
        Sim = |u ∩ c| / |u ∪ c|

        Args:
            set_u: Set of values for user
            set_c: Set of values for case
        Returns:
            float in [0, 1]
        """
        if not set_u and not set_c:
            return 1.0
        intersection = len(set_u & set_c)
        union = len(set_u | set_c)
        return intersection / union if union > 0 else 0.0

    def categorical_similarity(self, val_u: str, val_c: str) -> float:
        """
        Simple categorical equality similarity.
        Returns 1 if equal, 0 otherwise.
        """
        return 1.0 if val_u == val_c else 0.0

    def numerical_similarity(self, val_u: float, val_c: float, max_val: float = 100.0) -> float:
        """
        Numerical (continuous) similarity.
        Sim = 1 - |u - c| / max_val

        Args:
            val_u: Numerical value of user
            val_c: Numerical value of case
            max_val: Maximum value for normalization
        Returns:
            float in [0, 1]
        """
        if max_val == 0:
            return 1.0
        return max(0.0, 1.0 - abs(val_u - val_c) / max_val)

    def bert_similarity(self, emb_u: list, emb_c: list) -> float:
        """
        Semantic similarity using pre-computed BERT embeddings.
        Uses cosine similarity.
        """
        if not emb_u or not emb_c:
            return 0.0
        from .bert_model import bert_model
        return bert_model.cosine_similarity(emb_u, emb_c)

    def compute_feature_similarities(
        self,
        user_profile: Dict[str, Any],
        case_features: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Compute individual feature similarities between user and case.

        Returns dict of {feature_name: similarity_score}
        """
        sims = {}

        # 1. Skill Level (ordinal: beginner=0, intermediate=1, expert=2)
        sims['skill_level'] = self.ordinal_similarity(
            user_profile.get('skill_index', 0),
            case_features.get('skill_index', 0),
            self.SKILL_MAX_DIST
        )

        # 2. Memory Capacity (ordinal: short=0, medium=1, long=2)
        sims['memory_capacity'] = self.ordinal_similarity(
            user_profile.get('memory_index', 0),
            case_features.get('memory_index', 0),
            self.MEMORY_MAX_DIST
        )

        # 3. Learning Style (ordinal: theory=0, video=1, labs=2, project=3, mixed=4)
        sims['learning_style'] = self.ordinal_similarity(
            user_profile.get('style_index', 0),
            case_features.get('style_index', 0),
            self.STYLE_MAX_DIST
        )

        # 4. Background (categorical: Jaccard on singleton set)
        sims['background'] = self.jaccard_similarity(
            {user_profile.get('background', '')},
            {case_features.get('background', '')}
        )

        # 5. Goal Domain (categorical)
        sims['goal_domain'] = self.jaccard_similarity(
            {user_profile.get('goal_domain', '')},
            {case_features.get('goal_domain', '')}
        )

        # 6. Quiz Score (numerical)
        sims['quiz_score'] = self.numerical_similarity(
            user_profile.get('quiz_score', 0),
            case_features.get('quiz_score', 0),
            self.SCORE_MAX_DIST
        )

        # 7. Persona (categorical)
        sims['persona'] = self.categorical_similarity(
            user_profile.get('persona', ''),
            case_features.get('persona', '')
        )

        return sims

    def compute_weighted_feature_similarity(
        self,
        feature_sims: Dict[str, float],
        weights: Dict[str, float]
    ) -> float:
        """
        Compute weighted sum of feature similarities.
        Σ(wf * Sim_f) normalized by total weight.
        """
        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0

        weighted_sum = 0.0
        for feature, sim in feature_sims.items():
            w = weights.get(feature, 0.0)
            weighted_sum += w * sim

        return weighted_sum / total_weight

    def compute_total_similarity(
        self,
        user_profile: Dict[str, Any],
        case_features: Dict[str, Any],
        weights: Dict[str, float],
        alpha: float = 0.7
    ) -> Dict[str, Any]:
        """
        Compute total similarity between user profile and a case.

        Formula:
          Sim_total = α * Σ(wf * Sim_f) + (1-α) * Sim_BERT

        Args:
            user_profile: User feature dict
            case_features: Case feature dict
            weights: Feature weights (persona-based)
            alpha: Balance factor (0.7 = 70% feature, 30% BERT)

        Returns:
            Dict with total_similarity, feature_similarities, bert_similarity
        """
        # Feature-based similarity
        feature_sims = self.compute_feature_similarities(user_profile, case_features)
        weighted_feature_sim = self.compute_weighted_feature_similarity(feature_sims, weights)

        # BERT semantic similarity
        bert_sim = self.bert_similarity(
            user_profile.get('goal_embedding', []),
            case_features.get('goal_embedding', [])
        )

        # Aggregate
        total = alpha * weighted_feature_sim + (1 - alpha) * bert_sim

        return {
            'total_similarity': round(total, 4),
            'feature_similarity': round(weighted_feature_sim, 4),
            'bert_similarity': round(bert_sim, 4),
            'feature_details': {k: round(v, 4) for k, v in feature_sims.items()},
            'alpha': alpha,
        }


# Module-level instance
similarity_computer = SimilarityComputer()
