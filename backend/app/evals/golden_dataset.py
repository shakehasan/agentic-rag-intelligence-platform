from backend.app.schemas.evaluation import GoldenQuestion

GOLDEN_QUESTIONS: list[GoldenQuestion] = [
    GoldenQuestion(
        question="What does the AI governance policy say about human review?",
        expected_sources=["ai_governance_policy.md"],
        filters={"document_type": "policy"},
    ),
    GoldenQuestion(
        question="Summarize the QA automation strategy.",
        expected_sources=["qa_automation_strategy.md"],
    ),
    GoldenQuestion(
        question="What are the release readiness requirements?",
        expected_sources=["release_readiness_checklist.md"],
    ),
    GoldenQuestion(
        question="Compare the cloud deployment checklist and security review checklist.",
        expected_sources=["cloud_deployment_standard.md", "security_review_checklist.md"],
    ),
    GoldenQuestion(
        question="How should product teams handle privacy reviews?",
        expected_sources=["data_privacy_guideline.md"],
    ),
    GoldenQuestion(
        question="What is the weather today?",
        expected_sources=[],
        should_answer=False,
    ),
]
