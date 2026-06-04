from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    document_id: str
    source: str
    title: str
    document_type: str
    business_domain: str
    sensitivity_level: str
    created_at: datetime


class DocumentChunk(DocumentMetadata):
    chunk_id: str
    content: str


class IngestRequest(BaseModel):
    path: str | None = Field(
        default=None,
        description="Optional path to a document file or directory. Defaults to synthetic docs.",
    )
    reset_index: bool = True


class IngestResponse(BaseModel):
    indexed_documents: int
    indexed_chunks: int
    sources: list[str]


class DocumentSummary(BaseModel):
    document_id: str
    source: str
    title: str
    document_type: str
    business_domain: str
    sensitivity_level: str
    created_at: datetime
    chunk_count: int


class RetrievedChunk(BaseModel):
    source: str
    chunk_id: str
    document_type: str
    score: float
    excerpt: str
    title: str | None = None
    business_domain: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

