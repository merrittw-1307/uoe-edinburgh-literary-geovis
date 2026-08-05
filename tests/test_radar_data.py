"""
Regression tests for the five-author sector-distribution data behind the
radar chart (dissertation Table "Five Test Authors"). Guards the shipped
radar_data_v2.csv against drifting from the dominant-sector percentages
the dissertation reports for each author.
"""
import csv

EXPECTED_DOMINANT_SECTOR = {
    "Alexander McCall Smith": ("New Town", 43.6),
    "Irvine Welsh": ("Leith", 44.3),
    "John Gibson Lockhart": ("New Town", 25.9),
    "Walter Scott": ("Old Town", 32.0),
    "Robert Louis Stevenson": ("Old Town", 20.7),
}


def _load_rows(repo_root):
    path = repo_root / "data/processed/dir_1/radar/data/radar_data_v2.csv"
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sector_columns(rows):
    return [k for k in rows[0].keys() if k != "author"]


def test_five_authors_present(repo_root):
    rows = _load_rows(repo_root)
    authors = {r["author"] for r in rows}
    assert authors == set(EXPECTED_DOMINANT_SECTOR.keys())


def test_each_author_row_sums_to_one(repo_root):
    rows = _load_rows(repo_root)
    sectors = _sector_columns(rows)
    for row in rows:
        total = sum(float(row[s]) for s in sectors)
        assert abs(total - 1.0) < 0.01, f"{row['author']}'s sector proportions sum to {total}, not ~1.0"


def test_dominant_sector_matches_dissertation(repo_root):
    rows = _load_rows(repo_root)
    sectors = _sector_columns(rows)
    by_author = {r["author"]: r for r in rows}

    for author, (expected_sector, expected_pct) in EXPECTED_DOMINANT_SECTOR.items():
        row = by_author[author]
        dominant = max(sectors, key=lambda s: float(row[s]))
        assert dominant == expected_sector, f"{author}: expected dominant sector {expected_sector}, got {dominant}"
        actual_pct = float(row[dominant]) * 100
        assert abs(actual_pct - expected_pct) < 0.2, (
            f"{author}: expected {expected_sector} at {expected_pct}%, got {actual_pct:.1f}%"
        )
