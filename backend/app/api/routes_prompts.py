from fastapi import APIRouter

from backend.app.schemas.prompts import PromptRegistryResponse
from backend.app.services.prompt_registry import get_prompt_registry

router = APIRouter()


@router.get("/prompts", response_model=PromptRegistryResponse)
def prompts() -> PromptRegistryResponse:
    return get_prompt_registry()

