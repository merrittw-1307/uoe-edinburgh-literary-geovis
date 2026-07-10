# Project Handover Document
## A Visual Trace Map of Edinburgh Place Names in Literature
### MSc Dissertation — Merritt Wang (S2887338)
### University of Edinburgh, School of Informatics, 2025-2026

---

## CRITICAL: How to Use This Document

This document is a complete handover for continuing this project in a new conversation window. Read it fully before responding to Merritt. The project is active and ongoing — do not start from scratch. Always respond in **Chinese** unless Merritt writes in English. Do not simply agree with everything Merritt says — be objective and push back when appropriate.

---

## 1. Project Overview

### What This Project Is

An MSc dissertation project creating an **interactive visualisation system** for literary place names in Edinburgh. The core argument is that place names in literary text should be visualised as **independent narrative structure**, not as geographic information. Geographic maps assume meaning = location; in literature, meaning comes from narrative context.

### Student & Supervisory Team

- **Student**: Merritt Wang (also goes by Merritt; Chinese name 王铭宇/Mingyu Wang)
- **Supervisor**: Uta Hinrichs (co-director of VisHub, School of Informatics)
- **Tutor/Second supervisor**: Nina Pardal
- **GitHub**: merrittw-1307
- **Dissertation due**: 21 August 2026
- **Mid-term report**: 10 July 2026 (important milestone)

### Two Research Directions

**Direction 1 — Author Spatial Fingerprints (RQ1):**
Does each author's distribution of place-name mentions form a visually distinctive spatial signature that allows users to identify authors from their fingerprint alone?

**Direction 2 — Narrative Topology Networks (RQ2):**
Does the co-occurrence of place names within literary works reveal a narrative topology that diverges from the geographic topology of Edinburgh?

### Technology Stack

- **Data**: PostgreSQL 16 (local, Mac), Python (pandas, sqlalchemy, matplotlib, networkx)
- **Visualisation**: D3.js v7 (interactive, web-native)
- **Dissertation**: LaTeX on Overleaf (infthesis.cls template)
- **Version control**: GitHub (repo: merrittw-1307)

---

## 2. Data Sources

### Primary Database

**File**: `litlong_2022-06-21.sql` (145MB, 2.3 million lines)
**Location**: `/Users/wangmingyu/Downloads/UoE/Dissertation/data/raw/sql/litlong_original.sql`
**What it is**: Official complete PostgreSQL dump of the LitLong Edinburgh project database.
**Database name**: `litlong_edinburgh` (local PostgreSQL 16, user: wangmingyu, port 5432)

### Key Tables After Import

| Table | Rows | Description |
|-------|------|-------------|
| api_document | 620 | Literary works metadata (title, pubdate, type, url) |
| api_author | 424 | Authors (forenames, surname, gender, ol_id) |
| api_document_author | 1,232 | Many-to-many: documents ↔ authors |
| api_location | 2,135 | Place names (text, lat, lon, gazref, ptype) |
| api_locationmention | 50,248 | Each mention of a place in a document (start_word, end_word, page_id, sentence_id) |
| api_sentence | 50,248 | Full source text sentence for each mention |
| api_genre | 29 | Literary genres |
| api_document_genre | 2,682 | Many-to-many: documents ↔ genres |
| api_page | 20,077 | Page-level information |
| api_posmention | 2,085,834 | Part-of-speech annotations (not yet used) |
| mention_order | 50,248 | CUSTOM TABLE: derived narrative order fields |

### Custom Table: mention_order

Created by extracting and normalising the `start_word` field from `api_locationmention`.

**Key insight**: The `start_word` field (format: "w81489") is:
- Globally unique across the entire corpus
- Strictly monotonically increasing within each document
- This means it encodes narrative reading order directly

**Fields in mention_order**:
- `id` — same as api_locationmention.id
- `document_id` — foreign key to api_document
- `location_id` — foreign key to api_location
- `word_num` — integer extracted from start_word (e.g. "w81489" → 81489)
- `mention_order` — rank of this mention within its document (1 = first)
- `position_pct` — normalised position 0.0–1.0 within the document

### Secondary Data Files

