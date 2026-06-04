from backend.app.agents.state import AgentState
from backend.app.schemas.chat import IntentCategory

UNSUPPORTED_TERMS = {
    "weather",
    "stock",
    "sports",
    "medical",
    "legal",
    "password",
    "personal",
    "contact",
    "salary",
}


def classify_intent(state: AgentState) -> AgentState:
    query = state["query"].lower()
    if any(term in query for term in UNSUPPORTED_TERMS):
        intent: IntentCategory = "unsupported"
    elif any(term in query for term in {"compare", "difference", "versus", "vs"}):
        intent = "comparison"
    elif any(term in query for term in {"summarize", "summary", "overview"}):
        intent = "summarization"
    elif any(term in query for term in {"policy", "governance", "privacy"}):
        intent = "policy_question"
    elif any(
        term in query for term in {"architecture", "deployment", "api", "service", "security"}
    ):
        intent = "technical_question"
    else:
        intent = "factual_question"
    state["intent"] = intent
    return state
