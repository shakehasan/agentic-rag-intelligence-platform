from fastapi import APIRouter

from backend.app.agents.graph import run_agent
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.metrics import metrics_recorder

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    filters = request.filters.model_dump(exclude_none=True) if request.filters else None
    response = run_agent(request.query, filters=filters)
    metrics_recorder.record_chat_response(request.query, response)
    return response
