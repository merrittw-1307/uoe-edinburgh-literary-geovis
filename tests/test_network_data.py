"""
Regression tests for the five-author document-level co-occurrence data
(dissertation Finding 3/4, Appendix C). Guards the shipped network_edges.csv
against silently drifting from the numbers the dissertation reports: 403
pairs at weight >= 2, with Leith/Princes Street the strongest at weight 28.
"""
import csv


def _load_edges(repo_root):
    path = repo_root / "data/processed/dir_2/network/data/network_edges.csv"
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_edge_count_matches_dissertation(repo_root):
    edges = _load_edges(repo_root)
    assert len(edges) == 403


def test_all_edges_meet_minimum_weight(repo_root):
    edges = _load_edges(repo_root)
    assert all(int(e["weight"]) >= 2 for e in edges)


def test_strongest_pair_is_leith_princes_street(repo_root):
    edges = _load_edges(repo_root)
    strongest = max(edges, key=lambda e: int(e["weight"]))
    pair = {strongest["source"], strongest["target"]}
    assert pair == {"Leith", "Princes Street"}
    assert int(strongest["weight"]) == 28


def test_no_duplicate_or_self_pairs(repo_root):
    edges = _load_edges(repo_root)
    seen = set()
    for e in edges:
        assert e["source"] != e["target"], "an edge should not connect a place to itself"
        key = frozenset((e["source"], e["target"]))
        assert key not in seen, f"duplicate edge: {e['source']} / {e['target']}"
        seen.add(key)
