# Evaluation Strategy

The evaluation module uses a small synthetic golden dataset to exercise policy, quality, release, cloud, security, privacy, and unsupported-question scenarios.

Metrics:

- retrieval hit rate
- citation coverage
- answer groundedness
- unsupported answer rate
- average latency in milliseconds

This is intentionally lightweight, but it demonstrates the core operating loop for an AI service: define expected behavior, run repeatable checks, inspect failures, and improve retrieval, prompts, or guardrails based on measurable outcomes.

