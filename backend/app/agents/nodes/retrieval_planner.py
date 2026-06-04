from backend.app.agents.state import AgentState


def plan_retrieval(state: AgentState) -> AgentState:
    filters = dict(state.get("filters") or {})
    intent = state.get("intent")
    query = state["query"].lower()
    if intent == "policy_question" and "privacy" in query and not filters.get("document_type"):
        filters["document_type"] = "privacy"
    elif intent == "policy_question" and not filters.get("document_type"):
        filters["document_type"] = "policy"
    state["filters"] = {key: value for key, value in filters.items() if value}
    state["retrieval_strategy"] = "hybrid"
    return state
