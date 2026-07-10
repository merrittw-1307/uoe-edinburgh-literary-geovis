"""
Renders one illustrative full metro.html snapshot (20 authors) for a
screenshot, reusing the exact interchange-detection, spring-layout,
octilinear-correction, and label-placement code from build_metro_lines.py
and build_metro_html.py - no logic is duplicated, only the author-list
input and a couple of module-level path constants are swapped.
"""
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
METRO_PY_DIR = REPO_ROOT / "data/processed/dir_2/metro/py"
ALL_AUTHORS_NETWORK = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_network.json"
SCALE_DATA_DIR = REPO_ROOT / "data/processed/scale_exploration/data"
SCALE_D3_DIR = REPO_ROOT / "data/processed/scale_exploration/d3"

N_AUTHORS = 20


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    metro_lines = load_module("build_metro_lines", METRO_PY_DIR / "build_metro_lines.py")
    scale_test = load_module("metro_scale_test", Path(__file__).parent / "metro_scale_test.py")

    payload = json.loads(ALL_AUTHORS_NETWORK.read_text())
    mentions = payload["mentions"]
    author_totals = {}
    for m in mentions:
        author_totals[m["author"]] = author_totals.get(m["author"], 0) + m["mentions"]
    top_authors = sorted(author_totals, key=lambda a: -author_totals[a])[:N_AUTHORS]

    nodes, edges, place_books = scale_test.build_nodes_edges(mentions, top_authors)
    node_map = {n["place"]: n for n in nodes}
    lines = scale_test.run_pipeline(nodes, edges, place_books)

    full_graph = metro_lines.build_graph(edges, threshold=2, all_nodes=node_map.keys())
    home_line_of = {}
    for i, line in enumerate(lines):
        for p in line["stations"]:
            home_line_of[p] = i

    interchange_extra_stops = {i: [] for i in range(len(lines))}
    seen_pairs = set()
    for e in edges:
        if e["weight"] < metro_lines.INTERCHANGE_MIN:
            continue
        a, b, w = e["source"], e["target"], e["weight"]
        la, lb = home_line_of.get(a), home_line_of.get(b)
        if la is None or lb is None or la == lb:
            continue
        pair_key = tuple(sorted([a, b]))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        interchange_extra_stops[lb].append((b, a, w))
        interchange_extra_stops[la].append((a, b, w))

    for i, line in enumerate(lines):
        extras = sorted(interchange_extra_stops[i], key=lambda x: -x[2])
        for anchor, extra_station, w in extras:
            if extra_station in line["stations"]:
                continue
            if anchor not in line["stations"]:
                continue
            idx = line["stations"].index(anchor)
            line["stations"].insert(idx + 1, extra_station)

    stn_coords = metro_lines.compute_layout(full_graph, node_map.keys(), home_line_of)

    occurrence_count = {}
    for line in lines:
        for p in line["stations"]:
            occurrence_count[p] = occurrence_count.get(p, 0) + 1
    interchange_stations = sorted([p for p, c in occurrence_count.items() if c > 1])

    edge_books = {}
    for e in edges:
        key = f"{e['source']}|||{e['target']}"
        edge_books[key] = []

    result = {
        "lines": [
            {
                "id": i,
                "name": line["name"],
                "color": metro_lines.LINE_COLORS[i % len(metro_lines.LINE_COLORS)],
                "total_mentions": line["total_mentions"],
                "adjacency_backed": line["adjacency_backed"],
                "adjacency_total": line["adjacency_total"],
                "stations": [
                    {"name": p, **stn_coords[p], "home_line": home_line_of[p]}
                    for p in line["stations"]
                ],
            }
            for i, line in enumerate(lines)
        ],
        "interchanges": interchange_stations,
        "grid": {"w": metro_lines.GRID_W, "h": metro_lines.GRID_H},
        "nodes": nodes,
        "edges": edges,
        "edgeBooks": edge_books,
        "placeSentences": {},
        "placeBooks": {},
    }

    out_json = SCALE_DATA_DIR / f"metro_scale_{N_AUTHORS}authors.json"
    out_json.write_text(json.dumps(result, ensure_ascii=False))
    print(f"Wrote {out_json}")

    build_html = load_module("build_metro_html", METRO_PY_DIR / "build_metro_html.py")
    build_html.DATA_PATH = out_json
    build_html.OUT_PATH = SCALE_D3_DIR / f"metro_scale_explore_{N_AUTHORS}authors.html"
    build_html.BACKUP_PATH = SCALE_D3_DIR / "_unused_backup.html"
    build_html.main()


if __name__ == "__main__":
    main()
