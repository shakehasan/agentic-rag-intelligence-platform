from pydantic import BaseModel


class GoldenQuestion(BaseModel):
    question: str
    expected_sources: list[str]
    should_answer: bool = True
    filters: dict[str, str] | None = None


class EvaluationRequest(BaseModel):
    limit: int | None = None


class EvaluationMetrics(BaseModel):
    retrieval_hit_rate: float
    citation_coverage: float
    answer_groundedness: float
    unsupported_answer_rate: float
    average_latency_ms: float


class EvaluationResponse(BaseModel):
    metrics: EvaluationMetrics
    evaluated_questions: int
    report_path: str | None = None
    results_path: str | None = None
