from __future__ import annotations

from collections import Counter

from backend.app.schemas.documents import RetrievedChunk


def summarize_retrieval(results: list[RetrievedChunk]) -> dict[str, object]:
    if not results:
        return {
            "result_count": 0,
            "source_count": 0,
            "document_type_distribution": {},
            "average_score": 0.0,
            "top_source": None,
        }

    document_types = Counter(result.document_type for result in results)
    sources = Counter(result.source for result in results)
    average_score = sum(result.score for result in results) / len(results)
    return {
        "result_count": len(results),
        "source_count": len(sources),
        "document_type_distribution": dict(document_types),
        "average_score": round(average_score, 3),
        "top_source": results[0].source,
    }


def detect_retrieval_risks(results: list[RetrievedChunk], min_score: float = 0.3) -> list[str]:
    risks: list[str] = []
    if not results:
        return ["no_context_retrieved"]
    if results[0].score < min_score:
        risks.append("low_top_score")
    if len({result.source for result in results}) == 1 and len(results) > 2:
        risks.append("single_source_concentration")
    if not any(result.excerpt for result in results):
        risks.append("missing_excerpts")
    return risks

