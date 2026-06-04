from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_chat_endpoint_returns_citations() -> None:
    ingest = client.post("/ingest", json={"reset_index": True})
    assert ingest.status_code == 200

    response = client.post(
        "/chat",
        json={
            "query": "What does the AI governance policy say about human review?",
            "filters": {"document_type": "policy"},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["citations"]
    assert payload["citations"][0]["source"] == "ai_governance_policy.md"
    assert payload["guardrail_status"] == "passed"


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

