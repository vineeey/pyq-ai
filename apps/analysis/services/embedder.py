"""
Embedding generation service using sentence-transformers.
"""
import logging
from typing import List, Optional
import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Generates embeddings using sentence-transformers."""
    
    _model = None
    _model_name = None
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
    
    def _load_model(self):
        """Lazy load the embedding model."""
        if EmbeddingService._model is None or EmbeddingService._model_name != self.model_name:
            try:
                from sentence_transformers import SentenceTransformer
                EmbeddingService._model = SentenceTransformer(self.model_name)
                EmbeddingService._model_name = self.model_name
                logger.info(f"Loaded embedding model: {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text.
        
        Returns:
            List of floats representing the embedding, or None on failure
        """
        try:
            self._load_model()
            embedding = EmbeddingService._model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None
    
    def get_embeddings_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts.
        """
        try:
            self._load_model()
            embeddings = EmbeddingService._model.encode(texts, convert_to_numpy=True)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {e}")
            return [None] * len(texts)
