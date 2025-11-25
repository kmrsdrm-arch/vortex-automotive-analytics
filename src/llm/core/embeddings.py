"""Embedding generation utilities."""

from typing import List
from src.llm.core.client import client
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """Generate embeddings for text."""

    def __init__(self):
        """Initialize embedding generator."""
        self.client = client

    def generate(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        try:
            return self.client.generate_embeddings(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = []
        for text in texts:
            try:
                embedding = self.generate(text)
                embeddings.append(embedding)
            except Exception as e:
                logger.error(f"Error generating embedding for text: {e}")
                embeddings.append([])  # Empty embedding on error

        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings

