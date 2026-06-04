from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic RAG Intelligence Platform"
    environment: str = "local"
    log_level: str = "INFO"

    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"

    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "agentic-rag-intelligence-platform"

    vector_db: str = "chroma"
    vector_index_dir: Path = Path("data/index")
    synthetic_docs_dir: Path = Path("data/synthetic_docs")

    chunk_size: int = 900
    chunk_overlap: int = 140
    retrieval_top_k: int = 6
    min_confidence: float = 0.35
    hybrid_dense_weight: float = Field(default=0.55, ge=0.0, le=1.0)
    hybrid_sparse_weight: float = Field(default=0.45, ge=0.0, le=1.0)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

