"""
Shared data generator for network.html and linear.html (Direction 2).

Reproduces the exact 5-author / top-15-places-per-author filter used in
network_data2.py, then enriches it with:
  - sector for each place (from data/processed/sectors/location_sectors_v2.csv)
  - example sentences per place (for hover text-snippet feature)
  - contributing book titles per co-occurrence edge (for click detail panel)

Output is written to both dir_2/network/data/ and dir_2/linear/data/ so each
chart's own data folder stays self-contained, matching the existing project
convention of per-chart data/ directories.
"""
import json
import random
from itertools import combinations
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

RANDOM_SEED = 42
TOP_PLACES_PER_AUTHOR = 15
MIN_EDGE_WEIGHT = 2
MAX_SENTENCES_PER_PLACE = 4
MAX_SENTENCE_CHARS = 220

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SECTORS_CSV = REPO_ROOT / "data/processed/sectors/location_sectors_v2.csv"
OUTPUT_PATHS = [
    REPO_ROOT / "data/processed/dir_2/network/data/network_enriched.json",
    REPO_ROOT / "data/processed/dir_2/linear/data/linear_enriched.json",
]

engine = create_engine("postgresql://wangmingyu@localhost:5432/litlong_edinburgh")

QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    lm.document_id,
    d.title AS doc_title,
    l.text AS place,
    lm.sentence_id,
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
    print(f"Loaded {len(df)} mention rows for the 5 test authors")

    top_places = (
        df.groupby(["author", "place"])["sentence_id"]
        .count()
        .reset_index(name="mention_count")
        .sort_values("mention_count", ascending=False)
        .groupby("author")
        .head(TOP_PLACES_PER_AUTHOR)
    )
    df_filtered = df.merge(top_places[["author", "place"]], on=["author", "place"])
    print(f"Filtered to {df_filtered['place'].nunique()} active places")

    sectors = pd.read_csv(SECTORS_CSV)[["text", "sector"]].drop_duplicates("text")
    sector_by_place = dict(zip(sectors["text"], sectors["sector"]))

    nodes_series = df_filtered.groupby("place").size().sort_values(ascending=False)
    nodes = [
        {
            "place": place,
            "total_mentions": int(count),
            "sector": sector_by_place.get(place, "Outer Scotland"),
        }
        for place, count in nodes_series.items()
    ]

    edge_counts: dict[tuple[str, str], int] = {}
    edge_docs: dict[tuple[str, str], set[tuple[int, str, str]]] = {}
    for doc_id, group in df_filtered.groupby("document_id"):
        places = group["place"].unique().tolist()
        if len(places) < 2:
            continue
        doc_title = group["doc_title"].iloc[0]
        doc_author = group["author"].iloc[0]
        for p1, p2 in combinations(sorted(places), 2):
            key = (p1, p2)
            edge_counts[key] = edge_counts.get(key, 0) + 1
            edge_docs.setdefault(key, set()).add((int(doc_id), doc_title, doc_author))

    edges = [
        {"source": p1, "target": p2, "weight": w}
        for (p1, p2), w in edge_counts.items()
        if w >= MIN_EDGE_WEIGHT
    ]
    edges.sort(key=lambda e: -e["weight"])
    print(f"Computed {len(edges)} edges with weight >= {MIN_EDGE_WEIGHT}")

    edge_books = {}
    for (p1, p2), docs in edge_docs.items():
        if edge_counts[(p1, p2)] < MIN_EDGE_WEIGHT:
            continue
        key = f"{p1}|||{p2}"
        books = sorted({(title, author) for _, title, author in docs}, key=lambda x: x[0])
        edge_books[key] = [{"title": t, "author": a} for t, a in books]

    place_sentences = {}
    for place, group in df_filtered.groupby("place"):
        pool = group[["sentence_text", "doc_title", "author"]].drop_duplicates("sentence_text")
        sample_n = min(MAX_SENTENCES_PER_PLACE, len(pool))
        sample = pool.sample(n=sample_n, random_state=RANDOM_SEED)
        place_sentences[place] = [
            {
                "text": truncate(row.sentence_text),
                "book": row.doc_title,
                "author": row.author,
            }
            for row in sample.itertuples()
        ]

    place_books = {}
    for place, group in df_filtered.groupby("place"):
        counts = (
            group.groupby(["doc_title", "author"])
            .size()
            .reset_index(name="mentions")
            .sort_values("mentions", ascending=False)
        )
        place_books[place] = [
            {"title": row.doc_title, "author": row.author, "mentions": int(row.mentions)}
            for row in counts.itertuples()
        ]

    payload = {
        "nodes": nodes,
        "edges": edges,
        "edgeBooks": edge_books,
        "placeSentences": place_sentences,
        "placeBooks": place_books,
    }

    for out_path in OUTPUT_PATHS:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False))
        print(f"Wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
