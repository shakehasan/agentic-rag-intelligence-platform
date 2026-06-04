from __future__ import annotations

from statistics import mean
from typing import Any

from backend.app.schemas.evaluation import EvaluationMetrics


def compute_metrics(results: list[dict[str, Any]]) -> EvaluationMetrics:
    if not results:
        return EvaluationMetrics(
            retrieval_hit_rate=0.0,
            citation_coverage=0.0,
            answer_groundedness=0.0,
            unsupported_answer_rate=0.0,
            average_latency_ms=0.0,
        )

    answerable = [result for result in results if result["should_answer"]]
    unsupported = [result for result in results if not result["should_answer"]]

    retrieval_hits = [
        _has_expected_source(result["retrieved_sources"], result["expected_sources"])
        for result in answerable
    ]
    citation_hits = [
        _has_expected_source(result["citation_sources"], result["expected_sources"])
        for result in answerable
    ]
    grounded = [
        result["guardrail_status"] == "passed" and bool(result["citation_sources"])
        for result in answerable
    ]
    unsupported_refusals = [
        result["guardrail_status"] == "escalated" and not result["citation_sources"]
        for result in unsupported
    ]

    return EvaluationMetrics(
        retrieval_hit_rate=round(_ratio(retrieval_hits), 3),
        citation_coverage=round(_ratio(citation_hits), 3),
        answer_groundedness=round(_ratio(grounded), 3),
        unsupported_answer_rate=round(1 - _ratio(unsupported_refusals), 3),
        average_latency_ms=round(mean(result["latency_ms"] for result in results), 2),
    )


def _has_expected_source(actual: list[str], expected: list[str]) -> bool:
    if not expected:
        return True
    return any(source in actual for source in expected)


def _ratio(values: list[bool]) -> float:
    if not values:
        return 0.0
    return sum(1 for value in values if value) / len(values)