| File | Location | Description |
|------|----------|-------------|
| `directus.sql` | `data/raw/sql/` | LitLong CMS export; contains curated source text excerpts organised as "literary walking routes". Less useful now that api_sentence has full text. |
| `api_location.csv` | `data/raw/csv_snapshot/` | CSV snapshot; used to supplement api_location (which failed to import due to PostGIS dependency) |
| `api_document.csv` | `data/raw/csv_snapshot/` | CSV snapshot of api_document |
| `api_locationmention.csv` | `data/raw/csv_snapshot/` | CSV snapshot of api_locationmention |
| `locationByDocuments.csv` | `data/raw/csv_snapshot/` | Denormalised join of document + location data; not a native database table |

### Important Database Notes

- `api_location` **failed to import from SQL dump** because it uses PostGIS geometry types (`geom`, `poly` fields) and PostGIS is not installed. It was re-imported from the CSV snapshot using Python/pandas, retaining only: id, text, lat, lon, gazref, ptype. The PostGIS fields are not needed for current visualisation directions.
- The SQL dump originally belonged to user "palimpsest" on a remote server. Import errors about missing roles (palimpsest, postgres) are harmless — they only affect ownership, not data.
- `api_sentence` and `api_locationmention` have the same row count (50,248) — they are one-to-one: every mention has exactly one corresponding source sentence.

---

## 3. Directory Structure

```
/Users/wangmingyu/Downloads/UoE/Dissertation/
├── data/
│   ├── raw/
│   │   ├── sql/
│   │   │   ├── litlong_original.sql      ← full LitLong dump (145MB, DO NOT push to GitHub)
│   │   │   ├── litlong_processed.sql     ← mention_order + api_location export
│   │   │   ├── litlong_schema.sql        ← schema only, no data (push to GitHub)
│   │   │   └── directus.sql              ← CMS export (backup, low priority)
│   │   └── csv_snapshot/
│   │       ├── api_document.csv
│   │       ├── api_location.csv
│   │       ├── api_locationmention.csv
│   │       └── locationByDocuments.csv
│   └── processed/
│       ├── radar/
│       │   ├── py/                       ← radar_chart.png
│       │   ├── d3/                       ← radar.html (interactive, self-contained)
│       │   └── data/                     ← radar_data.csv
│       ├── barcode/
│       │   ├── py/                       ← barcode_chart.png, barcode_chart_log.png
│       │   ├── d3/                       ← barcode.html
│       │   └── data/                     ← barcode_data.csv
│       ├── network/
│       │   ├── py/                       ← network_chart_v3.png (v1,v2 may exist)
│       │   ├── d3/                       ← network.html
│       │   └── data/                     ← network_edges.csv, network_nodes.csv
│       ├── linear/
│       │   ├── py/                       ← linear_chart_v1.png
│       │   ├── d3/                       ← linear.html
│       │   └── data/                     ← (edges from network/data/)
│       ├── small_multiples/
│       │   ├── py/                       ← small_multiples.png
│       │   ├── d3/                       ← small_multiples.html
│       │   └── data/
│       └── metro/
│           ├── py/                       ← metro_chart_v1.png, metro_chart_v2.png
│           ├── d3/                       ← metro.html
│           └── data/
├── viz/                                  ← (may be superseded by processed/*/d3/)
└── overleaf → https://overleaf.com (shared with Uta Hinrichs)
```

---

## 4. Five Test Authors

Selected for: high mention counts, stylistic contrast, temporal diversity, strong literary-geographic associations.

| Author | Mentions | Books | Known spatial character | Colour |
|--------|----------|-------|------------------------|--------|
| Alexander McCall Smith | 7,320 | 17 | New Town (Scotland Street series) | #B85042 |
| Irvine Welsh | 2,634 | 8 | Leith (Trainspotting) | #1C7293 |
| John Gibson Lockhart | 3,046 | 6 | New Town (19th c. literary circle) | #2C5F2D |
| Walter Scott | 2,796 | 12 | Old Town (historical fiction) | #C9A227 |
| Robert Louis Stevenson | 1,778 | 16 | New Town + Leith (Gothic sensibility) | #7F77DD |

**IMPORTANT**: Author names in the database have leading/trailing spaces. Always use `TRIM(a.forenames) || ' ' || TRIM(a.surname)` in SQL queries. Match using separate forenames/surname conditions, not a concatenated string.

---

## 5. Six City Sectors

Defined by lat/lon ranges from `api_location` coordinates. Used as axes for the radar chart.

