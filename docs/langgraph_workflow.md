# LangGraph Workflow

The workflow is implemented as small, testable nodes and can be compiled into a LangGraph state graph when the dependency is available.

```mermaid
flowchart TD
    A[Intent Classifier] -->|unsupported| H[Escalation]
    A -->|supported| B[Query Rewriter]
    B --> C[Retrieval Planner]
    C --> D[Retriever]
    D -->|low confidence| H
    D -->|sufficient context| E[Answer Generator]
    E --> F[Hallucination Guard]
    F -->|failed| H
    F -->|passed| G[Compliance Guard]
    G -->|failed| H
    G -->|passed| I[Response]
```

The state carries query, intent, filters, retrieval strategy, retrieved context, answer, citations, confidence score, guardrail status, and trace metadata.

Unsupported questions, low-confidence retrieval, failed grounding checks, or invalid citations route to escalation. Escalation returns the standard insufficient-context response instead of inventing an answer.

