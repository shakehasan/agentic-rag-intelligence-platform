from fastapi import APIRouter

from backend.app.evals.rag_eval import run_evaluation
from backend.app.schemas.evaluation import EvaluationRequest, EvaluationResponse

router = APIRouter()


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest) -> EvaluationResponse:
    return run_evaluation(limit=request.limit, write_files=False)

