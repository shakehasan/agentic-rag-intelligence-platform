from __future__ import annotations

import os
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from backend.app.core.config import Settings


def configure_langsmith(settings: Settings) -> bool:
    """Enable LangSmith-compatible environment variables when a key is provided."""

    if not settings.langchain_api_key:
        return False

    os.environ.setdefault("LANGCHAIN_TRACING_V2", str(settings.langchain_tracing_v2).lower())
    os.environ.setdefault("LANGCHAIN_API_KEY", settings.langchain_api_key)
    os.environ.setdefault("LANGCHAIN_PROJECT", settings.langchain_project)
    return True


def new_trace_id() -> str:
    return f"demo-trace-{uuid.uuid4().hex[:12]}"


@contextmanager
def trace_run(name: str, metadata: dict[str, Any] | None = None) -> Iterator[str]:
    """Small trace wrapper that can be replaced by LangSmith traceable decorators.

    The app stays fully functional without a LangSmith key. When LangSmith variables are present,
    LangChain/LangGraph calls can be traced by the installed libraries.
    """

    _ = name, metadata
    trace_id = new_trace_id()
    yield trace_id
