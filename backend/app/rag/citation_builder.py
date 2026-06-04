from backend.app.schemas.chat import Citation
from backend.app.schemas.documents import RetrievedChunk


def build_citations(results: list[RetrievedChunk], limit: int = 4) -> list[Citation]:
    citations: list[Citation] = []
    seen: set[str] = set()
    for result in results:
        if result.chunk_id in seen:
            continue
        seen.add(result.chunk_id)
        citations.append(
            Citation(
                source=result.source,
                chunk_id=result.chunk_id,
                document_type=result.document_type,
                confidence=round(result.score, 2),
            )
        )
        if len(citations) >= limit:
            break
    return citations

