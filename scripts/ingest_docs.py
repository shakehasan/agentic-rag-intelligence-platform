from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from backend.app.core.config import get_settings
    from backend.app.services.cache import rebuild_index

    settings = get_settings()
    index = rebuild_index(settings.synthetic_docs_dir, settings)
    print(
        f"Indexed {index.indexed_documents} documents and {index.indexed_chunks} chunks "
        f"from {settings.synthetic_docs_dir}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
