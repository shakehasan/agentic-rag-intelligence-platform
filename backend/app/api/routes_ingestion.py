from pathlib import Path

from fastapi import APIRouter

from backend.app.core.config import get_settings
from backend.app.schemas.documents import IngestRequest, IngestResponse
from backend.app.services.cache import rebuild_index

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    settings = get_settings()
    path = Path(request.path) if request.path else settings.synthetic_docs_dir
    index = rebuild_index(path, settings)
    return IngestResponse(
        indexed_documents=index.indexed_documents,
        indexed_chunks=index.indexed_chunks,
        sources=index.sources,
    )