| Sector | Lat/Lon condition | Representative places |
|--------|------------------|----------------------|
| Leith & North | lat > 55.97 | Leith, Forth, Granton, Newhaven |
| New Town | lat ≥ 55.952, lon ∈ [-3.22, -3.175] | Princes St, Queen St, Moray Place |
| Old Town | lat < 55.952, lon ∈ [-3.20, -3.165] | High Street, Canongate, Grassmarket |
| East & Arthur's Seat | lon > -3.165, lat < 55.96 | Arthur's Seat, Holyrood, Abbeyhill |
| South Edinburgh | lat < 55.945 | Bruntsfield, Morningside, The Meadows |
| Outer Edinburgh | lat < 55.92 OR lon < -3.28 | Musselburgh, Cramond, Corstorphine |

**Validated**: Sector distributions match established literary-geographic knowledge for all 5 authors (e.g. Welsh → Leith 41.1%, McCall Smith → New Town 60.7%, Scott → Old Town 33.5%).

---

## 6. Key Data Findings

### Finding 1 — Author Spatial Languages Are Highly Individual
Among the 5 test authors, **ZERO place names are shared by 3 or more authors**. Only 18 place names are shared by exactly 2 authors. This confirms the core thesis: each author constructs an almost entirely private imaginary Edinburgh.

**Implication**: Individual place names cannot serve as radar chart axes (most axes would be zero for most authors). City sectors must be used instead.

### Finding 2 — Sector Distributions Validated Against Literary Knowledge
Data-driven results match established literary-geographic knowledge for all 5 authors. This cross-validation strengthens the methodology's credibility. Write this up prominently in the dissertation.

### Finding 3 — Co-occurrence Granularity
- **Sentence-level**: 0 co-occurring pairs (every sentence has ≤1 location mention)
- **Page-level**: up to 92 co-occurring places per page (too coarse → hairball)
- **Document-level**: 403 pairs with weight ≥ 2 (**selected as appropriate granularity**)

### Finding 4 — Narrative Topology Diverges From Geographic Topology
Strongest co-occurring pair: **Leith & Princes Street** (weight = 28). These are geographically separated (Leith is a port district ~2.5km north of Princes Street), yet they appear together in 28 different literary works. This is a concrete, data-driven example of narrative proximity ≠ geographic proximity. **This is the single most powerful finding for the dissertation argument.**

### Finding 5 — Walter Scott's Broad Geographic Range
Scott's data includes distant locations (Forth: lat 56.05, Haddington: lon -2.80, Linlithgow: lon -3.58). When using real coordinates for Small Multiples, Scott's range compressed the city centre for other authors. **Decision**: fix coordinate range to Edinburgh core (lat 55.88–56.01, lon -3.30 to -3.05) and filter out-of-range points.

---

## 7. Six Visualisations — Status and Design Decisions

### 7.1 Radar Chart (Direction 1 — Primary)

**File**: `radar/d3/radar.html` (self-contained, double-click to open)
**Status**: ✅ Complete, interactive

**Key decisions**:
- Axes = 6 city sectors (not individual place names — too sparse)
- Y-axis scaled to data maximum (0.65), not 1.0 — avoids 35% empty space
- Hover targets: invisible circles r=14px (not r=6px) — comfortable interaction
- Click legend to show/hide individual authors
- Data embedded as JS arrays (not external CSV) — works without local server

### 7.2 Bar-code Fingerprint (Direction 1 — Secondary)

**File**: `barcode/d3/barcode.html`
**Status**: ✅ Complete, interactive

**Key decisions**:
- Log scale (`np.log1p(value * 1000)`) — Welsh's Leith is an extreme outlier; linear scale compresses everything else flat
- Literary place-name data is long-tail distributed; log scale is standard treatment
- Hover shows place name + percentage

### 7.3 Small Multiples (Direction 1 — Tertiary)

**File**: `small_multiples/d3/small_multiples.html`
**Status**: ✅ Complete, interactive

