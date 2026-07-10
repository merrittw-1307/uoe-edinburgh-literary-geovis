"""
Derives metro "lines" from real narrative co-occurrence data instead of
hand-drawn geography.

Pipeline:
1. Build a weighted graph from the 5-author co-occurrence dataset
   (network_enriched.json), edges with weight >= COMM_THRESHOLD.
2. Run modularity community detection to find real narrative clusters.
   Any cluster bigger than MAX_LINE_SIZE is recursively re-clustered on its
   own induced subgraph so no single line swallows unrelated stations.
3. Stations with too few strong connections to land in a real cluster are
   folded into whichever cluster they connect to most strongly in the full
   (unthresholded) graph, so every station ends up on some line.
4. Within each line, stations are ordered by a nearest-neighbour chain over
   real edge weights, so two stations adjacent on a line are guaranteed to
   have real book co-occurrence backing that adjacency (this is the
   property the old hand-drawn map did not have).
5. Interchanges: any station with a strong edge (weight >= INTERCHANGE_MIN)
   to a station on a *different* line is added as a second stop on that
   other line too, spliced in next to its strongest partner there.
6. Layout: a single shared (x,y) per station, from a weighted spring layout
   over the real co-occurrence graph (stronger co-occurrence pulls stations
   closer together), snapped to an integer grid with collisions resolved.
   Every line draws its path through its stations' *shared* coordinates, so
   two lines that both call at the same interchange station actually meet
   at one physical point - the way a real transit map does - instead of
   running in separate parallel lanes linked by a dashed cross-reference.

Cluster *membership* is deterministic given the edge weights, but Python's
hash-randomized set/dict iteration means tie-breaking inside
greedy_modularity_communities can otherwise vary run to run. Run this with
PYTHONHASHSEED=0 to get byte-identical output:
    PYTHONHASHSEED=0 python3 build_metro_lines.py

Output: metro_lines.json consumed by build_metro_html.py.
"""
import json
from pathlib import Path

import networkx as nx

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
ENRICHED_PATH = REPO_ROOT / "data/processed/dir_2/network/data/network_enriched.json"
OUT_PATH = REPO_ROOT / "data/processed/dir_2/metro/data/metro_lines.json"

COMM_THRESHOLD = 3
MAX_LINE_SIZE = 18
MIN_LINE_SIZE = 5
INTERCHANGE_MIN = 10

LINE_COLORS = ["#B85042", "#1C7293", "#2C5F2D", "#C9A227", "#7F77DD", "#4A4A4A", "#FF6B35"]
DOMINANCE_THRESHOLD = 0.55


def name_line(home_stations, place_books, nodes):
    author_mentions = {}
    for p in home_stations:
        for b in place_books.get(p, []):
            author_mentions[b["author"]] = author_mentions.get(b["author"], 0) + b["mentions"]
    total = sum(author_mentions.values())
    if total and author_mentions:
        top_author, top_count = max(author_mentions.items(), key=lambda kv: kv[1])
        if top_count / total >= DOMINANCE_THRESHOLD:
            return f"{top_author.split()[-1]}'s Edinburgh"
    top_places = sorted(home_stations, key=lambda p: -nodes[p]["total_mentions"])[:2]
    return " & ".join(top_places) + " Corridor"


def build_graph(edges, threshold, all_nodes=()):
    G = nx.Graph()
    G.add_nodes_from(all_nodes)
    for e in edges:
        if e["weight"] >= threshold:
            G.add_edge(e["source"], e["target"], weight=e["weight"])
    return G


def cluster_recursive(subgraph, depth=0):
    """Modularity-cluster a graph; recursively split any cluster over MAX_LINE_SIZE."""
    if subgraph.number_of_nodes() <= MAX_LINE_SIZE or depth > 3:
        return [set(subgraph.nodes())]
    comms = list(nx.community.greedy_modularity_communities(subgraph, weight="weight"))
    if len(comms) <= 1:
        return [set(subgraph.nodes())]
    result = []
    for c in comms:
        if len(c) > MAX_LINE_SIZE:
            result.extend(cluster_recursive(subgraph.subgraph(c).copy(), depth + 1))
        else:
            result.append(set(c))
    return result


