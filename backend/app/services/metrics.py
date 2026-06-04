from __future__ import annotations

from collections import deque
from statistics import mean

from backend.app.schemas.chat import ChatResponse
from backend.app.schemas.metrics import ChatRunMetric, MetricsSnapshot


class MetricsRecorder:
    def __init__(self, max_items: int = 500) -> None:
        self.max_items = max_items
        self._runs: deque[ChatRunMetric] = deque()

    def record_chat_response(self, query: str, response: ChatResponse) -> ChatRunMetric:
        metadata = response.trace_metadata
        metric = ChatRunMetric(
            trace_id=response.trace_id,
            query=query,
            intent=metadata.intent if metadata else "unknown",
            retrieval_strategy=response.retrieval_strategy,
            confidence_score=response.confidence_score,
            guardrail_status=response.guardrail_status,
            citation_count=len(response.citations),
            retrieved_context_count=len(response.retrieved_context),
        )
        self._runs.append(metric)
        while len(self._runs) > self.max_items:
            self._runs.popleft()
        return metric

    def snapshot(self, recent_limit: int = 10) -> MetricsSnapshot:
        runs = list(self._runs)
        passed = [run for run in runs if run.guardrail_status == "passed"]
        escalated = [run for run in runs if run.guardrail_status == "escalated"]
        return MetricsSnapshot(
            total_chat_runs=len(runs),
            passed_guardrail_runs=len(passed),
            escalated_runs=len(escalated),
            average_confidence_score=_average([run.confidence_score for run in runs]),
            average_citation_count=_average([run.citation_count for run in runs]),
            recent_runs=runs[-recent_limit:],
        )


def _average(values: list[float | int]) -> float:
    if not values:
        return 0.0
    return round(mean(values), 3)


metrics_recorder = MetricsRecorder()

