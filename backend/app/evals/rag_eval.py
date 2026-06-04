from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from backend.app.agents.graph import run_agent
from backend.app.evals.golden_dataset import GOLDEN_QUESTIONS
from backend.app.evals.metrics import compute_metrics
from backend.app.schemas.evaluation import EvaluationResponse


def run_evaluation(
    limit: int | None = None,
    output_dir: Path | None = None,
    write_files: bool = True,
) -> EvaluationResponse:
    questions = GOLDEN_QUESTIONS[:limit] if limit else GOLDEN_QUESTIONS
    results: list[dict[str, Any]] = []

    for item in questions:
        started = time.perf_counter()
        response = run_agent(item.question, filters=item.filters)
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        results.append(
            {
                "question": item.question,
                "expected_sources": item.expected_sources,
                "should_answer": item.should_answer,
                "answer": response.answer,
                "retrieved_sources": sorted(
                    {context["source"] for context in response.retrieved_context}
                ),
                "citation_sources": sorted({citation.source for citation in response.citations}),
                "confidence_score": response.confidence_score,
                "guardrail_status": response.guardrail_status,
                "latency_ms": latency_ms,
            }
        )

    metrics = compute_metrics(results)
    report_path = None
    results_path = None
    if write_files:
        output_dir = output_dir or Path(".")
        output_dir.mkdir(parents=True, exist_ok=True)
        results_path = str(output_dir / "eval_results.json")
        report_path = str(output_dir / "eval_report.md")
        Path(results_path).write_text(
            json.dumps({"metrics": metrics.model_dump(), "results": results}, indent=2),
            encoding="utf-8",
        )
        Path(report_path).write_text(
            _render_report(metrics.model_dump(), results),
            encoding="utf-8",
        )

    return EvaluationResponse(
        metrics=metrics,
        evaluated_questions=len(questions),
        report_path=report_path,
        results_path=results_path,
    )


def _render_report(metrics: dict[str, Any], results: list[dict[str, Any]]) -> str:
    lines = [
        "# RAG Evaluation Report",
        "",
        "This report was generated from synthetic golden questions.",
        "",
        "## Metrics",
    ]
    for key, value in metrics.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Question Results"])
    for result in results:
        lines.append(
            f"- {result['question']} -> {result['guardrail_status']} "
            f"({result['latency_ms']} ms)"
        )
    lines.append("")
    return "\n".join(lines)
