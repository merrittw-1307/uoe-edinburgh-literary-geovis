"""
Place-level (not sector-level) mention data for all 408 authors with location
data, for barcode_scale_explore.html. Reuses the same query shape as
generate_all_authors_radar_data.py but keeps individual places instead of
aggregating to sectors, since the bar-code design's axis is place, not sector.

Unlike the original 5-author barcode.html (which fixes one shared 39-place
column universe so rows are visually aligned), this export gives each author
their own top-15 places by mention count. A shared column universe does not
scale past a handful of authors - see NOTES.md - so the scale-exploration
tool tests each author's own top-15, which is still a fair test of the
design's actual scaling bottleneck (number of stacked rows), independent of
the column-alignment question.
"""
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SECTORS_CSV = REPO_ROOT / "data/processed/sectors/location_sectors_v2.csv"
OUT_PATH = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_barcode.json"

TOP_N_PLACES = 15

engine = create_engine("postgresql://wangmingyu@localhost:5432/litlong_edinburgh")

QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    l.text AS place,
    COUNT(lm.id) AS mentions
FROM api_locationmention lm
JOIN api_location l ON lm.location_id = l.id
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
GROUP BY a.id, a.forenames, a.surname, l.text
"""


def main() -> None:
    df = pd.read_sql(QUERY, engine)
    df = df.groupby(["author", "place"], as_index=False)["mentions"].sum()
    print(f"Loaded {len(df)} (author, place) rows, {df['author'].nunique()} distinct author names")

    sectors = pd.read_csv(SECTORS_CSV)[["text", "sector"]].drop_duplicates("text")
    sector_by_place = dict(zip(sectors["text"], sectors["sector"]))
    df["sector"] = df["place"].map(sector_by_place).fillna("Outer Scotland")

    records = []
    for author, group in df.groupby("author"):
        total = int(group["mentions"].sum())
        top = group.sort_values("mentions", ascending=False).head(TOP_N_PLACES)
        top_total = int(top["mentions"].sum())
        places = [
            {
                "place": row.place,
                "sector": row.sector,
                "abs": int(row.mentions),
                "pct_of_top15": round(row.mentions / top_total, 4) if top_total else 0.0,
            }
            for row in top.itertuples()
        ]
        records.append({"author": author, "total_mentions": total, "places": places})

    records.sort(key=lambda r: -r["total_mentions"])
    records = [r for r in records if r["total_mentions"] > 0]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(records, ensure_ascii=False))
    print(f"Wrote {len(records)} authors to {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
