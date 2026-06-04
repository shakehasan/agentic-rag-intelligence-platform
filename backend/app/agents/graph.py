from __future__ import annotations

import time
from typing import Any

from backend.app.agents.nodes.answer_generator import generate_answer
from backend.app.agents.nodes.compliance_guard import validate_citations
from backend.app.agents.nodes.escalation import escalate
from backend.app.agents.nodes.hallucination_guard import validate_grounding
from backend.app.agents.nodes.intent_classifier import classify_intent
from backend.app.agents.nodes.query_rewriter import rewrite_query
from backend.app.agents.nodes.retrieval_planner import plan_retrieval
from backend.app.agents.nodes.retriever import retrieve_context
from backend.app.agents.state import AgentState
from backend.app.schemas.chat import ChatResponse, TraceMetadata
from backend.app.services.langsmith import new_trace_id


def build_langgraph():
    """Build a LangGraph graph when the dependency is available.

    The production route uses the same node functions through a deterministic runner so tests and
    local demos do not depend on optional graph compilation behavior.
    """

    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return None

    graph = StateGraph(AgentState)
    graph.add_node("intent_classifier", classify_intent)
    graph.add_node("query_rewriter", rewrite_query)
    graph.add_node("retrieval_planner", plan_retrieval)
    graph.add_node("retriever", retrieve_context)
    graph.add_node("answer_generator", generate_answer)
    graph.add_node("hallucination_guard", validate_grounding)
    graph.add_node("compliance_guard", validate_citations)
    graph.add_node("escalation", escalate)

    graph.set_entry_point("intent_classifier")
    graph.add_conditional_edges(
        "intent_classifier",
        lambda state: "unsupported" if state.get("intent") == "unsupported" else "supported",
        {"unsupported": "escalation", "supported": "query_rewriter"},
    )
    graph.add_edge("query_rewriter", "retrieval_planner")
    graph.add_edge("retrieval_planner", "retriever")
    graph.add_conditional_edges(
        "retriever",
        lambda state: "low_confidence" if state.get("should_escalate") else "ready",
        {"low_confidence": "escalation", "ready": "answer_generator"},
    )
    graph.add_edge("answer_generator", "hallucination_guard")
    graph.add_conditional_edges(
        "hallucination_guard",
        lambda state: "failed" if state.get("should_escalate") else "passed",
        {"failed": "escalation", "passed": "compliance_guard"},
    )
    graph.add_conditional_edges(
        "compliance_guard",
        lambda state: "failed" if state.get("should_escalate") else "passed",
        {"failed": "escalation", "passed": END},
    )
    graph.add_edge("escalation", END)
    return graph.compile()


def run_agent(query: str, filters: dict[str, str] | None = None) -> ChatResponse:
    started = time.perf_counter()
    state: AgentState = {
        "query": query,
        "filters": filters or {},
        "trace_id": new_trace_id(),
        "error_messages": [],
        "should_escalate": False,
    }

    state = classify_intent(state)
    if state.get("intent") == "unsupported":
        state = escalate(state)
    else:
        for node in (
            rewrite_query,
            plan_retrieval,
            retrieve_context,
        ):
            state = node(state)
        if state.get("should_escalate"):
            state = escalate(state)
        else:
            for node in (
                generate_answer,
                validate_grounding,
            ):
                state = node(state)
            if state.get("should_escalate"):
                state = escalate(state)
            else:
                state = validate_citations(state)
                if state.get("should_escalate"):
                    state = escalate(state)

    state["latency_ms"] = round((time.perf_counter() - started) * 1000, 2)
    trace_metadata = TraceMetadata(
        query=query,
        intent=state.get("intent", "unsupported"),
        retrieval_strategy=state.get("retrieval_strategy", "none"),
        retrieved_document_count=len({item.source for item in state.get("retrieved_context", [])}),
        confidence_score=state.get("confidence_score", 0.0),
        guardrail_status=state.get("guardrail_status", "unknown"),
    )

    return ChatResponse(
        answer=state.get("answer", ""),
        citations=state.get("citations", []),
        retrieval_strategy=state.get("retrieval_strategy", "none"),
        confidence_score=state.get("confidence_score", 0.0),
        guardrail_status=state.get("guardrail_status", "unknown"),
        trace_id=state.get("trace_id", "demo-trace-unavailable"),
        trace_metadata=trace_metadata,
        retrieved_context=[_context_payload(item) for item in state.get("retrieved_context", [])],
    )


def _context_payload(item: Any) -> dict[str, Any]:
    return {
        "source": item.source,
        "chunk_id": item.chunk_id,
        "document_type": item.document_type,
        "score": item.score,
        "excerpt": item.excerpt,
    }

