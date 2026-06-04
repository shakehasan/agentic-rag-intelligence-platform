from fastapi import APIRouter

from backend.app.evals.benchmark_bank import benchmark_summary, list_benchmark_cases
from backend.app.schemas.benchmarks import BenchmarkCaseResponse, BenchmarkCatalogResponse

router = APIRouter()


@router.get("/benchmarks", response_model=BenchmarkCatalogResponse)
def benchmarks(
    limit: int | None = 25,
    document_type: str | None = None,
    difficulty: str | None = None,
) -> BenchmarkCatalogResponse:
    cases = list_benchmark_cases(
        limit=limit,
        document_type=document_type,
        difficulty=difficulty,
    )
    return BenchmarkCatalogResponse(
        total_returned=len(cases),
        summary=benchmark_summary(),
        cases=[BenchmarkCaseResponse(**case.__dict__) for case in cases],
    )

