"""
Ships raw (author, place, document) mention data for the full corpus so
network_scale_explore.html can compute top-15-places-per-author and
document-level co-occurrence *client-side*, for whatever author subset (or
document subset, for the "2-3 books" test) the user selects interactively.

This mirrors the methodology already documented for the five-author
network.html (top 15 places per author by mention count, then document-level
co-occurrence among the union of those places) but generalises it to run
over an arbitrary selection rather than a hardcoded WHERE clause, so the
scale-exploration tool is a real interactive instrument rather than a fixed
set of screenshots.
"""
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SECTORS_CSV = REPO_ROOT / "data/processed/sectors/location_sectors_v2.csv"
OUT_PATH = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_network.json"

engine = create_engine("postgresql://wangmingyu@localhost:5432/litlong_edinburgh")

QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    l.text AS place,
    lm.document_id AS document_id,
    d.title AS doc_title,
    COUNT(lm.id) AS mentions
FROM api_locationmention lm
JOIN api_location l ON lm.location_id = l.id
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
JOIN api_document d ON lm.document_id = d.id
GROUP BY a.id, a.forenames, a.surname, l.text, lm.document_id, d.title
"""


def main() -> None:
    df = pd.read_sql(QUERY, engine)
    print(f"Loaded {len(df)} (author, place, document) rows")

    sectors = pd.read_csv(SECTORS_CSV)[["text", "sector"]].drop_duplicates("text")
    sector_by_place = dict(zip(sectors["text"], sectors["sector"]))
    df["sector"] = df["place"].map(sector_by_place).fillna("Outer Scotland")

    # Merge duplicate-name author records (see NOTES.md) by summing at the
    # (author, place, document) grain before export.
    df = df.groupby(["author", "place", "document_id", "doc_title", "sector"], as_index=False)["mentions"].sum()

    mentions = df.to_dict(orient="records")

    documents = (
        df[["document_id", "doc_title"]]
        .drop_duplicates("document_id")
        .rename(columns={"document_id": "id", "doc_title": "title"})
    )
    doc_authors = df.groupby("document_id")["author"].unique().apply(list)
    documents["authors"] = documents["id"].map(doc_authors)
    documents = documents.to_dict(orient="records")

    payload = {"mentions": mentions, "documents": documents}
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False))
    print(f"Wrote {len(mentions)} mention rows, {len(documents)} documents to {OUT_PATH} "
          f"({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
