"""Inserts `const placeSentences = {...};` into barcode.html right after placeToSector."""
import json
import os
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not locate repository root (no .git directory found)")


REPO_ROOT = Path(os.environ["DISSERTATION_REPO_ROOT"]) if os.environ.get("DISSERTATION_REPO_ROOT") else _find_repo_root(Path(__file__).resolve())
HTML_PATH = REPO_ROOT / "data/processed/dir_1/barcode/d3/barcode.html"
DATA_PATH = REPO_ROOT / "data/processed/dir_1/barcode/data/dir1_sentences.json"

ANCHOR = "\nlet currentOrder = 'sector';"

def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    data_json = json.dumps(data, ensure_ascii=False)
    html = HTML_PATH.read_text()
    if "const placeSentences" in html:
        print("placeSentences already present, skipping")
        return
    insertion = f"\nconst placeSentences = {data_json};\n"
    if ANCHOR not in html:
        raise RuntimeError("Anchor not found")
    html = html.replace(ANCHOR, insertion + ANCHOR, 1)
    HTML_PATH.write_text(html)
    print(f"Inserted placeSentences ({len(data_json)/1024:.1f} KB) into {HTML_PATH}")

if __name__ == "__main__":
    main()
