from backend.app.agents.state import AgentState


def rewrite_query(state: AgentState) -> AgentState:
    query = " ".join(state["query"].split())
    if len(query.split()) <= 3 and state.get("intent") != "unsupported":
        query = f"{query} in the Northstar Labs synthetic knowledge documents"
    state["rewritten_query"] = query
    return state

