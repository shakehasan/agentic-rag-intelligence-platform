from fastapi import APIRouter

from backend.app.agents.graph import run_agent
from backend.app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    filters = request.filters.model_dump(exclude_none=True) if request.filters else None
    return run_agent(request.query, filters=filters)

