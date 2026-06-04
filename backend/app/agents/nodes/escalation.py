from backend.app.agents.state import AgentState
from backend.app.services.llm_provider import INSUFFICIENT_CONTEXT_MESSAGE


def escalate(state: AgentState) -> AgentState:
    state["answer"] = INSUFFICIENT_CONTEXT_MESSAGE
    state["citations"] = []
    state["confidence_score"] = 0.0
    state["guardrail_status"] = "escalated"
    state["should_escalate"] = True
    return state

