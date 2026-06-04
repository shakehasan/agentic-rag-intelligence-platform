from typing import TypedDict

from backend.app.schemas.chat import Citation, IntentCategory, TraceMetadata
from backend.app.schemas.documents import RetrievedChunk


class AgentState(TypedDict, total=False):
    query: str
    filters: dict[str, str]
    intent: IntentCategory
    rewritten_query: str
    retrieval_strategy: str
    retrieved_context: list[RetrievedChunk]
    answer: str
    citations: list[Citation]
    confidence_score: float
    guardrail_status: str
    trace_id: str
    trace_metadata: TraceMetadata
    should_escalate: bool
    error_messages: list[str]
    latency_ms: float
