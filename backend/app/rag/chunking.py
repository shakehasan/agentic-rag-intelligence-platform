from __future__ import annotations

from backend.app.schemas.documents import DocumentChunk

from .loaders import RawDocument

SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def _merge_splits(parts: list[str], chunk_size: int, overlap: int) -> list[str]:
    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}{part}" if not current else f"{current} {part}"
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current.strip())
        current = part[-chunk_size:]
    if current:
        chunks.append(current.strip())

    if overlap <= 0 or len(chunks) <= 1:
        return chunks

    overlapped: list[str] = []
    previous_tail = ""
    for chunk in chunks:
        combined = f"{previous_tail} {chunk}".strip() if previous_tail else chunk
        overlapped.append(combined[: chunk_size + overlap].strip())
        previous_tail = chunk[-overlap:]
    return overlapped


def recursive_split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if len(normalized) <= chunk_size:
        return [normalized]

    for separator in SEPARATORS:
        if separator and separator in normalized:
            parts = [part.strip() for part in normalized.split(separator) if part.strip()]
            if parts:
                return _merge_splits(parts, chunk_size, overlap)

    return [
        normalized[index : index + chunk_size]
        for index in range(0, len(normalized), chunk_size)
    ]


def chunk_document(raw_document: RawDocument, chunk_size: int, overlap: int) -> list[DocumentChunk]:
    chunks = recursive_split_text(raw_document.content, chunk_size, overlap)
    return [
        DocumentChunk(
            **raw_document.metadata.model_dump(),
            chunk_id=f"{raw_document.metadata.document_id}-{index:03d}",
            content=chunk,
        )
        for index, chunk in enumerate(chunks, start=1)
    ]


def chunk_documents(
    raw_documents: list[RawDocument],
    chunk_size: int,
    overlap: int,
) -> list[DocumentChunk]:
    all_chunks: list[DocumentChunk] = []
    for document in raw_documents:
        all_chunks.extend(chunk_document(document, chunk_size=chunk_size, overlap=overlap))
    return all_chunks
