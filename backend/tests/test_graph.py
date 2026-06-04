from backend.app.agents.graph import run_agent
from backend.app.agents.nodes.hallucination_guard import validate_grounding
from backend.app.agents.state import AgentState


def test_unsupported_queries_route_to_escalation() -> None:
    response = run_agent("What is the weather today?")

    assert response.guardrail_status == "escalated"
    assert response.citations == []
    assert "not have enough context" in response.answer


def test_guardrail_blocks_unsupported_answer() -> None:
    state: AgentState = {
        "query": "Explain deployment approvals.",
        "answer": "Deployment approval is automatic for every service.",
        "retrieved_context": [],
        "citations": [],
        "should_escalate": False,
    }

    result = validate_grounding(state)

    assert result["should_escalate"] is True
    assert result["guardrail_status"] == "failed"

