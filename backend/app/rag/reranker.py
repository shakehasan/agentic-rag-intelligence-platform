from backend.app.schemas.documents import RetrievedChunk


class Reranker:
    """Extension point for cross-encoder or hosted reranking models."""

    def rerank(self, query: str, results: list[RetrievedChunk]) -> list[RetrievedChunk]:
        _ = query
        return results

