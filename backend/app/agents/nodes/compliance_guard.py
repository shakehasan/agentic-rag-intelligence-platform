from backend.app.agents.state import AgentState


def validate_citations(state: AgentState) -> AgentState:
    if state.get("should_escalate"):
        return state

    retrieved_ids = {context.chunk_id for context in state.get("retrieved_context", [])}
    citation_ids = {citation.chunk_id for citation in state.get("citations", [])}
    if not citation_ids or not citation_ids.issubset(retrieved_ids):
        state["guardrail_status"] = "failed"
        state["should_escalate"] = True
        state.setdefault("error_messages", []).append(
            "Citation set does not match retrieved context."
        )
    else:
        state["guardrail_status"] = "passed"
    return state
