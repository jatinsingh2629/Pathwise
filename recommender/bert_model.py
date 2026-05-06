"""
recommender/bert_model.py - BERT / Sentence-BERT model wrapper.

Uses Sentence-Transformers (all-MiniLM-L6-v2) to:
1. Encode learning goal text into embeddings
2. Classify domain from free-text goal
3. Compute semantic cosine similarity
"""

import re
import logging
from typing import List, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Domain keyword map for classification
DOMAIN_KEYWORDS = {
    'cybersecurity': [
        'cyber', 'security', 'hack', 'pentest', 'penetration', 'ctf', 'malware',
        'forensics', 'network security', 'ethical hack', 'infosec', 'vulnerability',
        'firewall', 'soc', 'threat', 'exploit'
    ],
    'data_science': [
        'data science', 'machine learning', 'ml', 'ai', 'deep learning', 'neural',
        'data analyst', 'data engineer', 'statistics', 'data mining', 'big data',
        'python data', 'pandas', 'tensorflow', 'pytorch'
    ],
    'web_development': [
        'web dev', 'frontend', 'backend', 'full stack', 'html', 'css', 'javascript',
        'react', 'angular', 'vue', 'node', 'django', 'flask', 'api', 'rest'
    ],
    'cloud_computing': [
        'cloud', 'aws', 'azure', 'gcp', 'devops', 'kubernetes', 'docker',
        'infrastructure', 'serverless', 'microservice', 'ci/cd', 'deployment'
    ],
    'programming': [
        'programming', 'coding', 'software', 'developer', 'java', 'python',
        'c++', 'algorithms', 'data structures', 'computer science', 'software engineer'
    ],
    'business_analytics': [
        'business', 'analytics', 'excel', 'sql', 'power bi', 'tableau',
        'reporting', 'kpi', 'dashboard', 'bi developer', 'business intelligence'
    ],
    'ui_ux_design': [
        'design', 'ui', 'ux', 'figma', 'user interface', 'user experience',
        'prototyping', 'wireframe', 'product design', 'graphic design'
    ],
    'mobile_development': [
        'mobile', 'android', 'ios', 'swift', 'kotlin', 'flutter', 'react native',
        'app development', 'mobile app'
    ],
    'database': [
        'database', 'sql', 'mysql', 'postgresql', 'mongodb', 'nosql',
        'dba', 'database admin', 'data modeling', 'orm'
    ],
    'networking': [
        'network', 'ccna', 'cisco', 'routing', 'switching', 'tcp/ip',
        'protocol', 'wireless', 'network admin', 'infrastructure'
    ],
}


class BERTModel:
    """
    Singleton wrapper around Sentence-Transformers model.
    Lazy-loads to avoid slow startup.
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_model(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Lazy-load Sentence-BERT model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading Sentence-BERT model: {model_name}")
                self._model = SentenceTransformer(model_name)
                logger.info("✅ BERT model loaded successfully.")
            except ImportError:
                logger.warning("sentence-transformers not installed. Using fallback TF-IDF embeddings.")
                self._model = None
            except Exception as e:
                logger.error(f"Failed to load BERT model: {e}")
                self._model = None
        return self._model

    def encode(self, texts: List[str], model_name: str = 'all-MiniLM-L6-v2') -> np.ndarray:
        """
        Encode list of texts to embeddings.
        Falls back to TF-IDF if BERT unavailable.
        """
        model = self.load_model(model_name)
        if model is not None:
            try:
                embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
                return embeddings
            except Exception as e:
                logger.error(f"BERT encoding failed: {e}")

        # --- Fallback: TF-IDF based embeddings ---
        return self._tfidf_fallback(texts)

    def _tfidf_fallback(self, texts: List[str]) -> np.ndarray:
        """
        TF-IDF based fallback embeddings when BERT is unavailable.
        Uses all domain keywords as vocabulary.
        """
        vocab = []
        for keywords in DOMAIN_KEYWORDS.values():
            vocab.extend(keywords)
        vocab = list(set(vocab))

        embeddings = []
        for text in texts:
            text_lower = text.lower()
            vec = np.array([
                1.0 if kw in text_lower else 0.0
                for kw in vocab
            ], dtype=np.float32)
            # L2 normalize
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            embeddings.append(vec)
        return np.array(embeddings)

    def encode_single(self, text: str, model_name: str = 'all-MiniLM-L6-v2') -> List[float]:
        """Encode a single text and return as Python list."""
        embeddings = self.encode([text], model_name)
        return embeddings[0].tolist()

    def cosine_similarity(self, emb1: List[float], emb2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        Returns value in [0, 1].
        """
        if not emb1 or not emb2:
            return 0.0
        a = np.array(emb1, dtype=np.float32)
        b = np.array(emb2, dtype=np.float32)
        if len(a) != len(b):
            # Truncate to shorter length
            min_len = min(len(a), len(b))
            a, b = a[:min_len], b[:min_len]
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        similarity = np.dot(a, b) / (norm_a * norm_b)
        return float(np.clip(similarity, 0.0, 1.0))

    def classify_domain(self, text: str) -> str:
        """
        Classify learning goal text into a domain using keyword matching + semantic scoring.
        Returns the most likely domain name.
        """
        text_lower = text.lower()
        domain_scores = {}

        # Keyword matching score
        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw in text_lower:
                    score += len(kw.split())  # Longer match = higher weight
            domain_scores[domain] = score

        # If we have a clear winner, return it
        best_domain = max(domain_scores, key=domain_scores.get)
        if domain_scores[best_domain] > 0:
            return best_domain

        # Fallback: try BERT semantic similarity against domain names
        try:
            goal_emb = self.encode_single(text)
            best_score = 0
            best_domain = 'programming'  # Default fallback
            for domain in DOMAIN_KEYWORDS.keys():
                domain_emb = self.encode_single(domain.replace('_', ' '))
                score = self.cosine_similarity(goal_emb, domain_emb)
                if score > best_score:
                    best_score = score
                    best_domain = domain
            return best_domain
        except Exception:
            return 'programming'


# Module-level singleton instance
bert_model = BERTModel()


def encode_text(text: str) -> List[float]:
    """Convenience function: encode a single text."""
    return bert_model.encode_single(text)


def classify_domain(text: str) -> str:
    """Convenience function: classify domain from text."""
    return bert_model.classify_domain(text)


def semantic_similarity(text1: str, text2: str) -> float:
    """Convenience function: compute semantic similarity between two texts."""
    emb1 = bert_model.encode_single(text1)
    emb2 = bert_model.encode_single(text2)
    return bert_model.cosine_similarity(emb1, emb2)
