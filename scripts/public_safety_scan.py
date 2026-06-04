from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path


def _terms() -> list[str]:
    return [
        "JP" + "Morgan",
        "JM" + "PC",
        "Cha" + "se",
        "em" + "ployer",
        "client " + "conf" + "idential",
        "pro" + "prietary",
        "internal " + "bank",
        "real " + "customer",
        "production " + "bank",
        "conf" + "idential",
        "restr" + "icted",
    ]


SKIPPED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".pytest_cache_local",
    ".pytest_tmp",
    ".ruff_cache",
    ".mypy_cache",
    "data/index",
}

ALLOWED_FILES = {
    Path("docs/public_safety.md"),
    Path("scripts/public_safety_scan.py"),
}


@dataclass(frozen=True)
class Finding:
    path: Path
    term: str
    line_number: int
    line: str


def scan_root(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    root = root.resolve()
    for current_root, dirnames, filenames in os.walk(root):
        current_path = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skipped_directory(current_path / dirname, root)
        ]
        for filename in filenames:
            path = current_path / filename
            if _should_skip(path, root):
                continue
            relative = path.relative_to(root)
            if relative in ALLOWED_FILES:
                continue
            text = _read_text(path)
            if text is None:
                continue
            findings.extend(_scan_text(relative, text))
    return findings


def _scan_text(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lowered_terms = [(term, term.lower()) for term in _terms()]
    for line_number, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for display_term, lowered_term in lowered_terms:
            if lowered_term in lowered:
                findings.append(
                    Finding(
                        path=path,
                        term=display_term,
                        line_number=line_number,
                        line=line.strip(),
                    )
                )
    return findings


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _should_skip(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    parts = set(relative.parts)
    return _is_skipped_directory(path.parent, root) or any(
        skipped in parts for skipped in SKIPPED_DIRS
    ) or path.suffix.lower() in {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".pdf",
        ".ico",
    }


def _is_skipped_directory(path: Path, root: Path) -> bool:
    relative = path.relative_to(root).as_posix()
    return path.name in SKIPPED_DIRS or relative in SKIPPED_DIRS or relative.startswith(
        "data/index/"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan public portfolio files for unsafe terms.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan.")
    args = parser.parse_args()
    findings = scan_root(Path(args.root))
    if findings:
        print("Public safety scan failed:")
        for finding in findings:
            print(
                f"- {finding.path}:{finding.line_number} "
                f"matched {finding.term!r}: {finding.line}"
            )
        return 1
    print("Public safety scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
