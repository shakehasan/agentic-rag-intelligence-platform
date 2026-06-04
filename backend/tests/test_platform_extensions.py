from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.rag.query_expansion import build_expanded_query, expand_query_terms
from backend.app.rag.retrieval_diagnostics import detect_retrieval_risks, summarize_retrieval
from backend.app.schemas.documents import RetrievedChunk

client = TestClient(app)


def test_solution_catalog_endpoint() -> None:
    response = client.get("/solutions")

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_solutions"] >= 5
    assert payload["solutions"][0]["public_safe_note"]


def test_prompt_registry_endpoint() -> None:
    response = client.get("/prompts")

    assert response.status_code == 200
    payload = response.json()
    assert payload["active_version"]
    assert len(payload["templates"]) >= 3


def test_metrics_endpoint_records_chat_runs() -> None:
    client.post("/ingest", json={"reset_index": True})
    chat_response = client.post(
        "/chat",
        json={"query": "What are the release readiness requirements?"},
    )
    assert chat_response.status_code == 200

    metrics_response = client.get("/metrics")
    payload = metrics_response.json()

    assert metrics_response.status_code == 200
    assert payload["total_chat_runs"] >= 1
    assert payload["recent_runs"]


def test_feedback_endpoint_accepts_public_safe_signal() -> None:
    response = client.post(
        "/feedback",
        json={
            "trace_id": "demo-trace-feedback",
            "query": "What are the release readiness requirements?",
            "signal": "helpful",
            "notes": "Synthetic reviewer feedback.",
        },
    )

    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_query_expansion_adds_domain_terms() -> None:
    terms = expand_query_terms("How should privacy reviews work?")
    expanded = build_expanded_query("How should privacy reviews work?")

    assert "retention" in terms
    assert "minimization" in expanded


def test_retrieval_diagnostics_summarize_results() -> None:
    result = RetrievedChunk(
        source="release_readiness_checklist.md",
        chunk_id="release-readiness-checklist-001",
        document_type="release",
        score=0.82,
        excerpt="Release readiness requires tests and evaluation review.",
    )

    summary = summarize_retrieval([result])
    risks = detect_retrieval_risks([result])

    assert summary["result_count"] == 1
    assert summary["top_source"] == "release_readiness_checklist.md"
    assert risks == []

