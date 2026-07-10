"""
Generalises radar_data_v2.csv from 5 hardcoded authors to all authors with
at least one location mention (420 of 424). Used by radar_scale_explore.html
so the author-count control can be tested at 2 / 5 / ~20 / all authors,
without touching the canonical 5-author radar.html or its data.

Sector percentages are computed the same way as the original 5-author
pipeline: percentage of an author's total mentions *excluding* Outer
Scotland, matching the documented sector methodology (Section 3.5 of the
dissertation). This script's output is spot-checked against the five
known values already published in Appendix table tab:authors.
"""
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SECTORS_CSV = REPO_ROOT / "data/processed/sectors/location_sectors_v2.csv"
OUT_PATH = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_radar.json"

SECTORS = [
    "Almond", "Canongate", "Craigentinny/Duddingston", "Forth", "Inverleith",
    "Leith", "Liberton/Gilmerton", "New Town", "Old Town", "Pentlands",
    "Portobello/Craigmillar", "South Central", "South West", "Western Edinburgh",
]

engine = create_engine("postgresql://wangmingyu@localhost:5432/litlong_edinburgh")

PLACE_QUERY = """
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

WORKS_QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    COUNT(DISTINCT lm.document_id) AS works
FROM api_locationmention lm
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
GROUP BY a.id, a.forenames, a.surname
"""


def main() -> None:
    places = pd.read_sql(PLACE_QUERY, engine)
    works = pd.read_sql(WORKS_QUERY, engine)
    print(f"Loaded {len(places)} (author, place) rows, {places['author'].nunique()} distinct author names")

    # Duplicate display names (same trimmed name, different author.id) are merged -
    # see NOTES.md. Summing here achieves that merge.
    places = places.groupby(["author", "place"], as_index=False)["mentions"].sum()
    works = works.groupby("author", as_index=False)["works"].sum()

    sectors = pd.read_csv(SECTORS_CSV)[["text", "sector"]].drop_duplicates("text")
    sector_by_place = dict(zip(sectors["text"], sectors["sector"]))
    places["sector"] = places["place"].map(sector_by_place).fillna("Outer Scotland")

    in_edinburgh = places[places["sector"] != "Outer Scotland"]
    author_totals = in_edinburgh.groupby("author")["mentions"].sum().rename("total_in_edinburgh")
    all_totals = places.groupby("author")["mentions"].sum().rename("total_mentions")

    sector_sums = (
        in_edinburgh.groupby(["author", "sector"])["mentions"].sum().unstack(fill_value=0)
    )
    for s in SECTORS:
        if s not in sector_sums.columns:
            sector_sums[s] = 0
    sector_sums = sector_sums[SECTORS]
    sector_pct = sector_sums.div(author_totals, axis=0).fillna(0.0)

    records = []
    for author in sector_pct.index:
        pct_row = sector_pct.loc[author]
        dominant_sector = pct_row.idxmax()
        records.append({
            "author": author,
            "total_mentions": int(all_totals.get(author, 0)),
            "works": int(works.set_index("author")["works"].get(author, 0)),
            "sector_pct": {s: round(float(pct_row[s]), 4) for s in SECTORS},
            "dominant_sector": dominant_sector,
            "dominant_pct": round(float(pct_row[dominant_sector]), 4),
        })

    records.sort(key=lambda r: -r["total_mentions"])
    records = [r for r in records if r["total_mentions"] > 0]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(records, ensure_ascii=False))
    print(f"Wrote {len(records)} authors to {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")

    # Spot-check against the five published values (Appendix tab:authors)
    published = {
        "Alexander McCall Smith": ("New Town", 0.436),
        "Irvine Welsh": ("Leith", 0.443),
        "John Gibson Lockhart": ("New Town", 0.259),
        "Walter Scott": ("Old Town", 0.320),
        "Robert Louis Stevenson": ("Old Town", 0.207),
    }
    by_name = {r["author"]: r for r in records}
    print("\nSpot-check against published Appendix values:")
    for name, (sector, pct) in published.items():
        r = by_name.get(name)
        if r is None:
            print(f"  {name}: NOT FOUND")
            continue
        match = "OK" if r["dominant_sector"] == sector and abs(r["dominant_pct"] - pct) < 0.002 else "MISMATCH"
        print(f"  {name}: computed {r['dominant_sector']} {r['dominant_pct']:.3f} vs published {sector} {pct:.3f} [{match}]")


if __name__ == "__main__":
    main()
