from __future__ import annotations

from pathlib import Path

from backend.app.core.config import Settings
from backend.app.schemas.documents import DocumentChunk, RetrievedChunk

from .chunking import chunk_documents
from .loaders import load_documents
from .sparse_retriever import BM25SparseRetriever
from .vector_store import LocalVectorStore


class HybridRetriever:
    def __init__(
        self,
        vector_store: LocalVectorStore,
        sparse_retriever: BM25SparseRetriever,
        dense_weight: float = 0.55,
        sparse_weight: float = 0.45,
        rrf_k: int = 60,
    ) -> None:
        self.vector_store = vector_store
        self.sparse_retriever = sparse_retriever
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight
        self.rrf_k = rrf_k

    @classmethod
    def from_chunks(
        cls,
        chunks: list[DocumentChunk],
        settings: Settings,
        persist: bool = True,
    ) -> HybridRetriever:
        vector_store = LocalVectorStore(settings.vector_index_dir)
        vector_store.reset()
        vector_store.add_chunks(chunks)
        if persist:
            vector_store.persist()
        sparse = BM25SparseRetriever(chunks)
        return cls(
            vector_store=vector_store,
            sparse_retriever=sparse,
            dense_weight=settings.hybrid_dense_weight,
            sparse_weight=settings.hybrid_sparse_weight,
        )

    @classmethod
    def load_or_build(cls, settings: Settings, docs_path: Path | None = None) -> HybridRetriever:
        vector_store = LocalVectorStore(settings.vector_index_dir)
        if vector_store.load():
            chunks = vector_store.chunks()
            return cls(
                vector_store=vector_store,
                sparse_retriever=BM25SparseRetriever(chunks),
                dense_weight=settings.hybrid_dense_weight,
                sparse_weight=settings.hybrid_sparse_weight,
            )
        docs_path = docs_path or settings.synthetic_docs_dir
        raw_documents = load_documents(docs_path)
        chunks = chunk_documents(raw_documents, settings.chunk_size, settings.chunk_overlap)
        return cls.from_chunks(chunks, settings)

    def retrieve(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
        strategy: str = "hybrid",
    ) -> list[RetrievedChunk]:
        if strategy == "dense":
            return self.vector_store.similarity_search(query, top_k=top_k, filters=filters)
        if strategy == "sparse":
            return self.sparse_retriever.search(query, top_k=top_k, filters=filters)

        dense_results = self.vector_store.similarity_search(query, top_k=top_k * 2, filters=filters)
        sparse_results = self.sparse_retriever.search(query, top_k=top_k * 2, filters=filters)
        fused = self._reciprocal_rank_fusion(dense_results, sparse_results)
        return fused[:top_k]

    def all_chunks(self) -> list[DocumentChunk]:
        return self.vector_store.chunks()

    def _reciprocal_rank_fusion(
        self,
        dense_results: list[RetrievedChunk],
        sparse_results: list[RetrievedChunk],
    ) -> list[RetrievedChunk]:
        scores: dict[str, float] = {}
        result_map: dict[str, RetrievedChunk] = {}

        for weight, results in (
            (self.dense_weight, dense_results),
            (self.sparse_weight, sparse_results),
        ):
            for rank, result in enumerate(results, start=1):
                scores[result.chunk_id] = scores.get(result.chunk_id, 0.0) + weight / (
                    self.rrf_k + rank
                )
                existing = result_map.get(result.chunk_id)
                if existing is None or result.score > existing.score:
                    result_map[result.chunk_id] = result

        max_score = max(scores.values(), default=1.0)
        fused: list[RetrievedChunk] = []
        for chunk_id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
            result = result_map[chunk_id].model_copy()
            result.score = round(score / max_score, 4)
            fused.append(result)
        return fused


def build_retriever_from_path(
    path: Path,
    settings: Settings,
) -> tuple[HybridRetriever, int, int, list[str]]:
    raw_documents = load_documents(path)
    chunks = chunk_documents(raw_documents, settings.chunk_size, settings.chunk_overlap)
    retriever = HybridRetriever.from_chunks(chunks, settings=settings, persist=True)
    sources = sorted({document.metadata.source for document in raw_documents})
    return retriever, len(raw_documents), len(chunks), sources
