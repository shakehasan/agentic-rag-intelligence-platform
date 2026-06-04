from backend.app.agents.state import AgentState
from backend.app.rag.query_expansion import build_expanded_query


def rewrite_query(state: AgentState) -> AgentState:
    query = " ".join(state["query"].split())
    if len(query.split()) <= 3 and state.get("intent") != "unsupported":
        query = f"{query} in the synthetic knowledge documents"
    state["rewritten_query"] = build_expanded_query(query)
    return state
