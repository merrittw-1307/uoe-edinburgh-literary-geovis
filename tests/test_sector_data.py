"""
Regression tests for the 14-sector spatial classification (dissertation
Section 3.4 / Appendix B). These guard the numbers actually reported in the
dissertation against silent drift if location_sectors_v2.csv is ever
regenerated: 2,135 places total, 1,480 exact point-in-polygon matches, 423
nearest-neighbour assignments, 232 excluded as "Outer Scotland".
"""
import csv

NAMED_SECTORS = {
    "Almond", "Craigentinny/Duddingston", "Forth", "Inverleith", "Leith",
    "Liberton/Gilmerton", "Pentlands", "Portobello/Craigmillar",
    "South Central", "South West", "Western Edinburgh",
    "Old Town", "New Town", "Canongate",
}


def _load_rows(repo_root):
    path = repo_root / "data/processed/sectors/location_sectors_v2.csv"
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_total_place_count(repo_root):
    rows = _load_rows(repo_root)
    assert len(rows) == 2135


def test_method_breakdown_matches_dissertation(repo_root):
    rows = _load_rows(repo_root)
    exact = sum(1 for r in rows if r["method"] == "exact")
    outside = sum(1 for r in rows if r["method"] == "outside")
    nearest = sum(1 for r in rows if r["method"].startswith("nearest"))

    assert exact == 1480
    assert outside == 232
    assert nearest == 423
    assert exact + outside + nearest == len(rows)


def test_sectors_are_the_documented_fourteen_plus_outer_scotland(repo_root):
    rows = _load_rows(repo_root)
    sectors = {r["sector"] for r in rows}
    assert sectors == NAMED_SECTORS | {"Outer Scotland"}


def test_outer_scotland_rows_are_exactly_the_outside_method_rows(repo_root):
    rows = _load_rows(repo_root)
    outer = {r["id"] for r in rows if r["sector"] == "Outer Scotland"}
    outside_method = {r["id"] for r in rows if r["method"] == "outside"}
    assert outer == outside_method
