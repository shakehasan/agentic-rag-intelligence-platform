from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.app.schemas.documents import DocumentChunk, RetrievedChunk

from .embeddings import HashingEmbeddingModel, cosine_similarity


class LocalVectorStore:
    """Small persistent vector store used for local demo runs.

    The code path is intentionally simple and deterministic. The project is configured so this
    class can be swapped for Chroma or Qdrant in a deployed environment.
    """

    def __init__(
        self,
        index_dir: Path,
        embedding_model: HashingEmbeddingModel | None = None,
    ) -> None:
        self.index_dir = index_dir
        self.index_path = index_dir / "local_vectors.json"
        self.embedding_model = embedding_model or HashingEmbeddingModel()
        self.entries: list[dict[str, Any]] = []

    def reset(self) -> None:
        self.entries = []
        if self.index_path.exists():
            self.index_path.unlink()

    def add_chunks(self, chunks: list[DocumentChunk]) -> None:
        vectors = self.embedding_model.embed_documents(chunk.content for chunk in chunks)
        self.entries = [
            {
                "chunk": chunk.model_dump(mode="json"),
                "vector": vector,
            }
            for chunk, vector in zip(chunks, vectors, strict=True)
        ]

    def persist(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")

    def load(self) -> bool:
        if not self.index_path.exists():
            return False
        self.entries = json.loads(self.index_path.read_text(encoding="utf-8"))
        return True

    def chunks(self) -> list[DocumentChunk]:
        return [DocumentChunk(**entry["chunk"]) for entry in self.entries]

    def similarity_search(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
    ) -> list[RetrievedChunk]:
        filters = filters or {}
        query_vector = self.embedding_model.embed_query(query)
        scored: list[tuple[float, DocumentChunk]] = []
        for entry in self.entries:
            chunk = DocumentChunk(**entry["chunk"])
            if not _matches_filters(chunk, filters):
                continue
            score = max(0.0, cosine_similarity(query_vector, entry["vector"]))
            scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [
            RetrievedChunk(
                source=chunk.source,
                chunk_id=chunk.chunk_id,
                document_type=chunk.document_type,
                score=round(score, 4),
                excerpt=_excerpt(chunk.content),
                title=chunk.title,
                business_domain=chunk.business_domain,
                metadata=chunk.model_dump(mode="json"),
            )
            for score, chunk in scored[:top_k]
            if score > 0
        ]


def _matches_filters(chunk: DocumentChunk, filters: dict[str, str]) -> bool:
    for key, value in filters.items():
        if not value:
            continue
        if getattr(chunk, key, None) != value:
            return False
    return True


def _excerpt(text: str, limit: int = 420) -> str:
    compact = " ".join(text.split())
    return compact if len(compact) <= limit else f"{compact[: limit - 3]}..."
