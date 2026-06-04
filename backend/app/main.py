from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import (
    routes_chat,
    routes_documents,
    routes_eval,
    routes_health,
    routes_ingestion,
)
from backend.app.core.config import get_settings
from backend.app.core.logging import configure_logging
from backend.app.services.langsmith import configure_langsmith


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    configure_langsmith(settings)

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Public-safe Agentic RAG API using synthetic Northstar Labs data.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(routes_health.router)
    app.include_router(routes_ingestion.router)
    app.include_router(routes_chat.router)
    app.include_router(routes_eval.router)
    app.include_router(routes_documents.router)
    return app


app = create_app()

