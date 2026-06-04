from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from backend.app.evals.rag_eval import run_evaluation

    response = run_evaluation(output_dir=ROOT, write_files=True)
    print(f"Evaluated {response.evaluated_questions} synthetic questions.")
    print(response.metrics.model_dump_json(indent=2))
    print(f"Wrote {response.results_path} and {response.report_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
