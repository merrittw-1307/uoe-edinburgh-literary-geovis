# A Visual Trace Map of Edinburgh Place Names in Literature

**MSc Dissertation** · University of Edinburgh, School of Informatics · 2025-2026  
**Student**: Merritt Wang · **Supervisor**: Uta Hinrichs (VisHub)

---

## Overview

Interactive visualisation system for literary place names in Edinburgh, using the [LitLong Edinburgh](http://litlong.org) database (548 works, 1687-2015, 50,248 place-name mention records).

Core argument: place names in literary text should be visualised as **narrative structure**, not as geographic information.

### Two Research Directions

**Direction 1 — Author Spatial Fingerprints**  
Does each author's distribution of place-name mentions form a visually distinctive spatial signature, allowing users to distinguish authors at a glance?

**Direction 2 — Narrative Topology Networks**  
Does the co-occurrence of place names across literary works reveal a topology that diverges from Edinburgh's geographic topology?

---

## Key Findings

- Among 5 test authors, **zero place names are shared by 3 or more authors** — each author constructs an almost entirely private imaginary Edinburgh
- **Leith and Princes Street** are the strongest co-occurring pair (weight=28 documents) despite being geographically separated — narrative proximity does not equal geographic proximity
- Author sector distributions match established literary-geographic knowledge:
  - McCall Smith: New Town 60.7% (Scotland Street series)
  - Welsh: Leith and North 41.1% (Trainspotting)
  - Scott: Old Town 33.5% (historical fiction)

---

## Quick Start — Interactive Visualisations

All D3.js files are self-contained. Double-click to open in browser (no server required).

| File | Direction | Description |
|------|-----------|-------------|
| data/processed/dir_1/radar/d3/radar.html | Fingerprint | Radar chart: 6 city sector axes; hover + legend filter |
| data/processed/dir_1/barcode/d3/barcode.html | Fingerprint | Bar-code fingerprint (log scale); hover for details |
| data/processed/dir_1/small_multiples/d3/small_multiples.html | Fingerprint | 5 panels on abstract Edinburgh map; scroll to zoom |
| data/processed/dir_2/network/d3/network.html | Topology | Force-directed network; drag nodes, weight slider |
| data/processed/dir_2/linear/d3/linear.html | Topology | Linear connection diagram; weight threshold slider |
| data/processed/dir_2/metro/d3/metro.html | Topology | Metro-style narrative map; scroll to zoom |

---

## Repository Structure

    Dissertation/
    ├── data/
    │   ├── raw/
    │   │   ├── sql/
    │   │   │   ├── litlong_original.sql         (EXCLUDED — 145MB, too large for GitHub)
    │   │   │   ├── litlong_processed_1Jul.sql   (EXCLUDED — 204MB, too large for GitHub)
    │   │   │   ├── litlong_schema.sql           Schema only, no data
    │   │   │   └── directus.sql                 CMS export
    │   │   └── csv_snapshot/                    CSV exports of core tables
    │   └── processed/
    │       ├── dir_1/                           Direction 1: Author Spatial Fingerprints
    │       │   ├── radar/       py, d3, data
    │       │   ├── barcode/     py, d3, data
    │       │   └── small_multiples/  py, d3, data
    │       └── dir_2/                           Direction 2: Narrative Topology Networks
    │           ├── network/     py, d3, data
    │           ├── linear/      py, d3, data
    │           └── metro/       py, d3, data
    ├── dissertation/
    │   └── main/                                LaTeX source files
    ├── ethics/                                  Ethics approval and study forms
    ├── proposal/                                Project proposal and reading materials
    ├── report/
    │   ├── presentations/                       Supervisor presentations
    │   └── session_reports/                     Development session reports
    └── docs/                                    Handover and project documentation

---

## Database Setup

    brew install postgresql@16
    brew services start postgresql@16
    createdb litlong_edinburgh
    psql litlong_edinburgh < data/raw/sql/litlong_schema.sql
    # litlong_processed_1Jul.sql is excluded from repo (204MB)
# Contact Merritt Wang for access to this file

If you have the full dump (not in repo):

    psql litlong_edinburgh < data/raw/sql/litlong_original.sql

---

## Python Dependencies

    pip install pandas sqlalchemy psycopg2-binary matplotlib networkx

---

## Five Test Authors

| Author | Mentions | Books | Dominant sector | Pct |
|--------|----------|-------|----------------|-----|
| Alexander McCall Smith | 7320 | 17 | New Town | 60.7% |
| Irvine Welsh | 2634 | 8 | Leith and North | 41.1% |
| John Gibson Lockhart | 3046 | 6 | New Town | 44.3% |
| Walter Scott | 2796 | 12 | Old Town | 33.5% |
| Robert Louis Stevenson | 1778 | 16 | New Town | 35.2% |

---

## Six City Sectors (Radar Chart Axes)

| Sector | Condition |
|--------|-----------|
| Leith and North | lat > 55.97 |
| New Town | lat >= 55.952, lon in [-3.22, -3.175] |
| Old Town | lat < 55.952, lon in [-3.20, -3.165] |
| East and Arthur's Seat | lon > -3.165, lat < 55.96 |
| South Edinburgh | lat < 55.945 |
| Outer Edinburgh | lat < 55.92 or lon < -3.28 |

---

## Technical Notes

- Co-occurrence granularity: document-level (sentence: 0 pairs; page: up to 92; document: 403 pairs)
- Log scale for bar-code: Welsh's Leith count (650) is an extreme outlier; log scale resolves long-tail compression
- Narrative order: start_word field is globally unique and monotonically increasing within each document
- PostGIS not required: geom/poly fields excluded; lat/lon centroids used throughout

---

## Planned Features

- Combined single-page interface integrating both directions
- Author selector dropdown (all 424 authors)
- Original source text hover (from api_sentence table)
- Reader-plot timeline (using position_pct from mention_order)
- Narrative weight analysis (using api_posmention POS data)

---

## Key References

- Anderson et al. (2016): Palimpsest/LitLong project
- Stange and Dork (2015): Novel City Maps
- Nollenburg and Wolff (2006): Metro-map layout algorithm
- Westphal (2011): Geocriticism
- Moretti (2005): Graphs, Maps, Trees
- Shneiderman (1996): Information seeking mantra

---

## License

Academic use only. LitLong database copyright University of Edinburgh. Visualisation code: MIT License.
