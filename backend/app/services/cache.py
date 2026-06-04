from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from backend.app.core.config import Settings, get_settings
from backend.app.rag.hybrid_retriever import HybridRetriever, build_retriever_from_path
from backend.app.schemas.documents import DocumentSummary


@dataclass
class RAGIndex:
    retriever: HybridRetriever
    indexed_documents: int
    indexed_chunks: int
    sources: list[str]
    loaded_at: datetime


_INDEX: RAGIndex | None = None


def get_index(settings: Settings | None = None) -> RAGIndex:
    global _INDEX
    settings = settings or get_settings()
    if _INDEX is None:
        retriever = HybridRetriever.load_or_build(settings)
        chunks = retriever.all_chunks()
        sources = sorted({chunk.source for chunk in chunks})
        _INDEX = RAGIndex(
            retriever=retriever,
            indexed_documents=len(sources),
            indexed_chunks=len(chunks),
            sources=sources,
            loaded_at=datetime.now(UTC),
        )
    return _INDEX


def rebuild_index(path: Path, settings: Settings | None = None) -> RAGIndex:
    global _INDEX
    settings = settings or get_settings()
    retriever, document_count, chunk_count, sources = build_retriever_from_path(path, settings)
    _INDEX = RAGIndex(
        retriever=retriever,
        indexed_documents=document_count,
        indexed_chunks=chunk_count,
        sources=sources,
        loaded_at=datetime.now(UTC),
    )
    return _INDEX


def document_summaries(settings: Settings | None = None) -> list[DocumentSummary]:
    index = get_index(settings)
    grouped: dict[str, dict] = {}
    for chunk in index.retriever.all_chunks():
        item = grouped.setdefault(
            chunk.document_id,
            {
                "document_id": chunk.document_id,
                "source": chunk.source,
                "title": chunk.title,
                "document_type": chunk.document_type,
                "business_domain": chunk.business_domain,
                "sensitivity_level": chunk.sensitivity_level,
                "created_at": chunk.created_at,
                "chunk_count": 0,
            },
        )
        item["chunk_count"] += 1
    return [
        DocumentSummary(**item)
        for item in sorted(grouped.values(), key=lambda row: row["source"])
    ]