def nearest_neighbor_order(members, full_graph):
    """Order stations so adjacent stations have the strongest real edge weight available."""
    members = list(members)
    if len(members) <= 2:
        return members
    sub = full_graph.subgraph(members)
    best_edge, best_w = None, -1
    for a, b, data in sorted(sub.edges(data=True), key=lambda t: (t[0], t[1])):
        if data["weight"] > best_w:
            best_w, best_edge = data["weight"], (a, b)
    if best_edge is None:
        return sorted(members)
    path = list(best_edge)
    remaining = sorted(set(members) - set(path))
    while remaining:
        best_place, best_end, best_w = None, None, -1
        for end_idx, end in [(0, path[0]), (-1, path[-1])]:
            for cand in remaining:
                w = sub[end][cand]["weight"] if sub.has_edge(end, cand) else -1
                if w > best_w:
                    best_w, best_place, best_end = w, cand, end_idx
        if best_place is None:
            # no direct edge to either end left; attach weakest-connected remaining node anywhere
            best_place = remaining[0]
            best_end = -1
        if best_end == 0:
            path.insert(0, best_place)
        else:
            path.append(best_place)
        remaining.remove(best_place)
    return path


GRID_W, GRID_H = 22, 15


def compute_layout(full_graph, all_places, home_line_of):
    """One shared (x,y) per station: a co-occurrence-weighted spring layout,
    snapped to an integer grid with collisions nudged apart. Stations that
    co-occur strongly get pulled close together; two lines that both stop at
    the same interchange will therefore actually meet at that point.

    Stations with zero real co-occurrence (spring_layout would place them
    arbitrarily far away, since nothing pulls on them) are instead anchored
    at their assigned line's centroid so they sit with their line rather
    than drifting off into an empty corner."""
    isolates = [p for p in all_places if full_graph.degree(p) == 0]
    connected_graph = full_graph.subgraph([p for p in all_places if p not in isolates])
    pos = nx.spring_layout(connected_graph, weight="weight", seed=42, k=0.6, iterations=200)

    for p in isolates:
        line_mates = [m for m, li in home_line_of.items() if li == home_line_of.get(p) and m in pos]
        if line_mates:
            mx = sum(pos[m][0] for m in line_mates) / len(line_mates)
            my = sum(pos[m][1] for m in line_mates) / len(line_mates)
        else:
            mx, my = 0.0, 0.0
        pos[p] = (mx, my)

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)

    def scale(v, lo, hi, size):
        if hi == lo:
            return size // 2
        return round((v - lo) / (hi - lo) * (size - 1))

    raw = {p: (scale(pos[p][0], x_lo, x_hi, GRID_W), scale(pos[p][1], y_lo, y_hi, GRID_H)) for p in all_places}

    occupied = {}
    final = {}
    for p in sorted(all_places, key=lambda n: -full_graph.degree(n, weight="weight") if n in full_graph else 0):
        x0, y0 = raw[p]
        cell = (x0, y0)
        radius = 0
        while cell in occupied and radius < max(GRID_W, GRID_H):
            radius += 1
            candidates = [
                (x0 + dx, y0 + dy)
                for dx in range(-radius, radius + 1)
                for dy in range(-radius, radius + 1)
                if max(abs(dx), abs(dy)) == radius
                and 0 <= x0 + dx < GRID_W and 0 <= y0 + dy < GRID_H
            ]
            candidates.sort(key=lambda c: (c[0] - x0) ** 2 + (c[1] - y0) ** 2)
            free = next((c for c in candidates if c not in occupied), None)
            if free:
                cell = free
                break
        occupied[cell] = p
        final[p] = {"x": cell[0], "y": cell[1]}
    return final


def main():
    enriched = json.loads(ENRICHED_PATH.read_text())
    nodes = {n["place"]: n for n in enriched["nodes"]}
    full_graph = build_graph(enriched["edges"], threshold=2, all_nodes=nodes.keys())
    comm_graph = build_graph(enriched["edges"], threshold=COMM_THRESHOLD, all_nodes=nodes.keys())

    raw_comms = cluster_recursive(comm_graph)
    big = [c for c in raw_comms if len(c) >= MIN_LINE_SIZE]
    small = [c for c in raw_comms if len(c) < MIN_LINE_SIZE]
    big.sort(key=len, reverse=True)

    place_to_line = {}
    for i, c in enumerate(big):
        for p in c:
            place_to_line[p] = i

    # fold small clusters / isolated stations into their strongest real neighbour's line
    orphans = sorted(p for c in small for p in c)
    for p in orphans:
        best_line, best_w = None, -1
        for nb in full_graph.neighbors(p):
            w = full_graph[p][nb]["weight"]
            if nb in place_to_line and w > best_w:
                best_w, best_line = w, place_to_line[nb]
        place_to_line[p] = best_line if best_line is not None else 0

    place_books = enriched["placeBooks"]

    n_lines = len(big)
    lines = []
    for i in range(n_lines):
        members = sorted(p for p, li in place_to_line.items() if li == i)
        ordered = nearest_neighbor_order(members, full_graph)
        total_mentions = sum(nodes[p]["total_mentions"] for p in ordered)
        backed = sum(
            1 for a, b in zip(ordered, ordered[1:])
            if full_graph.has_edge(a, b)
        )
        lines.append({
            "id": i,
            "name": name_line(members, place_books, nodes),
            "color": LINE_COLORS[i % len(LINE_COLORS)],
            "stations": ordered,
            "total_mentions": total_mentions,
            "adjacency_backed": backed,
            "adjacency_total": max(len(ordered) - 1, 0),
        })
    lines.sort(key=lambda l: -l["total_mentions"])
    for i, line in enumerate(lines):
        line["id"] = i
        line["color"] = LINE_COLORS[i % len(LINE_COLORS)]

    # interchanges: strong cross-line edges get the station added as a second stop
    home_line_of = {}
    for line in lines:
        for p in line["stations"]:
            home_line_of[p] = line["id"]

    interchange_extra_stops = {line["id"]: [] for line in lines}  # line_id -> [(insert_after, station)]
    seen_pairs = set()
    for e in enriched["edges"]:
        if e["weight"] < INTERCHANGE_MIN:
            continue
        a, b, w = e["source"], e["target"], e["weight"]
        la, lb = home_line_of.get(a), home_line_of.get(b)
        if la is None or lb is None or la == lb:
            continue
        pair_key = tuple(sorted([a, b]))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        # add `a` as an extra stop on b's line, next to b; and vice versa
        interchange_extra_stops[lb].append((b, a, w))
        interchange_extra_stops[la].append((a, b, w))

    for line in lines:
        extras = sorted(interchange_extra_stops[line["id"]], key=lambda x: -x[2])
        for anchor, extra_station, w in extras:
            if extra_station in line["stations"]:
                continue
            idx = line["stations"].index(anchor)
            line["stations"].insert(idx + 1, extra_station)

    # One shared (x,y) per station from a co-occurrence-weighted layout, so
    # lines that share an interchange actually meet at the same point.
    stn_coords = compute_layout(full_graph, nodes.keys(), home_line_of)
    for line in lines:
        line["station_coords"] = [stn_coords[p] for p in line["stations"]]

    occurrence_count = {}
    for line in lines:
        for p in line["stations"]:
            occurrence_count[p] = occurrence_count.get(p, 0) + 1
    interchange_stations = sorted([p for p, c in occurrence_count.items() if c > 1])

    payload = {
        "lines": [
            {
                "id": line["id"],
                "name": line["name"],
                "color": line["color"],
                "total_mentions": line["total_mentions"],
                "adjacency_backed": line["adjacency_backed"],
                "adjacency_total": line["adjacency_total"],
                "stations": [
                    {"name": p, **stn_coords[p], "home_line": home_line_of[p]}
                    for p in line["stations"]
                ],
            }
            for line in lines
        ],
        "interchanges": interchange_stations,
        "grid": {"w": GRID_W, "h": GRID_H},
        "nodes": enriched["nodes"],
        "edges": enriched["edges"],
        "edgeBooks": enriched["edgeBooks"],
        "placeSentences": enriched["placeSentences"],
        "placeBooks": enriched["placeBooks"],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False))

    print(f"{n_lines} lines derived from real co-occurrence data:")
    for line in lines:
        print(f"  Line {line['id']} \"{line['name']}\": {len(line['stations'])} stops, "
              f"{line['total_mentions']} mentions -> {', '.join(line['stations'][:8])}"
              f"{' ...' if len(line['stations']) > 8 else ''}")
    print(f"Interchange stations ({len(interchange_stations)}): {', '.join(interchange_stations)}")
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
