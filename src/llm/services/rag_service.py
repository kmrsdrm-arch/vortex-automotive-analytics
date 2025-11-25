"""RAG (Retrieval-Augmented Generation) service."""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from src.llm.core.client import client
from src.llm.core.embeddings import EmbeddingGenerator
from src.database.models import InsightHistory
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RAGService:
    """Retrieval-Augmented Generation service."""

    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
        self.client = client
        self.embedding_generator = EmbeddingGenerator()

    def retrieve_similar_insights(
        self, query: str, limit: int = 5, insight_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve insights similar to query (simple keyword-based for now)."""
        try:
            # In a full RAG implementation, we'd use vector similarity
            # For now, using simple keyword matching

            query_lower = query.lower()
            keywords = query_lower.split()

            # Query insights from database
            insights_query = self.db.query(InsightHistory)

            if insight_type:
                insights_query = insights_query.filter(InsightHistory.insight_type == insight_type)

            insights = insights_query.order_by(InsightHistory.generated_at.desc()).limit(100).all()

            # Score insights based on keyword matches
            scored_insights = []
            for insight in insights:
                text_lower = insight.insight_text.lower()
                score = sum(1 for keyword in keywords if keyword in text_lower)

                if score > 0:
                    scored_insights.append(
                        {
                            "id": insight.id,
                            "text": insight.insight_text,
                            "type": insight.insight_type,
                            "generated_at": insight.generated_at.isoformat(),
                            "score": score,
                        }
                    )

            # Sort by score and return top results
            scored_insights.sort(key=lambda x: x["score"], reverse=True)
            similar = scored_insights[:limit]

            logger.info(f"Retrieved {len(similar)} similar insights for query: {query}")
            return similar

        except Exception as e:
            logger.error(f"Error retrieving similar insights: {e}")
            return []

    def answer_with_context(self, question: str, context_limit: int = 3) -> Dict[str, Any]:
        """Answer question using retrieved context."""
        try:
            # Retrieve relevant insights
            similar_insights = self.retrieve_similar_insights(question, limit=context_limit)

            # Build context
            context = "\n\n".join([f"- {ins['text']}" for ins in similar_insights])

            if not context:
                context = "No relevant historical insights found."

            # Generate answer with context
            prompt = f"""Answer the following question about automotive analytics:

Question: {question}

Relevant Historical Insights:
{context}

Provide a comprehensive answer based on the question and any relevant insights."""

            system_prompt = "You are an automotive analytics expert. Use the provided historical insights to inform your answers, but also apply your general knowledge about automotive sales and inventory analytics."

            answer = self.client.structured_completion(system_prompt, prompt, temperature=0.7)

            response = {
                "question": question,
                "answer": answer,
                "context_used": similar_insights,
                "context_count": len(similar_insights),
            }

            logger.info(f"Generated RAG answer with {len(similar_insights)} context items")
            return response

        except Exception as e:
            logger.error(f"Error generating RAG answer: {e}")
            raise

