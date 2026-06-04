import re

from backend.app.agents.state import AgentState
from backend.app.services.llm_provider import INSUFFICIENT_CONTEXT_MESSAGE


def validate_grounding(state: AgentState) -> AgentState:
    answer = state.get("answer", "")
    contexts = state.get("retrieved_context", [])
    if answer == INSUFFICIENT_CONTEXT_MESSAGE:
        state["guardrail_status"] = "insufficient_context"
        state["should_escalate"] = True
        return state

    if not answer or not contexts or not state.get("citations"):
        state["guardrail_status"] = "failed"
        state["should_escalate"] = True
        state.setdefault("error_messages", []).append("Answer lacks retrieved support.")
        return state

    context_text = " ".join(
        str(context.metadata.get("content") or context.excerpt).lower() for context in contexts
    )
    answer_terms = {
        token.lower()
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", answer)
        if len(token) > 4
    }
    if not answer_terms:
        state["guardrail_status"] = "failed"
        state["should_escalate"] = True
        return state

    supported_terms = {term for term in answer_terms if term in context_text}
    support_ratio = len(supported_terms) / len(answer_terms)
    if support_ratio < 0.55:
        state["guardrail_status"] = "failed"
        state["should_escalate"] = True
        state.setdefault("error_messages", []).append("Answer support ratio below threshold.")
    else:
        state["guardrail_status"] = "passed"
    return state

