from fastapi import APIRouter, Depends

from backend.app.schemas.feedback import FeedbackRequest, FeedbackResponse
from backend.app.security.api_key import require_optional_api_key
from backend.app.services.feedback import feedback_store

router = APIRouter()


@router.post(
    "/feedback",
    response_model=FeedbackResponse,
    dependencies=[Depends(require_optional_api_key)],
)
def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    record = feedback_store.add(request)
    return FeedbackResponse(
        accepted=True,
        total_feedback_items=feedback_store.count(),
        record=record,
    )
