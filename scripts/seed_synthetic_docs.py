from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "data" / "synthetic_docs"


DOCUMENTS = {
    "ai_governance_policy.md": """---
document_id: ai-governance-policy
title: AI Governance Policy
document_type: policy
business_domain: responsible-ai
sensitivity_level: synthetic-demo
created_at: 2026-01-12T00:00:00Z
---
# AI Governance Policy

Northstar Labs uses this synthetic policy to define responsible AI review practices.
High-impact AI decisions require documented human review before release. Teams must record
the intended use, user impact, model limitations, evaluation results, and rollback owner.

AI assistants must answer from approved indexed sources. If retrieved context does not support
an answer, the assistant must say it does not have enough context in the indexed documents.

Model changes require version notes, evaluation checks, prompt review, and trace sampling.
""",
    "platform_architecture_note.md": """---
document_id: platform-architecture-note
title: Platform Architecture Note
document_type: architecture
business_domain: platform-engineering
sensitivity_level: synthetic-demo
created_at: 2026-01-18T00:00:00Z
---
# Platform Architecture Note

The Knowledge Intelligence Assistant is modeled as a FastAPI service with a graph workflow.
The workflow separates intent classification, query rewriting, retrieval planning, hybrid
retrieval, answer synthesis, and guardrail checks.

The service stores embeddings in a local vector index for demo runs. A managed vector database
can replace the local store through the retrieval interface. Observability metadata includes
intent, retrieval strategy, document count, confidence score, and guardrail status.
""",
    "qa_automation_strategy.md": """---
document_id: qa-automation-strategy
title: QA Automation Strategy
document_type: quality
business_domain: engineering-quality
sensitivity_level: synthetic-demo
created_at: 2026-01-20T00:00:00Z
---
# QA Automation Strategy

The QA automation strategy emphasizes contract tests, retrieval regression tests, API smoke
tests, and evaluation checks for grounded answers. Every release candidate should run ingestion
tests, hybrid retrieval tests, unsupported-query tests, and citation validation.

Test data must remain synthetic. Golden questions should cover policy, architecture, support,
security, privacy, release, and deployment scenarios. Failures are triaged by whether they affect
retrieval recall, citation quality, or answer support.
""",
    "release_readiness_checklist.md": """---
document_id: release-readiness-checklist
title: Release Readiness Checklist
document_type: release
business_domain: delivery
sensitivity_level: synthetic-demo
created_at: 2026-01-22T00:00:00Z
---
# Release Readiness Checklist

Release readiness requires passing unit tests, API tests, safety scan, ingestion validation,
evaluation review, and observability verification. The release owner confirms rollback steps,
runtime configuration, service health checks, and dashboard links.

For AI features, readiness also requires prompt version notes, retrieval hit-rate review,
citation coverage review, and a sample trace inspection. Any unsupported answer behavior must
return the standard insufficient-context response.
""",
    "cloud_deployment_standard.md": """---
document_id: cloud-deployment-standard
title: Cloud Deployment Standard
document_type: deployment
business_domain: cloud-platform
sensitivity_level: synthetic-demo
created_at: 2026-01-24T00:00:00Z
---
# Cloud Deployment Standard

The reference deployment pattern uses a containerized FastAPI service, managed secrets, centralized
logging, health probes, autoscaling, and a managed vector database. Configuration is provided
through environment variables and deployment manifests.

Deployment reviews check image provenance, network policy, runtime identity, storage lifecycle,
and rollback automation. Observability should include request latency, retrieval latency, error
rate, confidence score distribution, and guardrail outcomes.
""",
    "incident_postmortem_template.md": """---
document_id: incident-postmortem-template
title: Incident Postmortem Template
document_type: incident
business_domain: reliability
sensitivity_level: synthetic-demo
created_at: 2026-01-26T00:00:00Z
---
# Incident Postmortem Template

Postmortems describe impact, timeline, detection source, contributing factors, mitigation steps,
and prevention actions. For AI incidents, the template adds retrieved context samples, citations,
trace identifiers, prompt versions, evaluation gaps, and guardrail outcomes.

Action items should be owner-assigned, time-bound, and linked to a measurable verification step.
The tone is learning-oriented and blameless.
""",
    "data_privacy_guideline.md": """---
document_id: data-privacy-guideline
title: Data Privacy Guideline
document_type: privacy
business_domain: data-governance
sensitivity_level: synthetic-demo
created_at: 2026-01-28T00:00:00Z
---
# Data Privacy Guideline

Product teams should complete a privacy review before adding a new document source, attribute,
or user-visible AI feature. The review records purpose, retention period, access pattern,
minimization controls, and deletion workflow.

The assistant should only index approved synthetic demo content in this repository. Privacy checks
also verify that logs avoid raw document dumps and store only operational metadata needed for
debugging and evaluation.
""",
    "support_knowledge_article.md": """---
document_id: support-knowledge-article
title: Support Knowledge Article
document_type: support
business_domain: user-operations
sensitivity_level: synthetic-demo
created_at: 2026-02-01T00:00:00Z
---
# Support Knowledge Article

When users receive an insufficient-context response, support teams should confirm that the relevant
document is indexed, metadata filters are correct, and the question is within the demo knowledge
space. Users can retry with a more specific question or request that a new synthetic document be
added to the index.

Support responses should explain that the assistant prefers refusal over unsupported claims.
""",
    "product_requirements_demo.md": """---
document_id: product-requirements-demo
title: Product Requirements Demo
document_type: product
business_domain: product-engineering
sensitivity_level: synthetic-demo
created_at: 2026-02-03T00:00:00Z
---
# Product Requirements Demo

The demo assistant should provide grounded answers, citations, retrieval strategy, confidence
score, guardrail status, and trace metadata. Users can filter by document type and inspect indexed
document summaries through an API endpoint.

Success metrics include answer usefulness, citation quality, unsupported-query refusal rate,
latency, and retrieval hit rate on synthetic golden questions.
""",
    "security_review_checklist.md": """---
document_id: security-review-checklist
title: Security Review Checklist
document_type: security
business_domain: application-security
sensitivity_level: synthetic-demo
created_at: 2026-02-05T00:00:00Z
---
# Security Review Checklist

Security review covers authentication, authorization, input validation, dependency scanning,
network exposure, secret handling, logging controls, and abuse-case testing. AI services add
prompt-injection tests, source-citation checks, refusal tests, and trace metadata review.

The service should avoid hardcoded secrets, validate request payloads, and keep demo data separate
from generated indexes.
""",
    "engineering_onboarding_guide.md": """---
document_id: engineering-onboarding-guide
title: Engineering Onboarding Guide
document_type: onboarding
business_domain: engineering-enablement
sensitivity_level: synthetic-demo
created_at: 2026-02-07T00:00:00Z
---
# Engineering Onboarding Guide

New contributors start by reading the architecture notes, running the safety scan, ingesting
synthetic documents, calling the chat endpoint, and running evaluation. The preferred workflow is
small changes, focused tests, and clear trace metadata for AI behavior.

Contributors should keep examples generic and avoid adding organization-specific details.
""",
    "vendor_evaluation_memo.md": """---
document_id: vendor-evaluation-memo
title: Vendor Evaluation Memo
document_type: vendor
business_domain: platform-strategy
sensitivity_level: synthetic-demo
created_at: 2026-02-09T00:00:00Z
---
# Vendor Evaluation Memo

Vector database options should be evaluated by retrieval quality, metadata filtering, operational
fit, backup capability, cost predictability, and developer experience. Reranking options should
be evaluated by latency, relevance lift, integration effort, and observability support.

The demo uses a local index by default so reviewers can run the project without external services.
""",
}


def main() -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, content in DOCUMENTS.items():
        (DOCS_DIR / filename).write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Seeded {len(DOCUMENTS)} synthetic documents in {DOCS_DIR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

