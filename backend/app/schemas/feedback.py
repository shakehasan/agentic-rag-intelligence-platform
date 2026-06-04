from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

FeedbackSignal = Literal["helpful", "partially_helpful", "not_helpful", "unsafe_or_unsupported"]


class FeedbackRequest(BaseModel):
    trace_id: str = Field(min_length=3)
    query: str = Field(min_length=2)
    signal: FeedbackSignal
    notes: str | None = Field(default=None, max_length=1000)
    expected_source: str | None = None


class FeedbackRecord(FeedbackRequest):
    recorded_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class FeedbackResponse(BaseModel):
    accepted: bool
    total_feedback_items: int
    record: FeedbackRecord

