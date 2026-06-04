# Solution Catalog

The solution catalog is a public-safe set of synthetic blueprints that show how the platform can support multiple knowledge intelligence workflows without using real organization data.

## Included Blueprints

- AI Governance Policy Intelligence
- Release Readiness Copilot
- Cloud Deployment Advisor
- QA Strategy Intelligence
- Privacy Review Assistant
- Incident Review Assistant
- Support Triage Assistant
- Architecture Explainer
- Security Review Assistant
- Vendor Evaluation Assistant

Each blueprint includes a problem statement, architecture pattern, capabilities, evaluation focus, and public-safe note. The catalog is exposed through:

```bash
curl http://localhost:8000/solutions
```

Filtering by domain is supported:

```bash
curl "http://localhost:8000/solutions?domain=responsible-ai"
```

## Why This Matters

Production-style AI platforms are rarely a single endpoint. They support repeatable patterns across related workflows: policy lookup, release checks, quality strategy, cloud deployment guidance, and privacy review. The catalog demonstrates that the same core RAG and orchestration architecture can be applied across multiple synthetic domains while preserving source grounding and safety behavior.
