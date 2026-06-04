from typing import Any, Literal

from pydantic import BaseModel, Field

IntentCategory = Literal[
    "factual_question",
    "summarization",
    "comparison",
    "policy_question",
    "technical_question",
    "unsupported",
]


class ChatFilters(BaseModel):
    document_type: str | None = None
    business_domain: str | None = None
    source: str | None = None


class ChatRequest(BaseModel):
    query: str = Field(min_length=2)
    filters: ChatFilters | None = None


class Citation(BaseModel):
    source: str
    chunk_id: str
    document_type: str
    confidence: float


class TraceMetadata(BaseModel):
    query: str
    intent: IntentCategory
    retrieval_strategy: str
    retrieved_document_count: int
    confidence_score: float
    guardrail_status: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieval_strategy: str
    confidence_score: float
    guardrail_status: str
    trace_id: str
    trace_metadata: TraceMetadata | None = None
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)

