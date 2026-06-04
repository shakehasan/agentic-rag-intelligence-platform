from pathlib import Path

from backend.app.core.config import Settings
from backend.app.rag.chunking import chunk_documents
from backend.app.rag.hybrid_retriever import HybridRetriever
from backend.app.rag.loaders import load_documents


def test_hybrid_retrieval_returns_relevant_documents() -> None:
    settings = Settings(
        vector_index_dir=Path("test_artifacts/retrieval_index"),
        synthetic_docs_dir=Path("data/synthetic_docs"),
    )
    docs = load_documents(settings.synthetic_docs_dir)
    chunks = chunk_documents(docs, chunk_size=500, overlap=80)
    retriever = HybridRetriever.from_chunks(chunks, settings=settings, persist=False)

    results = retriever.retrieve(
        "What does the AI governance policy say about human review?",
        top_k=4,
        filters={"document_type": "policy"},
    )

    assert results
    assert results[0].source == "ai_governance_policy.md"
    assert "human review" in results[0].excerpt.lower()
