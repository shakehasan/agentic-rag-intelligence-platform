from backend.app.agents.state import AgentState
from backend.app.rag.citation_builder import build_citations
from backend.app.services.llm_provider import GroundedLLMProvider


def generate_answer(state: AgentState) -> AgentState:
    provider = GroundedLLMProvider()
    contexts = state.get("retrieved_context", [])
    generated = provider.generate_grounded_answer(
        query=state["query"],
        contexts=contexts,
        intent=state.get("intent", "factual_question"),
    )
    state["answer"] = generated.answer
    state["citations"] = build_citations(contexts)
    state["confidence_score"] = round(
        min(generated.confidence, state.get("confidence_score", generated.confidence)),
        2,
    )
    return state

