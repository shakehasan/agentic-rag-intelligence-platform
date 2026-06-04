from backend.app.schemas.prompts import PromptRegistryResponse, PromptTemplateRecord

ACTIVE_PROMPT_VERSION = "rag-grounded-answer-v1"


PROMPT_TEMPLATES = [
    PromptTemplateRecord(
        prompt_id="intent-classifier",
        version="intent-classifier-v1",
        purpose="Classify the user request before retrieval planning.",
        template=(
            "Classify the query as factual_question, summarization, comparison, "
            "policy_question, technical_question, or unsupported."
        ),
        guardrail_notes=[
            "Unsupported requests route to the insufficient-context handler.",
            "Classification should not answer the user directly.",
        ],
    ),
    PromptTemplateRecord(
        prompt_id="rag-grounded-answer",
        version=ACTIVE_PROMPT_VERSION,
        purpose="Generate concise source-grounded answers from retrieved context.",
        template=(
            "Answer only from retrieved context. If context is insufficient, return the "
            "standard insufficient-context response. Never invent sources."
        ),
        guardrail_notes=[
            "Every substantive claim must be supported by retrieved context.",
            "Citations are built from retrieved chunk metadata only.",
        ],
    ),
    PromptTemplateRecord(
        prompt_id="hallucination-guard",
        version="hallucination-guard-v1",
        purpose="Validate that generated answer terms are supported by context.",
        template=(
            "Compare answer content against retrieved snippets and flag answers with low "
            "support ratio for escalation."
        ),
        guardrail_notes=[
            "Guardrail output controls routing, not user-facing prose.",
            "Failed checks produce an insufficient-context response.",
        ],
    ),
]


def get_prompt_registry() -> PromptRegistryResponse:
    return PromptRegistryResponse(
        active_version=ACTIVE_PROMPT_VERSION,
        templates=PROMPT_TEMPLATES,
    )

