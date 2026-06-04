from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from backend.app.core.errors import IngestionError
from backend.app.schemas.documents import DocumentMetadata

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".csv"}


@dataclass(frozen=True)
class RawDocument:
    metadata: DocumentMetadata
    content: str


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _infer_document_type(path: Path) -> str:
    stem = path.stem.lower()
    if "policy" in stem:
        return "policy"
    if "architecture" in stem:
        return "architecture"
    if "privacy" in stem:
        return "privacy"
    if "security" in stem:
        return "security"
    if "release" in stem:
        return "release"
    if "incident" in stem:
        return "incident"
    if "support" in stem:
        return "support"
    if "qa" in stem or "automation" in stem:
        return "quality"
    if "requirement" in stem:
        return "product"
    if "vendor" in stem:
        return "vendor"
    if "onboarding" in stem:
        return "onboarding"
    if "deployment" in stem or "cloud" in stem:
        return "deployment"
    return "knowledge"


def _parse_date(value: str | None) -> datetime:
    if not value:
        return datetime.now(UTC)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(UTC)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed


def _parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text.strip()

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text.strip()

    metadata: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, parts[2].strip()


def _load_markdown_or_text(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    return _parse_front_matter(text)


def _load_csv(path: Path) -> tuple[dict[str, str], str]:
    rows: list[str] = []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for index, row in enumerate(reader, start=1):
            values = "; ".join(f"{key}: {value}" for key, value in row.items())
            rows.append(f"Row {index}: {values}")
    return {}, "\n".join(rows)


def _load_pdf(path: Path) -> tuple[dict[str, str], str]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise IngestionError("PDF ingestion requires the pypdf package.") from exc

    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return {}, text.strip()


def load_document(path: Path) -> RawDocument:
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise IngestionError(f"Unsupported file type: {path.suffix}")

    if path.suffix.lower() in {".txt", ".md"}:
        raw_metadata, content = _load_markdown_or_text(path)
    elif path.suffix.lower() == ".csv":
        raw_metadata, content = _load_csv(path)
    else:
        raw_metadata, content = _load_pdf(path)

    if not content.strip():
        raise IngestionError(f"No extractable content found in {path}")

    source = path.name
    document_id = raw_metadata.get("document_id") or _slug(path.stem)
    title = raw_metadata.get("title") or path.stem.replace("_", " ").title()
    metadata = DocumentMetadata(
        document_id=document_id,
        source=source,
        title=title,
        document_type=raw_metadata.get("document_type") or _infer_document_type(path),
        business_domain=raw_metadata.get("business_domain") or "knowledge-operations",
        sensitivity_level=raw_metadata.get("sensitivity_level") or "synthetic-demo",
        created_at=_parse_date(raw_metadata.get("created_at")),
    )
    return RawDocument(metadata=metadata, content=content)


def discover_documents(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_EXTENSIONS else []
    if not path.exists():
        raise IngestionError(f"Document path does not exist: {path}")
    return sorted(
        file
        for file in path.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def load_documents(path: Path) -> list[RawDocument]:
    return [load_document(file) for file in discover_documents(path)]
