from fastapi import APIRouter

from backend.app.schemas.metrics import MetricsSnapshot
from backend.app.services.metrics import metrics_recorder

router = APIRouter()


@router.get("/metrics", response_model=MetricsSnapshot)
def metrics() -> MetricsSnapshot:
    return metrics_recorder.snapshot()

