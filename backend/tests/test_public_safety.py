import shutil
from pathlib import Path

from scripts.public_safety_scan import scan_root


def test_public_safety_scan_blocks_banned_terms() -> None:
    scan_dir = Path("test_artifacts/public_safety_scan")
    shutil.rmtree(scan_dir, ignore_errors=True)
    docs = scan_dir / "docs"
    docs.mkdir(parents=True)
    (docs / "public_safety.md").write_text("allowed " + ("conf" + "idential"), encoding="utf-8")
    (scan_dir / "unsafe.md").write_text("not allowed " + ("conf" + "idential"), encoding="utf-8")

    findings = scan_root(scan_dir)

    assert len(findings) == 1
    assert findings[0].path == Path("unsafe.md")
    shutil.rmtree(scan_dir, ignore_errors=True)
