from pydantic import BaseModel


class PromptTemplateRecord(BaseModel):
    prompt_id: str
    version: str
    purpose: str
    template: str
    guardrail_notes: list[str]


class PromptRegistryResponse(BaseModel):
    active_version: str
    templates: list[PromptTemplateRecord]

