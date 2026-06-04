# Operational Playbook

This playbook describes the public-safe operating model for the Agentic RAG Intelligence Platform.

## Local Quality Gates

Run these checks before publishing changes:

```bash
python scripts/public_safety_scan.py
ruff check .
pytest
python scripts/run_eval.py
```

The public safety scan verifies that unsafe terms are not introduced outside the dedicated safety statement. Ruff checks code quality, pytest validates ingestion and API behavior, and the evaluation script measures retrieval and grounded-response behavior on synthetic golden questions.

## Runtime Signals

The platform exposes lightweight runtime metrics through `/metrics`. The snapshot tracks chat run count, passed guardrail runs, escalated runs, average confidence score, average citation count, and recent trace metadata.

These metrics are intentionally simple for local use. In a deployed environment, the same signal shape can be exported to centralized monitoring and alerting.

## Feedback Loop

The `/feedback` endpoint captures reviewer signals for a trace id and query. Feedback is stored in memory for local demo runs and can be replaced with a durable store in a cloud deployment.

The feedback loop supports practical AI operations:

- Identify low-confidence answer patterns.
- Compare reviewer expectations with citations.
- Prioritize retrieval and prompt improvements.
- Build future evaluation datasets from reviewed traces.

## Prompt Registry

The `/prompts` endpoint exposes active prompt templates and guardrail notes. Keeping prompt purpose, version, and validation rules visible makes the workflow easier to review and debug.

## Release Checklist

Before presenting or publishing the repository:

- Run public safety scan.
- Run unit tests.
- Run lint checks.
- Run synthetic evaluation.
- Confirm README examples still match API behavior.
- Confirm commit attribution uses the intended GitHub account.

