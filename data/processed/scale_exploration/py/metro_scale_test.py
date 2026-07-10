"""
Re-runs the metro-map community-detection pipeline (build_metro_lines.py)
at different author-count scales, reusing its clustering/sequencing/naming
functions directly rather than duplicating them.

Unlike the other five scale-exploration tools, this one is not a live
interactive HTML page: community detection, spring embedding, and
octilinear correction are batch Python operations (networkx), not
something to reasonably re-implement in client-side JS in the time
available. Instead this script runs the real pipeline at each benchmark N
and reports the same structural diagnostics (line count, size
distribution, adjacency-backed ratio) used for the five-author version, so
the comparison is apples-to-apples. One illustrative N (20 authors) is also
rendered as a full HTML file via build_metro_html.py for a screenshot.
"""
import importlib.util
import json
import sys
import time
from itertools import combinations
from pathlib import Path

import networkx as nx

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
METRO_PY_DIR = REPO_ROOT / "data/processed/dir_2/metro/py"
ALL_AUTHORS_NETWORK = REPO_ROOT / "data/processed/scale_exploration/data/all_authors_network.json"
OUT_JSON_DIR = REPO_ROOT / "data/processed/scale_exploration/data"
OUT_HTML_DIR = REPO_ROOT / "data/processed/scale_exploration/d3"

TOP_N_PLACES_PER_AUTHOR = 15
MIN_EDGE_WEIGHT = 2

# Import build_metro_lines.py as a module without running its __main__ block.
spec = importlib.util.spec_from_file_location("build_metro_lines", METRO_PY_DIR / "build_metro_lines.py")
metro_lines = importlib.util.module_from_spec(spec)
sys.modules["build_metro_lines"] = metro_lines
spec.loader.exec_module(metro_lines)


def build_nodes_edges(mentions, author_list):
    rows = [m for m in mentions if m["author"] in author_list]
    by_author_place = {}
    for r in rows:
        key = (r["author"], r["place"])
        by_author_place[key] = by_author_place.get(key, 0) + r["mentions"]

    top_places = set()
    by_author = {}
    for (author, place), mentions_sum in by_author_place.items():
        by_author.setdefault(author, []).append((place, mentions_sum))
    for author, places in by_author.items():
        places.sort(key=lambda x: -x[1])
        top_places.update(p for p, _ in places[:TOP_N_PLACES_PER_AUTHOR])

    filtered = [r for r in rows if r["place"] in top_places]
    node_mentions = {}
    for r in filtered:
        node_mentions[r["place"]] = node_mentions.get(r["place"], 0) + r["mentions"]

    by_doc = {}
    for r in filtered:
        by_doc.setdefault(r["document_id"], set()).add(r["place"])
    edge_weight = {}
    for places in by_doc.values():
        for p1, p2 in combinations(sorted(places), 2):
            edge_weight[(p1, p2)] = edge_weight.get((p1, p2), 0) + 1

    nodes = [{"place": p, "total_mentions": m} for p, m in node_mentions.items()]
    edges = [{"source": p1, "target": p2, "weight": w} for (p1, p2), w in edge_weight.items() if w >= MIN_EDGE_WEIGHT]

    place_books = {}
    for r in filtered:
        place_books.setdefault(r["place"], []).append({"author": r["author"], "mentions": r["mentions"]})

    return nodes, edges, place_books


def run_pipeline(nodes, edges, place_books):
    node_map = {n["place"]: n for n in nodes}
    full_graph = metro_lines.build_graph(edges, threshold=2, all_nodes=node_map.keys())
    comm_graph = metro_lines.build_graph(edges, threshold=metro_lines.COMM_THRESHOLD, all_nodes=node_map.keys())

    raw_comms = metro_lines.cluster_recursive(comm_graph)
    big = [c for c in raw_comms if len(c) >= metro_lines.MIN_LINE_SIZE]
    small = [c for c in raw_comms if len(c) < metro_lines.MIN_LINE_SIZE]
    big.sort(key=len, reverse=True)

    place_to_line = {}
    for i, c in enumerate(big):
        for p in c:
            place_to_line[p] = i

    orphans = sorted(p for c in small for p in c)
    for p in orphans:
        best_line, best_w = None, -1
        for nb in full_graph.neighbors(p):
            w = full_graph[p][nb]["weight"]
            if nb in place_to_line and w > best_w:
                best_w, best_line = w, place_to_line[nb]
        place_to_line[p] = best_line if best_line is not None else (0 if big else None)

    lines = []
    for i in range(len(big)):
        members = sorted(p for p, li in place_to_line.items() if li == i)
        if not members:
            continue
        ordered = metro_lines.nearest_neighbor_order(members, full_graph)
        total_mentions = sum(node_map[p]["total_mentions"] for p in ordered)
        backed = sum(1 for a, b in zip(ordered, ordered[1:]) if full_graph.has_edge(a, b))
        lines.append({
            "name": metro_lines.name_line(members, place_books, node_map),
            "stations": ordered,
            "total_mentions": total_mentions,
            "adjacency_backed": backed,
            "adjacency_total": max(len(ordered) - 1, 0),
        })
    lines.sort(key=lambda l: -l["total_mentions"])
    return lines


def main():
    payload = json.loads(ALL_AUTHORS_NETWORK.read_text())
    mentions = payload["mentions"]
    all_author_totals = {}
    for m in mentions:
        all_author_totals[m["author"]] = all_author_totals.get(m["author"], 0) + m["mentions"]
    by_mentions = sorted(all_author_totals, key=lambda a: -all_author_totals[a])

    scenarios = {
        "2": ["Alexander McCall Smith", "Irvine Welsh"],
        "5 (baseline)": ["Alexander McCall Smith", "Irvine Welsh", "John Gibson Lockhart", "Walter Scott", "Robert Louis Stevenson"],
        "20": by_mentions[:20],
        "50": by_mentions[:50],
    }

    results = {}
    for label, authors in scenarios.items():
        t0 = time.time()
        nodes, edges, place_books = build_nodes_edges(mentions, authors)
        elapsed_data = time.time() - t0
        t0 = time.time()
        lines = run_pipeline(nodes, edges, place_books)
        elapsed_cluster = time.time() - t0

        total_backed = sum(l["adjacency_backed"] for l in lines)
        total_adj = sum(l["adjacency_total"] for l in lines)
        results[label] = {
            "n_authors": len(authors),
            "n_nodes": len(nodes),
            "n_edges": len(edges),
            "n_lines": len(lines),
            "line_sizes": [len(l["stations"]) for l in lines],
            "line_names": [l["name"] for l in lines],
            "adjacency_backed": total_backed,
            "adjacency_total": total_adj,
            "adjacency_pct": round(100 * total_backed / total_adj, 1) if total_adj else None,
            "data_gen_seconds": round(elapsed_data, 3),
            "cluster_seconds": round(elapsed_cluster, 3),
        }
        print(f"\n=== {label} authors ===")
        print(f"  {len(nodes)} nodes, {len(edges)} edges -> {len(lines)} lines, sizes {results[label]['line_sizes']}")
        print(f"  names: {results[label]['line_names']}")
        print(f"  adjacency backed: {total_backed}/{total_adj} ({results[label]['adjacency_pct']}%)")
        print(f"  timing: data {elapsed_data:.3f}s, clustering {elapsed_cluster:.3f}s")

    out_path = OUT_JSON_DIR / "metro_scale_results.json"
    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
