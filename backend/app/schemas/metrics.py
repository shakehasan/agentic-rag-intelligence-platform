from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ChatRunMetric(BaseModel):
    trace_id: str
    query: str
    intent: str
    retrieval_strategy: str
    confidence_score: float
    guardrail_status: str
    citation_count: int
    retrieved_context_count: int
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MetricsSnapshot(BaseModel):
    total_chat_runs: int
    passed_guardrail_runs: int
    escalated_runs: int
    average_confidence_score: float
    average_citation_count: float
    recent_runs: list[ChatRunMetric]

