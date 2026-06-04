class AppError(Exception):
    """Base application exception."""


class IngestionError(AppError):
    """Raised when document ingestion cannot complete."""


class RetrievalError(AppError):
    """Raised when retrieval cannot complete."""


class GuardrailError(AppError):
    """Raised when a generated answer fails validation."""

