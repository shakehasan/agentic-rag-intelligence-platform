from pathlib import Path

from backend.app.rag.chunking import chunk_documents
from backend.app.rag.loaders import load_documents


def test_ingestion_creates_chunks() -> None:
    docs = load_documents(Path("data/synthetic_docs"))
    chunks = chunk_documents(docs, chunk_size=320, overlap=40)

    assert len(docs) >= 10
    assert len(chunks) >= len(docs)
    assert all(chunk.chunk_id for chunk in chunks)
    assert all(chunk.source.endswith(".md") for chunk in chunks)

