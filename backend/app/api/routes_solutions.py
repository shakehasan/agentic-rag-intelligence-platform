from fastapi import APIRouter

from backend.app.schemas.solutions import SolutionCatalogResponse
from backend.app.solutions.catalog import list_solution_blueprints

router = APIRouter()


@router.get("/solutions", response_model=SolutionCatalogResponse)
def solutions(domain: str | None = None) -> SolutionCatalogResponse:
    blueprints = list_solution_blueprints(domain=domain)
    return SolutionCatalogResponse(total_solutions=len(blueprints), solutions=blueprints)

