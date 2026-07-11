"""
Generates example-sentence data for the Combined Interface's outer detail
panel, for all 408 authors (not just the five-author canonical set).

Mirrors dir_1/radar/py/generate_dir1_sentences.py exactly (same sampling,
same truncation, same random seed) but drops the WHERE-author filter and
restricts to each author's own top-15 places by mention count, matching
the top-15-per-author convention already used by the live radar/barcode/
network/linear rendering in combined_interface.html -- these are exactly
the (author, place) pairs reachable through the UI, so nothing outside
that set needs sentence data.
"""
import json
import random
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

RANDOM_SEED = 42
MAX_SENTENCES_PER_PLACE = 3
MAX_SENTENCE_CHARS = 220
TOP_N_PLACES = 15

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
OUT_PATH = REPO_ROOT / "data/processed/combined/data/all_authors_sentences.json"

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
"""


def truncate(text: str) -> str:
    text = " ".join(text.split())
    if len(text) <= MAX_SENTENCE_CHARS:
        return text
    return text[:MAX_SENTENCE_CHARS].rsplit(" ", 1)[0] + "…"


def main() -> None:
    random.seed(RANDOM_SEED)
    df = pd.read_sql(QUERY, engine)
    print(f"Loaded {len(df)} sentence-linked mention rows for all authors")

    mention_counts = df.groupby(["author", "place"]).size().reset_index(name="mentions")
    mention_counts["rank"] = mention_counts.groupby("author")["mentions"].rank(method="first", ascending=False)
    top_pairs = set(
        zip(
            mention_counts.loc[mention_counts["rank"] <= TOP_N_PLACES, "author"],
            mention_counts.loc[mention_counts["rank"] <= TOP_N_PLACES, "place"],
        )
    )
    df = df[df.apply(lambda r: (r.author, r.place) in top_pairs, axis=1)]
    print(f"Restricted to {len(top_pairs)} (author, place) top-15 pairs -> {len(df)} rows")

    sentences_by_author_place: dict[str, dict[str, list[dict]]] = {}
    for (author, place), group in df.groupby(["author", "place"]):
        pool = group[["sentence_text", "doc_title"]].drop_duplicates("sentence_text")
        sample_n = min(MAX_SENTENCES_PER_PLACE, len(pool))
        sample = pool.sample(n=sample_n, random_state=RANDOM_SEED)
        sentences_by_author_place.setdefault(author, {})[place] = [
            {"text": truncate(row.sentence_text), "book": row.doc_title}
            for row in sample.itertuples()
        ]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(sentences_by_author_place, ensure_ascii=False))
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB), {len(sentences_by_author_place)} authors")


if __name__ == "__main__":
    main()
