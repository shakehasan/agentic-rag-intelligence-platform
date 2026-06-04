from collections import deque

from backend.app.core.config import get_settings
from backend.app.schemas.feedback import FeedbackRecord, FeedbackRequest


class FeedbackStore:
    def __init__(self) -> None:
        self._items: deque[FeedbackRecord] = deque()

    def add(self, request: FeedbackRequest) -> FeedbackRecord:
        settings = get_settings()
        record = FeedbackRecord(**request.model_dump())
        self._items.append(record)
        while len(self._items) > settings.max_feedback_items:
            self._items.popleft()
        return record

    def list_recent(self, limit: int = 50) -> list[FeedbackRecord]:
        return list(self._items)[-limit:]

    def count(self) -> int:
        return len(self._items)


feedback_store = FeedbackStore()

