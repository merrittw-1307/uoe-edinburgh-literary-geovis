"""Inserts `const placeSentences = {...};` into radar.html right after detailData."""
import json
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
HTML_PATH = REPO_ROOT / "data/processed/dir_1/radar/d3/radar.html"
DATA_PATH = REPO_ROOT / "data/processed/dir_1/radar/data/dir1_sentences.json"

ANCHOR = "\nconst N = sectors.length;"

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
