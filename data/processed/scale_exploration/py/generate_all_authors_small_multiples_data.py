"""
Per-author (place, lat, lon, mentions) data for all 408 authors, for
small_multiples_scale_explore.html. Unlike the sector/co-occurrence
exports, this one needs coordinates, so it joins api_location directly
rather than reusing the other scale-exploration JSON files.

Restricted to the same Edinburgh-core bounding box as the original
small_multiples.html (Finding 5), for the same reason: a handful of
authors (Scott especially) reference locations far outside the city centre
that would otherwise compress the core-area bubbles into an unreadable
band.
"""
import json
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

def _find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("Could not locate repository root (no .git directory found)")


REPO_ROOT = Path(os.environ["DISSERTATION_REPO_ROOT"]) if os.environ.get("DISSERTATION_REPO_ROOT") else _find_repo_root(Path(__file__).resolve())
OUT_PATH = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_small_multiples.json"

LAT_MIN, LAT_MAX = 55.85, 56.02
LON_MIN, LON_MAX = -3.35, -3.05
TOP_N_PLACES = 20

engine = create_engine(os.environ.get("LITLONG_DB_URL", "postgresql://localhost:5432/litlong_edinburgh"))

QUERY = """
SELECT
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    l.text AS place,
    l.lat,
    l.lon,
    COUNT(lm.id) AS mentions
FROM api_locationmention lm
JOIN api_location l ON lm.location_id = l.id
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
WHERE l.lat IS NOT NULL AND l.lon IS NOT NULL
GROUP BY a.id, a.forenames, a.surname, l.id, l.text, l.lat, l.lon
"""


def main() -> None:
    df = pd.read_sql(QUERY, engine)
    df = df.groupby(["author", "place", "lat", "lon"], as_index=False)["mentions"].sum()
    in_core = df[(df.lat >= LAT_MIN) & (df.lat <= LAT_MAX) & (df.lon >= LON_MIN) & (df.lon <= LON_MAX)]
    print(f"Loaded {len(df)} (author, place) rows with coordinates, {len(in_core)} within the Edinburgh core bbox")

    records = []
    for author, group in in_core.groupby("author"):
        top = group.sort_values("mentions", ascending=False).head(TOP_N_PLACES)
        places = [
            {"place": r.place, "lat": float(r.lat), "lon": float(r.lon), "mentions": int(r.mentions)}
            for r in top.itertuples()
        ]
        records.append({
            "author": author,
            "total_mentions": int(group["mentions"].sum()),
            "places": places,
        })

    records.sort(key=lambda r: -r["total_mentions"])
    records = [r for r in records if r["places"]]

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(records, ensure_ascii=False))
    print(f"Wrote {len(records)} authors to {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