**Key decisions**:
- Uses real-world coordinates (supervisor's sketch explicitly noted "Real-world")
- Abstract city map SVG overlay: Firth of Forth, Arthur's Seat hill silhouette, Pentland Hills ridge, Edinburgh Castle symbol, Holyrood diamond, Water of Leith river, neighbourhood labels
- Per-panel D3 zoom (1-10x) for inspecting dense clusters
- 3+2 flex layout (3 panels top row, 2 bottom row, centred)
- Coordinate range fixed to Edinburgh core; Scott's distant places filtered out
- **Finding**: single-panel readability lower than radar chart; value is comparative

### 7.4 Force-directed Network (Direction 2 — Primary)

**File**: `network/d3/network.html`
**Status**: ✅ Complete, interactive

**Key decisions**:
- Document-level co-occurrence (not sentence or page — see Finding 3)
- Edge weight threshold slider (range 8–28); simulation re-runs on change
- Scaled edge width: (weight/maxWeight)² × 12 — squared normalisation gives visible difference between strong and weak connections
- Node labels BELOW nodes (y = node.y + radius + 12) — not inside (invisible against dark fill)
- Hover: top 5 co-occurring places + total mentions
- Drag nodes, scroll to zoom/pan

**Debugging history** (3 iterations):
- v1: weight × 0.3 → no visible width difference
- v2: sqrt scaling → marginal improvement, centre still dense
- v3: threshold ≥ 8 + squared normalisation + spring k=3.5 → resolved

**Important note**: Node positions carry NO geographic meaning. Proximity in the graph = narrative proximity only. This is by design and supports the dissertation argument.

### 7.5 Linear Connection Diagram (Direction 2 — Secondary)

**File**: `linear/d3/linear.html`
**Status**: ✅ Complete, interactive

**Key decisions**:
- Linear axis instead of circular (chord diagram) — **supervisor's explicit feedback**: circular form implies cyclical structure, inappropriate for literary narrative which has a beginning and end
- Places ordered left-to-right by total mention frequency
- Bézier arcs: height proportional to horizontal distance between nodes
- Weight threshold slider (range 6–28)
- Hover arcs: source, target, weight; hover nodes: mention count

### 7.6 Metro-style Map (Direction 2 — Illustrative)

**File**: `metro/d3/metro.html`
**Status**: ✅ Complete, interactive

**Key decisions**:
- 8 lines, 50+ stations on manual grid layout (unit = 58px)
- Manual layout chosen because algorithmic metro-map layout is a known NP-hard graph drawing problem (cite: Nöllenburg & Wolff, 2006)
- Interchange stations marked with double-circle symbol
- Scroll to zoom/pan; hover for station info
- Simpler version retained over the advanced version (line toggle, search, info panel) — added complexity distracted from the core visual

**8 lines**:
- North Line (#1C7293) — coastal north Edinburgh
- Old Town Line (#B85042) — historic Royal Mile axis
- South Line (#2C5F2D) — southern residential belt
- East-West Line (#C9A227) — cross-city
- Circle Line (#7F77DD) — inner city loop
- North-South Line (#A26769) — meridional through-line
- Outer Line (#4A4A4A) — outer suburbs
- West Line (#FF6B35) — western approach

---

## 8. Supervisor Communication History

### Week 1 Meeting
**Tasks assigned**:
- Read ethics materials (done; approval #446635)
- Complete data protection training (done; both Learn Ultra modules, 90/90)
- Unpack data, set up PostgreSQL
- Think about how to extract place name order
- Start visualisation sketches
- Start Overleaf project

### Week 3 Meeting (after Vishub presentation)
Merritt did a 5-minute presentation to the VisHub group (8 attendees, online+in-person). Uta attended.

**Tasks assigned**:
- PostgreSQL (continuing from Week 1)
- Think about user-centred feedback sessions:
  - Who to recruit (audience of sketches?)
  - In-person or online?
  - What to learn from participants?
  - How to introduce sketches/prototypes?
- Prepare study forms (modify PIS and Consent Form for this study)
- Plan study timeline in Gantt chart
- Fingerprint sketches: Reader-plot, Reader-sketch(?), Network sketch
- "What are you hoping to achieve? Distinguishing between different authors"

**Supervisor's hand-drawn sketches** (two pages):
- Page 1: Radar chart with "5 books, 300 mentions", "overlap of locations/5 books", "Alpha", "by genre", "city sectors"
- Page 2: Various sketch ideas including barcode style, small multiples with "Real-world" annotation, Reader-plot timeline concept

**"Reader-sketch"**: This term appeared in supervisor's notes with a question mark. Its exact meaning is unclear. **Ask supervisor to clarify this at the next meeting.**

### Key Decisions Made in Supervisor Meetings
- **Chord diagram → linear**: Supervisor said circular form implies cyclical structure; inappropriate for linear literary narrative
- **City sectors as radar axes**: From supervisor's hand-drawn sketch ("city sectors")
- **D3.js over R**: Supervisor expressed uncertainty about R's interactive capabilities; D3.js confirmed
- **Interactive over static**: Confirmed in Week 3/4 discussion

### VisHub Group
The supervisor (Uta Hinrichs) co-directs VisHub (Edinburgh Visualisation Hub) with Benjamin Bach. The group includes PhD students, postdocs, and visiting scholars. Merritt attended a VisHub meeting where April Cain presented on "Dataset design is a process of representation." Other attendees included Sarah Dunn, Jinrui Wang, Xinyu Zhu, Lina Alqurashi, Tomas Vancisin, Yiqian Cui.

---

## 9. Pending Tasks

### Immediate (should be done before next supervisor meeting)

| Task | Priority | Notes |
|------|----------|-------|
| Share presentation slides with Uta | HIGH | Slides done, not yet sent |
| Share Overleaf with Uta | HIGH | Skeleton done, not yet shared |
| Ask Uta: what is "Reader-sketch"? | HIGH | Unclear from notes |
| Design user feedback study | HIGH | Decided: online, 2 groups (experts + general public) |
| Modify PIS and Consent Form | MEDIUM | Ethics #446635; select Option C (observation) |
| Add study timeline to Gantt chart | MEDIUM | Need to confirm week for study |

### Technical (ongoing)

| Task | Priority | Notes |
|------|----------|-------|
| Build combined interface | HIGH | Single HTML integrating both directions; author dropdown |
| Expand author pool to 20-30 | MEDIUM | Reminder: trigger at Week 6 |
| Add api_sentence hover (original text) | HIGH | "Killer feature"; trigger at Week 7 |
| Push to GitHub | MEDIUM | Clean up directory first |
| Validate start_word ordering systematically | LOW | Tested on 3 docs; should test more |

---

## 10. Roadmap and Scale Expansion Plan

**This is critical information**: The current 5-author prototype is correct for the exploration/evaluation stage. Here is when and how to expand:

### Week 5 (after user study)
- Select final 2-3 visualisation designs based on user feedback
- Begin planning combined interface architecture

### Week 6 — SCALE TRIGGER
**Remind Merritt**: Expand author pool from 5 to 20-30. Add multi-select dropdown to the combined interface. Choose authors for diversity in: time period (17th–21st c.), genre, gender, geographic focus within Edinburgh.

### Week 7 — SCALE TRIGGER
**Remind Merritt**: Implement `api_sentence` original text hover. This is the "killer feature" — hover on any place name in any visualisation → popup showing the actual literary sentence where that place appears. Data is ready (50,248 sentences in database). Need to decide: pre-load all sentences in JS, or fetch on demand via a lightweight backend.

### Week 8 (pre-submission)
- Test combined interface on different screen sizes
- Ensure smooth demo performance
- Check all interactive features work in Safari and Chrome

### Final product scale (at submission)
- 1 combined interactive interface (not 6 separate HTML files)
- Author selector: all 424 authors available, default: 5 core test authors
- 2 main directions: fingerprint + topology
- Each direction: primary + optional secondary visualisation
- Original text hover on all place names
- Network graph: top 50 high-frequency place names

---

## 11. Future Research Directions (for dissertation Future Work section)

### Direction 3: Narrative Weight (via api_posmention)
2,085,834 POS annotation records are available but unused. Could support analysis of whether a place appears in:
- Dialogue vs narration
- Climactic scenes vs background description
- Beginning vs end of narrative
This would add a "weight" dimension to place mentions beyond simple frequency.

### Direction 4: Literary Silences
Which Edinburgh places NEVER appear in literature? The database has 2,135 places that DO appear; comparing to a complete Edinburgh gazetteer would reveal what has been systematically ignored by literary authors. Mentioned in the original project proposal.

### Reader-plot Timeline
Using the `position_pct` field in `mention_order`, create a timeline showing when in a book each place appears. The data is ready. This was prototyped in Python but not included in the user study.

### Algorithmic Metro-map Layout
The manual metro-map layout is not generalisable. Implementing Nöllenburg & Wolff's algorithm would be a contribution to graph drawing as well as literary visualisation.

### Expansion to Full Author Corpus
The 5-author prototype can be scaled to all 424 authors. This would require UI work (pagination, clustering, search) but the data pipeline is already built.

---

## 12. Python Scripts (saved in /tmp/ on the development machine)

These scripts will be lost if the machine restarts. They should be saved properly.

| Script | Purpose |
|--------|---------|
| `/tmp/barcode_data.py` | Generates barcode_data.csv |
| `/tmp/barcode_plot2.py` | Log-scale bar-code chart |
| `/tmp/network_data2.py` | Document-level co-occurrence edges + nodes |
| `/tmp/network_plot3.py` | Force-directed network v3 (final) |
| `/tmp/linear_plot.py` | Linear connection diagram |
| `/tmp/metro_plot2.py` | Metro map v2 (8 lines) |
| `/tmp/rewrite_sm.py` | Small multiples with abstract city map |
| `/tmp/update_outline.py` | City map outline update script |

**Action needed**: Copy these to `data/processed/*/py/` directories before they are lost.

---

## 13. LaTeX Dissertation Status

**Platform**: Overleaf (not yet shared with supervisor — do this immediately)
**Template**: `infthesis.cls` (University of Edinburgh Informatics MSc template)
**Ethics declaration**: Application number 446635

**Chapter structure** (15,000 word target):
1. Introduction (~1,500 words)
2. Literature Review (~3,000 words)
3. Design (~2,000 words) — covers design rationale, data findings, candidate designs per direction
4. Implementation (~3,500 words) — data pipeline, D3 implementation details, combined interface
5. Evaluation (~2,500 words) — user study design, results, analysis
6. Discussion (~2,000 words) — improvements, key findings discussion, limitations
7. Conclusion (~700 words)
Appendices: PIS, Consent Form, task questions, database schema, sector definitions, author table

**Key references to collect**:
- Anderson et al. (2016): LitLong/Palimpsest project paper
- Stange & Dörk (2015): Novel City Maps (CRITICAL — most directly related work)
- Nöllenburg & Wolff (2006): Metro-map layout algorithm
- Westphal (2011): Geocriticism
- Moretti (2005): Graphs, Maps, Trees
- Shneiderman (1996): Information seeking mantra
- Tufte (1983): Envisioning Information (small multiples)
- Fruchterman & Reingold (1991): Force-directed layout
- Beck (1933): London Underground map

---

## 14. User Study Design (decided, not yet executed)

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Format | Online | Broader recruitment, larger sample, saves time |
| Groups | 2: domain experts (geography/literature) + general public | Test whether design preferences differ |
| Introduction | Project purpose only — NO explanation of each chart | Avoids priming; tests self-explanatory designs |
| Task 1 | Author identification (fingerprint direction) | Metric: accuracy rate |
| Task 2 | Narrative relationship identification (topology direction) | Metric: accuracy + perception of narrative/geographic divergence |
| Vote | Most intuitive design per direction | Quantitative preference data |
| Timeline | Must complete before 10 July mid-term report | So report can include user study findings |
| Tool | Qualtrics (university licence) or Google Forms | TBD |

---

## 15. Session Report

A comprehensive HTML session report (`session_report_v2.html`) was generated documenting all decisions and findings from the main development session (30 June 2026). It contains **15 screenshot placeholders** to be filled in by a separate conversation window. The report covers:
- Database setup and validation
- Key data findings
- All 6 Python prototype visualisations
- Complete decision log (Python phase)
- All 6 D3.js interactive implementations
- Complete decision log (D3 phase)

---

## 16. Merritt's Personal Context (relevant to supervision relationship)

- Merritt is doing an MSc in Computer Science at Edinburgh, graduating September 2026
- Has a background in Data Science (undergraduate, China University of Geosciences Beijing)
- Programming experience: Python, C/C++, Java, R, SQL, MATLAB
- Prefers Chinese for responses
- Wants this project to be genuinely excellent, not just "done"
- Sometimes needs encouragement, but also needs honest pushback — do not simply agree
- Attended VisHub meeting and felt out of place (imposter syndrome); was reassured that this is normal and that many attendees are non-native English speakers too
- The project is part of a broader life chapter — Merritt takes it seriously

---

## 17. What the Next Conversation Window Should Do First

1. **Read this entire document** before responding
2. **Ask Merritt** what the most pressing task is right now
3. **Check which of the pending tasks** (Section 9) have been completed since this document was written
4. **Remind Merritt** to:
   - Share slides with Uta
   - Share Overleaf with Uta
   - Save Python scripts from /tmp/ before they are lost
   - Ask Uta about "Reader-sketch"
5. **Continue from where we left off**: the immediate next steps were to push everything to GitHub and continue building the combined interface

---

*Document generated: 1 July 2026*
*Project status: Python prototypes complete, D3 interactive versions complete, combined interface not yet started, user study not yet run*
