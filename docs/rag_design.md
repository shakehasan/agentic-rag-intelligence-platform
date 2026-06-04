# RAG Design

The ingestion pipeline normalizes supported files into a common document model:

- document id
- source
- title
- document type
- business domain
- sensitivity level
- creation timestamp
- chunk id
- content

Chunking uses recursive splitting with configurable size and overlap. Metadata stays attached to each chunk so filters and citations are available throughout retrieval and answer generation.

Hybrid retrieval combines deterministic dense search with BM25 sparse search. Reciprocal rank fusion balances semantic recall with lexical precision, which helps policy and checklist questions where exact terms matter.

The optional reranker module is intentionally a placeholder extension point. A cross-encoder, hosted reranking API, or local model can be added behind the same interface.

