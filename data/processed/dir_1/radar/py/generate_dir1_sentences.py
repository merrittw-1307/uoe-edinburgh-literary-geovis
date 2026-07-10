"""
Adds example-sentence data for radar.html and barcode.html, and a full
sector+books+sentences enrichment for small_multiples.html.

Does NOT recompute the percentages/abs counts/book lists already embedded
in radar.html and barcode.html (those are correct and left untouched) -
this only adds a parallel lookup keyed by (author, place) so the existing
numbers can't drift. small_multiples.html has no sector/book/sentence data
at all yet, so for that one we parse its existing embedded `data` object
(to keep lat/lon/mention_count exactly as-is) and attach the new fields.
"""
import json
import re
import random
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

RANDOM_SEED = 42
MAX_SENTENCES_PER_PLACE = 3
MAX_SENTENCE_CHARS = 220
MAX_BOOKS_FOR_SMALL_MULTIPLES = 5

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SECTORS_CSV = REPO_ROOT / "data/processed/sectors/location_sectors_v2.csv"
SMALL_MULTIPLES_HTML = REPO_ROOT / "data/processed/dir_1/small_multiples/d3/small_multiples.html"

OUT_SENTENCES_PATHS = [
    REPO_ROOT / "data/processed/dir_1/radar/data/dir1_sentences.json",
    REPO_ROOT / "data/processed/dir_1/barcode/data/dir1_sentences.json",
]
OUT_SMALL_MULTIPLES = REPO_ROOT / "data/processed/dir_1/small_multiples/data/small_multiples_enriched.json"

engine = create_engine("postgresql://wangmingyu@localhost:5432/litlong_edinburgh")

QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    l.text AS place,
    d.title AS doc_title,
    s.text AS sentence_text
FROM api_locationmention lm
JOIN api_location l ON lm.location_id = l.id
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
JOIN api_document d ON lm.document_id = d.id
JOIN api_sentence s ON lm.sentence_id = s.id
WHERE (
    (TRIM(a.forenames) = 'Walter' AND TRIM(a.surname) = 'Scott') OR
    (TRIM(a.forenames) = 'Robert Louis' AND TRIM(a.surname) = 'Stevenson') OR
    (TRIM(a.forenames) = 'Irvine' AND TRIM(a.surname) = 'Welsh') OR
    (TRIM(a.forenames) = 'John Gibson' AND TRIM(a.surname) = 'Lockhart') OR
    (TRIM(a.forenames) = 'Alexander' AND TRIM(a.surname) = 'McCall Smith')
)
"""


def truncate(text: str) -> str:
    text = " ".join(text.split())
    if len(text) <= MAX_SENTENCE_CHARS:
        return text
    return text[:MAX_SENTENCE_CHARS].rsplit(" ", 1)[0] + "…"


def main() -> None:
    random.seed(RANDOM_SEED)
    df = pd.read_sql(QUERY, engine)
    print(f"Loaded {len(df)} mention rows for the 5 test authors (no top-N filter)")

    sectors = pd.read_csv(SECTORS_CSV)[["text", "sector"]].drop_duplicates("text")
    sector_by_place = dict(zip(sectors["text"], sectors["sector"]))

    sentences_by_author_place: dict[str, dict[str, list[dict]]] = {}
    books_by_author_place: dict[str, dict[str, list[dict]]] = {}

    for (author, place), group in df.groupby(["author", "place"]):
        pool = group[["sentence_text", "doc_title"]].drop_duplicates("sentence_text")
        sample_n = min(MAX_SENTENCES_PER_PLACE, len(pool))
        sample = pool.sample(n=sample_n, random_state=RANDOM_SEED)
        sentences_by_author_place.setdefault(author, {})[place] = [
            {"text": truncate(row.sentence_text), "book": row.doc_title}
            for row in sample.itertuples()
        ]

        counts = group.groupby("doc_title").size().reset_index(name="count").sort_values("count", ascending=False)
        books_by_author_place.setdefault(author, {})[place] = [
            {"title": row.doc_title, "count": int(row.count)}
            for row in counts.head(MAX_BOOKS_FOR_SMALL_MULTIPLES).itertuples()
        ]

    for out_path in OUT_SENTENCES_PATHS:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(sentences_by_author_place, ensure_ascii=False))
        print(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")

    # Enrich small_multiples.html's existing embedded `data` object in place.
    html = SMALL_MULTIPLES_HTML.read_text()
    match = re.search(r"const data = (\{.*?\});", html)
    if not match:
        raise RuntimeError("Could not find `const data = {...};` in small_multiples.html")
    sm_data = json.loads(match.group(1))

    for author, places in sm_data.items():
        for entry in places:
            place = entry["place"]
            entry["sector"] = sector_by_place.get(place, "Outer Scotland")
            entry["books"] = books_by_author_place.get(author, {}).get(place, [])
            entry["sentences"] = sentences_by_author_place.get(author, {}).get(place, [])

    OUT_SMALL_MULTIPLES.parent.mkdir(parents=True, exist_ok=True)
    OUT_SMALL_MULTIPLES.write_text(json.dumps(sm_data, ensure_ascii=False))
    print(f"Wrote {OUT_SMALL_MULTIPLES} ({OUT_SMALL_MULTIPLES.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
