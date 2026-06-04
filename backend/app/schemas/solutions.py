from pydantic import BaseModel


class SolutionCapability(BaseModel):
    name: str
    description: str


class SolutionBlueprint(BaseModel):
    solution_id: str
    title: str
    domain: str
    problem_statement: str
    architecture_pattern: str
    capabilities: list[SolutionCapability]
    evaluation_focus: list[str]
    public_safe_note: str


class SolutionCatalogResponse(BaseModel):
    total_solutions: int
    solutions: list[SolutionBlueprint]

