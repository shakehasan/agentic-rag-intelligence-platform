from fastapi import APIRouter

from backend.app.schemas.documents import DocumentSummary
from backend.app.services.cache import document_summaries

router = APIRouter()


@router.get("/documents", response_model=list[DocumentSummary])
def list_documents() -> list[DocumentSummary]:
    return document_summaries()

