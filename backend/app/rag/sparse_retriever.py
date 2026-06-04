from __future__ import annotations

import math
from collections import Counter

from backend.app.schemas.documents import DocumentChunk, RetrievedChunk

from .embeddings import tokenize
from .vector_store import _excerpt, _matches_filters


class BM25SparseRetriever:
    def __init__(self, chunks: list[DocumentChunk] | None = None, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.chunks: list[DocumentChunk] = []
        self.doc_tokens: list[list[str]] = []
        self.term_frequencies: list[Counter[str]] = []
        self.document_frequencies: Counter[str] = Counter()
        self.average_length = 0.0
        if chunks:
            self.build(chunks)

    def build(self, chunks: list[DocumentChunk]) -> None:
        self.chunks = chunks
        self.doc_tokens = [tokenize(chunk.content) for chunk in chunks]
        self.term_frequencies = [Counter(tokens) for tokens in self.doc_tokens]
        self.document_frequencies = Counter()
        for tokens in self.doc_tokens:
            self.document_frequencies.update(set(tokens))
        self.average_length = (
            sum(len(tokens) for tokens in self.doc_tokens) / max(len(self.doc_tokens), 1)
        )

    def search(
        self,
        query: str,
        top_k: int,
        filters: dict[str, str] | None = None,
    ) -> list[RetrievedChunk]:
        filters = filters or {}
        query_terms = tokenize(query)
        raw_scores: list[tuple[float, DocumentChunk]] = []
        total_docs = max(len(self.chunks), 1)

        for index, chunk in enumerate(self.chunks):
            if not _matches_filters(chunk, filters):
                continue
            length = max(len(self.doc_tokens[index]), 1)
            score = 0.0
            for term in query_terms:
                tf = self.term_frequencies[index].get(term, 0)
                if tf == 0:
                    continue
                df = self.document_frequencies.get(term, 0)
                idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
                denominator = tf + self.k1 * (1 - self.b + self.b * length / self.average_length)
                score += idf * (tf * (self.k1 + 1)) / denominator
            raw_scores.append((score, chunk))

        raw_scores.sort(key=lambda item: item[0], reverse=True)
        max_score = raw_scores[0][0] if raw_scores else 0.0
        results: list[RetrievedChunk] = []
        for score, chunk in raw_scores[:top_k]:
            if score <= 0:
                continue
            normalized = score / max_score if max_score else 0.0
            results.append(
                RetrievedChunk(
                    source=chunk.source,
                    chunk_id=chunk.chunk_id,
                    document_type=chunk.document_type,
                    score=round(normalized, 4),
                    excerpt=_excerpt(chunk.content),
                    title=chunk.title,
                    business_domain=chunk.business_domain,
                    metadata=chunk.model_dump(mode="json"),
                )
            )
        return results

