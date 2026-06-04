from pydantic import BaseModel


class BenchmarkCaseResponse(BaseModel):
    case_id: str
    query: str
    expected_document_type: str
    expected_topic: str
    intent: str
    should_answer: bool
    difficulty: str
    tags: tuple[str, ...]


class BenchmarkCatalogResponse(BaseModel):
    total_returned: int
    summary: dict[str, object]
    cases: list[BenchmarkCaseResponse]

