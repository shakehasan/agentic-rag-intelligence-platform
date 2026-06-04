from backend.app.agents.state import AgentState
from backend.app.core.config import get_settings
from backend.app.services.cache import get_index


def retrieve_context(state: AgentState) -> AgentState:
    settings = get_settings()
    index = get_index(settings)
    strategy = state.get("retrieval_strategy", "hybrid")
    results = index.retriever.retrieve(
        state.get("rewritten_query") or state["query"],
        top_k=settings.retrieval_top_k,
        filters=state.get("filters"),
        strategy=strategy,
    )
    state["retrieved_context"] = results

    if not results:
        state["confidence_score"] = 0.0
        state["should_escalate"] = True
        state.setdefault("error_messages", []).append("No relevant context retrieved.")
        return state

    confidence = sum(result.score for result in results[:3]) / min(len(results), 3)
    state["confidence_score"] = round(confidence, 2)
    if confidence < settings.min_confidence:
        state["should_escalate"] = True
        state.setdefault("error_messages", []).append("Retrieval confidence below threshold.")
    return state

