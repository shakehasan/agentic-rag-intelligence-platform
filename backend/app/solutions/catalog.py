from backend.app.schemas.solutions import SolutionBlueprint, SolutionCapability

PUBLIC_SAFE_NOTE = (
    "This blueprint uses fictional synthetic scenarios and demo data only."
)


SOLUTION_BLUEPRINTS = [
    SolutionBlueprint(
        solution_id="governance-policy-intelligence",
        title="AI Governance Policy Intelligence",
        domain="responsible-ai",
        problem_statement=(
            "Teams need grounded answers about review requirements, model change controls, "
            "and responsible AI operating practices."
        ),
        architecture_pattern=(
            "Agentic RAG with policy-aware retrieval planning and guardrail routing."
        ),
        capabilities=[
            SolutionCapability(
                name="Policy intent detection",
                description="Classifies governance and review questions before retrieval.",
            ),
            SolutionCapability(
                name="Grounded policy response",
                description="Answers only from indexed synthetic policy documents.",
            ),
            SolutionCapability(
                name="Insufficient-context refusal",
                description="Routes unsupported requests to a standard fallback response.",
            ),
        ],
        evaluation_focus=["policy retrieval hit rate", "citation coverage", "refusal accuracy"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="release-readiness-copilot",
        title="Release Readiness Copilot",
        domain="delivery",
        problem_statement=(
            "Release owners need a fast way to inspect readiness checks, rollback tasks, "
            "and AI-specific validation requirements."
        ),
        architecture_pattern="Checklist-grounded RAG with release metadata filtering.",
        capabilities=[
            SolutionCapability(
                name="Readiness checklist retrieval",
                description="Retrieves release requirements and validation steps.",
            ),
            SolutionCapability(
                name="Traceable answer package",
                description="Returns answer, citations, confidence score, and trace id.",
            ),
            SolutionCapability(
                name="Evaluation-backed quality loop",
                description="Measures answer grounding and citation quality over golden questions.",
            ),
        ],
        evaluation_focus=["checklist recall", "latency", "groundedness"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="cloud-deployment-advisor",
        title="Cloud Deployment Advisor",
        domain="cloud-platform",
        problem_statement=(
            "Platform teams need concise deployment guidance covering runtime configuration, "
            "managed secrets, health checks, and observability."
        ),
        architecture_pattern=(
            "Hybrid retrieval over deployment standards with operational guardrails."
        ),
        capabilities=[
            SolutionCapability(
                name="Deployment standard lookup",
                description="Finds relevant cloud deployment requirements.",
            ),
            SolutionCapability(
                name="Operational metadata",
                description="Includes retrieval strategy and trace metadata for debugging.",
            ),
            SolutionCapability(
                name="Guardrail validation",
                description="Checks that generated guidance is supported by retrieved context.",
            ),
        ],
        evaluation_focus=["source diversity", "answer support ratio", "response latency"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="qa-strategy-intelligence",
        title="QA Strategy Intelligence",
        domain="engineering-quality",
        problem_statement=(
            "Engineering teams need searchable guidance for automation strategy, regression "
            "coverage, and evaluation-driven AI quality checks."
        ),
        architecture_pattern=(
            "Dense plus sparse retrieval over synthetic quality strategy documents."
        ),
        capabilities=[
            SolutionCapability(
                name="Quality scenario retrieval",
                description="Retrieves QA strategy, regression, and validation guidance.",
            ),
            SolutionCapability(
                name="Evaluation result reporting",
                description="Generates metrics for retrieval and grounded answer quality.",
            ),
            SolutionCapability(
                name="Feedback capture",
                description="Stores reviewer feedback signals for later analysis.",
            ),
        ],
        evaluation_focus=["retrieval hit rate", "feedback distribution", "citation usefulness"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="privacy-review-assistant",
        title="Privacy Review Assistant",
        domain="data-governance",
        problem_statement=(
            "Product teams need a structured way to answer privacy review questions using "
            "approved synthetic guidance."
        ),
        architecture_pattern="Metadata-filtered RAG with privacy-aware routing.",
        capabilities=[
            SolutionCapability(
                name="Privacy document filtering",
                description="Routes privacy questions to the privacy guideline when appropriate.",
            ),
            SolutionCapability(
                name="Grounded checklist synthesis",
                description="Summarizes review requirements from retrieved chunks.",
            ),
            SolutionCapability(
                name="Logging-safe telemetry",
                description="Tracks operational metadata without storing raw user secrets.",
            ),
        ],
        evaluation_focus=["privacy source recall", "unsupported answer rate", "guardrail outcomes"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="incident-review-assistant",
        title="Incident Review Assistant",
        domain="reliability",
        problem_statement=(
            "Reliability teams need structured answers about incident timelines, action items, "
            "trace review, and prevention patterns."
        ),
        architecture_pattern=(
            "Incident-document RAG with trace-aware context packaging and escalation handling."
        ),
        capabilities=[
            SolutionCapability(
                name="Postmortem context retrieval",
                description="Finds synthetic incident review fields and action item guidance.",
            ),
            SolutionCapability(
                name="Trace-focused summarization",
                description=(
                    "Surfaces trace identifiers and evaluation gaps from retrieved context."
                ),
            ),
            SolutionCapability(
                name="Prevention action synthesis",
                description="Summarizes owner-assigned follow-up actions from source content.",
            ),
        ],
        evaluation_focus=["incident source recall", "summary grounding", "trace metadata coverage"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="support-triage-assistant",
        title="Support Triage Assistant",
        domain="user-operations",
        problem_statement=(
            "Support teams need grounded guidance for insufficient-context responses, metadata "
            "filters, and document indexing checks."
        ),
        architecture_pattern="Support knowledge RAG with fallback-first answer behavior.",
        capabilities=[
            SolutionCapability(
                name="Support article retrieval",
                description="Retrieves guidance for resolving synthetic support scenarios.",
            ),
            SolutionCapability(
                name="Fallback explanation",
                description="Explains why unsupported answers are refused.",
            ),
            SolutionCapability(
                name="Question refinement guidance",
                description="Suggests more specific question patterns when context is limited.",
            ),
        ],
        evaluation_focus=["support article recall", "fallback accuracy", "response usefulness"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="architecture-explainer",
        title="Architecture Explainer",
        domain="platform-engineering",
        problem_statement=(
            "Engineering reviewers need a concise view of service layers, graph workflow, "
            "observability metadata, and retrieval interfaces."
        ),
        architecture_pattern="Architecture-note RAG with workflow-aware answer construction.",
        capabilities=[
            SolutionCapability(
                name="Layered architecture lookup",
                description="Retrieves details about API, graph, retrieval, and guardrail layers.",
            ),
            SolutionCapability(
                name="Workflow explanation",
                description="Explains how state moves through orchestration nodes.",
            ),
            SolutionCapability(
                name="Integration summary",
                description="Summarizes how local indexes can be replaced by managed services.",
            ),
        ],
        evaluation_focus=["architecture source recall", "technical clarity", "citation quality"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="security-review-assistant",
        title="Security Review Assistant",
        domain="application-security",
        problem_statement=(
            "Application teams need source-grounded review guidance for authentication, "
            "authorization, request validation, logging controls, and prompt-injection tests."
        ),
        architecture_pattern="Security checklist RAG with guardrail and citation validation.",
        capabilities=[
            SolutionCapability(
                name="Checklist retrieval",
                description="Finds synthetic security review requirements.",
            ),
            SolutionCapability(
                name="Prompt-injection review support",
                description="Surfaces AI-service specific review items from indexed context.",
            ),
            SolutionCapability(
                name="Citation validation",
                description="Ensures review answers cite retrieved checklist chunks.",
            ),
        ],
        evaluation_focus=["security source recall", "review completeness", "guardrail status"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
    SolutionBlueprint(
        solution_id="vendor-evaluation-assistant",
        title="Vendor Evaluation Assistant",
        domain="platform-strategy",
        problem_statement=(
            "Platform teams need a repeatable way to compare retrieval infrastructure options, "
            "reranking approaches, operational fit, and observability support."
        ),
        architecture_pattern="Vendor memo RAG with comparison intent routing.",
        capabilities=[
            SolutionCapability(
                name="Evaluation criteria retrieval",
                description="Finds synthetic scoring criteria for platform options.",
            ),
            SolutionCapability(
                name="Comparison answer generation",
                description="Synthesizes tradeoffs across retrieved vendor memo context.",
            ),
            SolutionCapability(
                name="Decision traceability",
                description="Returns citations and confidence scores for review.",
            ),
        ],
        evaluation_focus=["comparison grounding", "citation coverage", "source diversity"],
        public_safe_note=PUBLIC_SAFE_NOTE,
    ),
]


def list_solution_blueprints(domain: str | None = None) -> list[SolutionBlueprint]:
    if not domain:
        return SOLUTION_BLUEPRINTS
    return [blueprint for blueprint in SOLUTION_BLUEPRINTS if blueprint.domain == domain]
