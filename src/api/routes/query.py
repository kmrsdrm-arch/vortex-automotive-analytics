"""Natural language query endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.api.schemas.requests import NLQueryRequest, RAGQueryRequest
from src.api.schemas.responses import NLQueryResponse
from src.llm.services.nl_query_service import NLQueryService
from src.llm.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1/query", tags=["Query"])


@router.post("", response_model=NLQueryResponse)
async def natural_language_query(request: NLQueryRequest, db: Session = Depends(get_db)):
    """Process natural language query."""
    service = NLQueryService(db)
    result = service.process_query(request.question)
    return NLQueryResponse(**result)


@router.post("/rag")
async def rag_query(request: RAGQueryRequest, db: Session = Depends(get_db)):
    """Answer question using RAG (Retrieval-Augmented Generation)."""
    service = RAGService(db)
    return service.answer_with_context(request.question, request.context_limit)

