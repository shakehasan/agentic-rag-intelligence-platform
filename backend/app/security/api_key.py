from __future__ import annotations

from fastapi import Header, HTTPException, status

from backend.app.core.config import get_settings


async def require_optional_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Require an API key only when one is configured.

    This keeps local demo runs frictionless while showing the service boundary where API
    authentication would be enforced in a deployed environment.
    """

    settings = get_settings()
    expected = getattr(settings, "api_key", None)
    if not expected:
        return
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )
