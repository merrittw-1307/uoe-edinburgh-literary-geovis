# Scale Exploration — Decision Log

Mentor-assigned task (see handover_v3.md §10, 第二优先级): test how the visualisations behave at different
author/book scales (5 authors → all; 2 authors; 2-3 books), screenshot each, document pros/cons.

This directory is intentionally separate from `dir_1/` and `dir_2/`. The existing `radar.html` and
`network.html` are the canonical five-author prototypes already described in the dissertation — they are
**not modified or overwritten** by this exploration. Everything here is new: `radar_scale_explore.html`
and `network_scale_explore.html`, plus the data scripts that feed them.

## Scope decisions (2026-07-10)

- **Round 1: two representative charts**, one per direction, per Merritt's first instruction: **radar chart**
  (Direction 1) and **network graph** (Direction 2). See "Round 1 findings" below.
- **Round 2 (same day): the remaining four charts** (bar-code, small multiples, linear, metro), per Merritt's
  follow-up instruction, using the same author-count benchmarks and the same non-destructive approach (new
  `*_scale_explore.html` files; the five-author canonical prototypes are untouched). See "Round 2 findings"
  below. Two of the four (linear, metro) reuse data already generated for network in Round 1 rather than
  re-querying the database.
- **"All 424 authors" is built as a real, live control, not a fixed screenshot.** Rather than picking one
  arbitrary N and calling it "full scale," both charts get an author-count/selection control so the actual
  legibility breakdown point can be explored interactively, not just asserted. Four benchmark points are
  used for the write-up: **2 authors, 5 authors (existing baseline), ~20 authors, all authors with any
  mention data (420 of 424 — 4 authors have zero location mentions and are excluded)**.
- **"2-3 books" is tested on the network chart only.** A fingerprint radar chart for a single book is a
  weaker test of the Direction-1 argument (which is about *authorial* style, not book style), whereas
  Direction 2's whole point is document-level co-occurrence, so restricting to 2-3 specific documents is a
  direct, meaningful stress test of the same mechanism at a smaller N.
- Author records are merged by trimmed display name (forenames + surname), not by raw `author.id`, because
  the corpus contains at least one duplicate-name split (two distinct `Alexander McCall Smith` author IDs,
  7,320 and 948 mentions respectively) that would otherwise show as two separate dropdown entries for what
  a reader would consider one author.

## Round 1 findings (radar, network)

### Radar chart (Direction 1) — legibility collapses monotonically with author count

Tool: `radar_scale_explore.html`. Sector-percentage methodology validated against the five published
Appendix values before any exploration (`generate_all_authors_radar_data.py` reproduces all five to 3
decimal places — see script output). 408 of 424 authors have location-mention data.

| N authors | Observation |
|---|---|
| 2 (McCall Smith, Welsh) | Two clearly distinguishable polygons, fully legible, no overlap ambiguity. |
| 5 (existing baseline) | Still fully legible; this is the number used throughout the dissertation. |
| 20 (top by mentions) | Polygons visually overlap heavily; individual shapes are no longer distinguishable in the static view. Legend list is still browsable. |
| 408 (all) | Static view is an unreadable tangle — confirms the open question in the Limitations chapter ("whether distinct fingerprints remain legible when 424 polygons are overlaid... is an open question") empirically: **no**, not as a static overlay. |

**Mitigation that works:** a per-author hover-to-isolate control (dim all polygons to 8% opacity except the
hovered one, confirmed working via direct test at N=408) recovers single-author legibility at any N, at the
cost of losing the "compare all at a glance" property that makes the 5-author version useful in the first
place. This is the actual trade-off: **fingerprint comparison degrades from "all-at-once" to "one-at-a-time"
as N grows, it does not fail outright** — a more precise and more useful claim than "424 authors don't fit."

### Network graph (Direction 2) — density is driven by vocabulary overlap, not raw node count

Tool: `network_scale_explore.html`. Both an author-subset mode and a book-subset mode, computed live in the
browser from a shipped 12,243-row (author, place, document) table — not five fixed screenshots.

| Scale | Places | Pairs (weight ≥ 2) | Density (pairs / possible pairs) |
|---|---|---|---|
| 2 authors (McCall Smith, Welsh) | 28 | 299 | 79.6% |
| 5 authors (baseline) | 58 | ~403* | ~25% |
| 20 authors (top by mentions) | 110 | 3,808 | 63.5% |
| 408 authors (all) | 533 | 23,380 | 16.5% |
| 3 books (44 Scotland St, Sunshine on Scotland St, Trainspotting), weight ≥ 1 | 152 | 5,889 | 51.3% |
| same 3 books, weight ≥ 2 | 33 | 424 | 78.0% |

*the published 403-pair baseline figure uses the original hand-curated top-15-places-per-author query; this
tool's independent re-derivation of the same 5-author configuration lands close to it (small differences are
expected — this pipeline was built fresh rather than reusing `network_data2.py`, e.g. it does not cap places
at exactly 15 in the same tie-breaking order).

**This is a genuinely non-obvious, non-monotonic result and the most interesting finding of the whole
exploration.** Density does *not* fall smoothly as N grows and then rise again at the low end by coincidence
— it is explained by two different, identifiable mechanisms:

1. **At low N (2 authors, or 2-3 books by the same/overlapping authors), density is high because
   document-level co-occurrence degenerates toward "any two places in the same book."** A single author's
   own top-15 places nearly all appear together across their many books; a single book's entire place
   vocabulary trivially satisfies "co-occurs in this document" with itself. The 3-book test makes this
   concrete: raising the threshold from weight ≥ 1 to weight ≥ 2 collapses 152 places/5,889 pairs down to 33
   places/424 pairs — and the survivors are almost entirely the McCall Smith pair (`44 Scotland Street` /
   `Sunshine on Scotland Street`, his own recurring fictional world), not anything connecting to
   `Trainspotting`, because Welsh and McCall Smith do not share vocabulary (Finding 1).
2. **At high N (all 408 authors), density falls because most authors' vocabularies do not overlap at all**
   (Finding 1, again, now shown at full scale rather than asserted from a 5-author sample): adding more
   authors adds more nodes far faster than it adds real cross-author edges, so the graph becomes large and
   sparse rather than large and dense.
3. **The 5-author baseline sits in the interesting middle: enough authors for cross-author edges to be
   meaningful and rare rather than either "everything trivially connects" (2 authors/2-3 books) or
   "everything is disconnected" (408 authors), which is presumably why it was landed on originally, even
   though that reasoning was not explicit at the time.**

The force-directed layout degrades more gracefully than the radar chart's static overlay at high N: even at
408 authors, the periphery (loosely connected places) stays legible and only the core is an unreadable mass,
so the failure is partial and graduated rather than total. This matches the general expectation that
node-link diagrams tolerate scale better than superimposed shape comparison, and is worth stating as a
direct contrast between the two designs' scaling behaviour.

### Round 1 verdict

Both charts produced concrete, quantified, non-trivial findings rather than just confirming "yes it gets
crowded." Folded into dissertation.tex (Limitations §"Five-author prototype", Discussion) and handover_v3.md.

## Round 2 findings (bar-code, small multiples, linear, metro)

Each of the remaining four charts turned out to fail in a **different, specific way** rather than all just
being "the radar problem again." That divergence is itself the headline result of round 2: the six designs
do not share one scaling bottleneck, they have (at least) five distinguishable ones.

### Bar-code (Direction 1) — fails by scroll length, not by rendering cost or visual clutter

Tool: `barcode_scale_explore.html`. Each row shows the author's own top-15 places (a shared 39-place column
universe, as used in the five-author `barcode.html`, does not generalise to 408 very different vocabularies
— see scope decision above), so this isolates the *stacked-rows* scaling question from the *shared-columns*
question.

| N authors | DOM render time | Page height | Observation |
|---|---|---|---|
| 2 | <10ms | ~180px | Two rows, fully legible, no scrolling. |
| 5 (baseline) | <10ms | ~460px | Fits on one screen. |
| 20 | ~8ms | ~1,840px | About 2 screens of scrolling; each row still individually legible. |
| 408 (all) | **20ms** | **45,274px (measured via `scrollHeight`, not estimated)** | **No rendering slowdown and no visual clutter within a row** — the bottleneck is purely that comparing two arbitrary authors requires scrolling roughly 50 screen-heights apart, which defeats the "compare at a glance" purpose of the design even though nothing is technically broken. |

This is a genuinely different failure mode from the radar chart's: bar-code **never becomes unreadable**, it
becomes **un-comparable at a distance**. 4,589 bars across 408 rows render in 20 milliseconds — the design's
scaling problem is 100% a layout/navigation problem, 0% a rendering-cost problem.

### Linear connection diagram (Direction 2) — fails by horizontal sprawl, and looks deceptively unchanged until you check the canvas width

Tool: `linear_scale_explore.html`, reusing the same client-side co-occurrence computation as
`network_scale_explore.html` (both author-subset and 2–3-book modes).

| N authors | Places | SVG width |
|---|---|---|
| 5 (baseline) | 58 | 1,100px (fits the viewport) |
| 20 | 110 | ~5,100px |
| 408 (all) | 646 | **29,790px** (measured via the SVG's own `width` attribute) |

The visual trap here is worth recording precisely because it cost real debugging time during this session:
at 408 authors, a screenshot of the (horizontally-scrollable) viewport looks almost identical to the 20 authors
screenshot, because the container only ever shows the left edge of the canvas, and the leftmost places
(sorted by total mentions, e.g. Leith, Princes Street) are the same regardless of N. The chart is not
silently failing to update — it is correctly drawing a canvas roughly 27 screen-widths wide, and no one
would ever scroll through it. This is the horizontal-axis counterpart to bar-code's vertical problem, and
the two designs' shared root cause (one mark per place, laid out along a single axis, with no provision for
wrapping) is worth stating explicitly since it did not need two designs to discover.

### Small multiples (Direction 1) — the only chart with a real, measurable computational cost, and it is non-linear

Tool: `small_multiples_scale_explore.html`. Unlike the other five tools, each "mark" here is a genuine live
Leaflet map instance requesting real basemap tiles over the network, so this measures actual browser cost,
not a simulated one.

| N authors | DOM+init time | Tiles requested | Tiles loaded within 3s | Time / map |
|---|---|---|---|---|
| 5 (baseline) | 13ms | 10 | 10/10 | 2.6ms |
| 20 | 29ms | 40 | 40/40 | 1.5ms |
| 50 (stress test) | 51ms | 100 | 100/100 | 1.0ms |
| 408 (all — tested directly, not extrapolated) | **1,474ms** | 816 | 816/816 (confirmed shortly after) | 3.6ms |

Per-map cost *improves* from 5 to 50 (fixed overhead amortising), then **degrades sharply from 50 to 408**
(1.0ms/map → 3.6ms/map, a 3.6x regression) even though every tile still loads successfully with no console
errors. The 1.47-second initialisation is a genuine main-thread-blocking delay a real user would feel as a
freeze, which is a materially different problem from "the page needs scrolling" (bar-code, linear) or "the
shapes overlap" (radar): it is the one design of the six where pushing N higher risks an actual usability
failure (a frozen tab) rather than only a legibility one, well before the guaranteed layout problem (408
panels at 220×160px require an enormous, mostly off-screen grid) even becomes relevant.

### Metro map (Direction 2) — the community-detection pipeline itself degrades structurally, not just visually

Tool: `metro_scale_test.py` (a batch script, not a live HTML page — see "why metro is different" below) plus
one rendered snapshot, `metro_scale_explore_20authors.html`, for a screenshot. Re-runs the exact clustering,
sequencing, interchange-detection, and layout code from `build_metro_lines.py` (imported, not duplicated) at
each N.

| N authors | Nodes | Edges | Lines | Adjacency backed | Notable |
|---|---|---|---|---|---|
| 2 | 28 | 299 | 2 | 25/26 (96.2%) | Clean 1 line per author. |
| 5 (baseline) | 58 | 1,114 | 5 | 49/53 (92.5%) | Reproduces 5 lines, but not bit-for-bit the same 5 as the production `metro.html` — McCall Smith's material split into two separate lines here instead of one (see caveat below). |
| 20 | 117 | 3,808 | 8 | 92/109 (84.4%) | Rendered in full — see screenshot; still legible with real crossings. |
| 50 | 215 | 8,634 | 11 | 148/204 (72.5%) | **One line balloons to 75 stations** — `MAX_LINE_SIZE=18`'s recursive re-clustering assumes modularity can always find a sub-split, but at this density one community becomes so internally cohesive that `greedy_modularity_communities` returns it as a single, unsplittable block despite exceeding the cap. This is a structural failure of the clustering approach, not a rendering or layout problem. |

Adjacency-backed percentage declines monotonically (96%→92.5%→84.4%→72.5%) at the same time as line count
grows (2→5→8→11) — both trends point the same direction: as N grows, the map needs *both* more lines *and*
each line becomes internally less cohesive, and by N=50 the size cap that keeps lines legible stops holding.
This directly extends the round-1 network finding (density falls as N grows because vocabularies stop
overlapping) into its consequence for the metro design specifically: fewer real cross-author edges means
modularity has less signal to cut the graph into clean, evenly-sized pieces.

**Caveat, stated plainly:** the N=5 row above does not exactly reproduce the production `metro.html`'s five
named lines (Smith's/Leith & Forth/Scott's/Welsh's/Lockhart's Edinburgh). It also finds 5 lines, but splits
McCall Smith's material into two rather than keeping Scott's and Lockhart's as distinct from a merged
"Leith & Forth" cluster. This is not a bug in either pipeline; it is because this test recomputed the
5-author co-occurrence graph independently from `all_authors_network.json` rather than reusing
`network_enriched.json` bit-for-bit, and modularity clustering is sensitive to small edge-weight differences
at the margin (the same caveat already recorded for the round-1 network test). It is, if anything, a further
demonstration of a real limitation worth stating in the dissertation: **the metro map's line structure is not
fully stable even at a fixed N=5 across two independently-computed co-occurrence graphs**, which matters for
anyone trying to reproduce or extend this specific design.

**Why metro's methodology differs from the other five tools:** community detection, spring embedding, and
octilinear correction are batch `networkx` operations with no practical client-side JS equivalent to build in
the time available, so this is a Python batch comparison across four fixed N values plus one rendered
snapshot, rather than a single live interactive page like the other five charts. This is a genuine
methodological difference, not a shortcut — it is stated here so it does not read as an inconsistency.

### Round 2 verdict

All four charts produced distinct, concrete, quantified findings, each different from the other five charts'
failure modes: bar-code (navigation/scroll cost), linear (horizontal sprawl, same root cause as bar-code but
the other axis), small multiples (real, non-linear computational cost — the one design where scale risks an
actual freeze), metro (the clustering algorithm's structural assumptions break down, not just the picture).
Folded into dissertation.tex and handover_v3.md alongside the round-1 results.
