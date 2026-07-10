"""
Rebuilds metro.html from data/metro_lines.json (produced by
build_metro_lines.py). Unlike the old hand-drawn version, every line here
is derived from real 5-author book co-occurrence data via community
detection - see the docstring in build_metro_lines.py for the pipeline.
"""
import json
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
DATA_PATH = REPO_ROOT / "data/processed/dir_2/metro/data/metro_lines.json"
OUT_PATH = REPO_ROOT / "data/processed/dir_2/metro/d3/metro.html"
BACKUP_PATH = REPO_ROOT / "data/processed/dir_2/metro/d3/metro_v1_geographic.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Edinburgh Literary Metro Map</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #F0F2F8;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
  }
  h1 { font-size: 20px; color: #21295C; margin-bottom: 6px; text-align: center; }
  .subtitle { font-size: 13px; color: #888; margin-bottom: 6px; text-align: center; max-width: 760px; }
  .note {
    font-size: 10.5px; color: #1E5C3A; background: #E9F7EF;
    border-left: 3px solid #27AE60; padding: 7px 12px;
    margin-bottom: 18px; border-radius: 0 4px 4px 0; max-width: 760px; text-align: left;
  }
  .controls { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; justify-content: center; margin-bottom: 14px; font-size: 12px; color: #555; }
  input[type=text] { border: 1px solid #C0C8D8; border-radius: 14px; padding: 5px 12px; font-size: 12px; width: 170px; }
  .reset-btn {
    border: 1.5px solid #C0C8D8; background: white; border-radius: 14px;
    padding: 4px 12px; font-size: 11px; cursor: pointer; color: #333;
  }
  .reset-btn:hover { background: #E8EAF6; border-color: #21295C; }

  .main { display: flex; gap: 18px; align-items: flex-start; }
  #chart-scroll { max-width: min(980px, 92vw); overflow: auto; border-radius: 14px; }
  #chart { position: relative; }
  .legend {
    display: flex; flex-direction: column; gap: 6px; min-width: 250px; max-width: 280px;
  }
  .legend-item {
    display: flex; flex-direction: column; gap: 2px; cursor: pointer;
    padding: 8px 10px; border-radius: 8px; border: 1.5px solid #E0E4F0; background: white;
    transition: all 0.15s; user-select: none;
  }
  .legend-item:hover { border-color: #B0B8D0; }
  .legend-item.inactive { opacity: 0.35; }
  .legend-top { display: flex; align-items: center; gap: 8px; font-size: 12.5px; font-weight: bold; }
  .legend-line { width: 22px; height: 5px; border-radius: 3px; flex-shrink: 0; }
  .legend-meta { font-size: 10.5px; color: #999; padding-left: 30px; }
  .legend-hint { font-size: 10px; color: #AAA; margin-top: 2px; }

  .tooltip {
    position: fixed; background: white; border: 1px solid #E0E4F0; border-radius: 8px;
    padding: 9px 13px; font-size: 12px; pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12); display: none; z-index: 100; max-width: 240px;
  }
  .tooltip .station { font-weight: bold; font-size: 13px; color: #21295C; margin-bottom: 3px; }

  #detail-panel {
    min-width: 260px; max-width: 300px; background: white; border: 1px solid #E0E4F0;
    border-radius: 12px; padding: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    display: none; flex-shrink: 0;
  }
  #detail-panel .close-btn { float: right; cursor: pointer; color: #CCC; font-size: 16px; line-height: 1; }
  #detail-panel .close-btn:hover { color: #666; }
  #detail-panel .dp-name { font-size: 16px; font-weight: bold; color: #21295C; margin-bottom: 2px; }
  #detail-panel .dp-meta { font-size: 12px; color: #888; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #EEE; }
  #detail-panel h4 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #999; margin: 10px 0 6px; }
  #detail-panel .row { font-size: 12px; color: #444; padding: 4px 0; border-bottom: 1px solid #F5F5F5; display: flex; justify-content: space-between; gap: 8px; }
  #detail-panel .row .lbl { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #detail-panel .row .val { color: #999; flex-shrink: 0; font-size: 11px; }
  #detail-panel .dp-quote { margin-top: 10px; padding-top: 8px; border-top: 1px solid #EEE; font-style: italic; color: #444; font-size: 11px; line-height: 1.4; }
  #detail-panel .dp-quote .src { font-style: normal; color: #999; display: block; margin-top: 3px; }
  #detail-panel .line-chip { display: inline-flex; align-items: center; gap: 5px; font-size: 11px; padding: 2px 8px; border-radius: 10px; background: #F4F6FB; margin: 2px 4px 2px 0; }
  #detail-panel .line-chip .dot { width: 7px; height: 7px; border-radius: 50%; }
</style>
</head>
<body>
<h1>Edinburgh Literary Metro Map</h1>
<div class="subtitle">Lines are narrative corridors derived from real book co-occurrence data (not geography) · hover stations to explore · click for details · scroll to zoom</div>
<div class="note">Method: lines come from modularity clustering on the 403-pair, 5-author co-occurrence graph, then ordered so adjacent stops share real book co-occurrence · <strong>__ADJ_BACKED__/__ADJ_TOTAL__ (__ADJ_PCT__%)</strong> of adjacent stops on this map share at least one book, versus 15/67 (22%) on the original geography-based draft.</div>

<div class="controls">
  <input type="text" id="search" placeholder="Search a station…">
  <button class="reset-btn" id="btn-reset">Show all lines</button>
</div>

<div class="main">
  <div id="chart-scroll"><div id="chart"></div></div>
  <div style="display:flex;flex-direction:column;gap:14px;">
    <div class="legend" id="legend"></div>
    <div class="legend-hint">Click a line to isolate it · click again to show all</div>
    <div id="detail-panel">
      <span class="close-btn" id="close-detail">&#x2715;</span>
      <div class="dp-name" id="dp-name"></div>
      <div class="dp-meta" id="dp-meta"></div>
      <div id="dp-lines"></div>
      <h4>Top co-occurring places</h4>
      <div id="dp-cooccur"></div>
      <h4>Books mentioning this place</h4>
      <div id="dp-books"></div>
      <div class="dp-quote" id="dp-quote"></div>
    </div>
  </div>
</div>
<div class="tooltip" id="tooltip"></div>

<script>
const DATA = /*__DATA_JSON__*/;
const LINES = DATA.lines;
const NODES = {};
DATA.nodes.forEach(n => NODES[n.place] = n);
const EDGES = DATA.edges;
const PLACE_BOOKS = DATA.placeBooks;
const PLACE_SENTENCES = DATA.placeSentences;
const INTERCHANGES = new Set(DATA.interchanges);

const UNIT_X = 42, UNIT_Y = 42;
const OFFSET_X = 40, OFFSET_Y = 40;
const W = OFFSET_X * 2 + (DATA.grid.w - 1) * UNIT_X;
const H = OFFSET_Y * 2 + (DATA.grid.h - 1) * UNIT_Y;

// One entry per unique station name, aggregated across every line it stops on.
const STATIONS = {};
LINES.forEach(line => {
  line.stations.forEach(s => {
    if (!STATIONS[s.name]) STATIONS[s.name] = { name: s.name, x: s.x, y: s.y, lines: [] };
    STATIONS[s.name].lines.push(line.id);
  });
});

const tooltip = document.getElementById('tooltip');
const panel = document.getElementById('detail-panel');
let activeLine = null;
let searchTerm = '';

const svg = d3.select('#chart')
  .append('svg')
  .attr('width', W)
  .attr('height', H)
  .style('background', '#ECEEF5')
  .style('border-radius', '14px');

const g = svg.append('g');

svg.call(d3.zoom().scaleExtent([0.4, 3]).on('zoom', e => g.attr('transform', e.transform)));

function px(x) { return OFFSET_X + x * UNIT_X; }
function py(y) { return OFFSET_Y + y * UNIT_Y; }

// Real transit maps restrict every segment to 0/45/90 degrees (Beck's rule).
// A straight hop between two arbitrary grid cells rarely satisfies that, so
// insert one diagonal-then-straight bend point per hop - the classic
// schematic-map "dog-leg" - instead of drawing an odd-angle diagonal.
function octilinearPoints(gridPts) {
  const out = [gridPts[0]];
  for (let i = 1; i < gridPts.length; i++) {
    const [x1, y1] = gridPts[i - 1];
    const [x2, y2] = gridPts[i];
    const dx = x2 - x1, dy = y2 - y1;
    const adx = Math.abs(dx), ady = Math.abs(dy);
    if (adx !== 0 && ady !== 0 && adx !== ady) {
      const m = Math.min(adx, ady);
      out.push([x1 + Math.sign(dx) * m, y1 + Math.sign(dy) * m]);
    }
    out.push([x2, y2]);
  }
  return out;
}

function gridPathData(gridPts) {
  return octilinearPoints(gridPts)
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${px(p[0])},${py(p[1])}`)
    .join(' ');
}

function topCooccurrences(place) {
  return EDGES
    .filter(e => e.source === place || e.target === place)
    .sort((a, b) => b.weight - a.weight)
    .slice(0, 5)
    .map(e => ({ place: e.source === place ? e.target : e.source, weight: e.weight }));
}

function showStationPanel(name) {
  const n = NODES[name];
  document.getElementById('dp-name').textContent = name;
  document.getElementById('dp-meta').textContent = n
    ? `${n.sector} · ${n.total_mentions} total mentions`
    : 'Not among the 57 core co-occurrence places';

  const memberLines = LINES.filter(l => l.stations.some(s => s.name === name));
  document.getElementById('dp-lines').innerHTML = memberLines.map(l =>
    `<span class="line-chip"><span class="dot" style="background:${l.color}"></span>${l.name}</span>`
  ).join('');

  const co = topCooccurrences(name);
  document.getElementById('dp-cooccur').innerHTML = co.length
    ? co.map(c => `<div class="row"><span class="lbl">${c.place}</span><span class="val">${c.weight}</span></div>`).join('')
    : '<div class="row"><span class="lbl">No strong co-occurrences</span></div>';

  const books = PLACE_BOOKS[name] || [];
  document.getElementById('dp-books').innerHTML = books.length
    ? books.slice(0, 6).map(b => `<div class="row"><span class="lbl">${b.title}</span><span class="val">${b.mentions}×</span></div>`).join('')
    : '<div class="row"><span class="lbl">No book details available</span></div>';

  const s = PLACE_SENTENCES[name];
  document.getElementById('dp-quote').innerHTML = (s && s.length)
    ? `“${s[0].text}”<span class="src">— ${s[0].book}, ${s[0].author}</span>`
    : '';

  panel.style.display = 'block';
}
document.getElementById('close-detail').addEventListener('click', () => panel.style.display = 'none');

function applyFilters() {
  g.selectAll('.line-path').attr('opacity', l => activeLine === null || l.id === activeLine ? 1 : 0.1);
  g.selectAll('.station-circle, .station-dot').attr('opacity', d => {
    const lineOk = activeLine === null || d.lines.includes(activeLine);
    const searchOk = !searchTerm || d.name.toLowerCase().includes(searchTerm);
    return lineOk && searchOk ? 1 : 0.12;
  });
  g.selectAll('.station-label').attr('opacity', d => {
    const lineOk = activeLine === null || d.lines.includes(activeLine);
    const searchOk = !searchTerm || d.name.toLowerCase().includes(searchTerm);
    return lineOk && searchOk ? 1 : 0.12;
  });
}

// Draw lines - each line's path runs through its stations' *shared* grid
// coordinates, so two lines that both stop at the same interchange actually
// meet at that point instead of running in separate parallel lanes.
LINES.forEach(line => {
  const gridPts = line.stations.map(s => [s.x, s.y]);
  const pathData = gridPathData(gridPts);
  g.append('path')
    .datum(line)
    .attr('class', 'line-path')
    .attr('d', pathData)
    .attr('fill', 'none')
    .attr('stroke', line.color)
    .attr('stroke-width', 5)
    .attr('stroke-linecap', 'round')
    .attr('stroke-linejoin', 'round')
    .attr('cursor', 'pointer')
    .on('click', function(event, l) {
      activeLine = (activeLine === l.id) ? null : l.id;
      applyFilters();
    })
    .on('mouseover', function(event, l) {
      tooltip.style.display = 'block';
      tooltip.innerHTML = `
        <div class="station" style="color:${l.color}">${l.name}</div>
        <div style="color:#888;font-size:11px">${l.stations.length} stops · ${l.total_mentions} mentions</div>
        <div style="color:#AAA;font-size:10px;margin-top:4px">Click to isolate this line</div>`;
    })
    .on('mousemove', event => {
      tooltip.style.left = (event.clientX + 14) + 'px';
      tooltip.style.top = (event.clientY - 10) + 'px';
    })
    .on('mouseout', () => tooltip.style.display = 'none');
});

// Greedy label placement: try 8 compass positions around each circle and
// keep the first one that doesn't overlap an already-placed label or
// circle, so two nearby stations (common once real co-occurrence pulls a
// cluster tight) don't end up with overlapping text.
function estimateBox(text, x, y, anchor, fontSize) {
  const w = text.length * fontSize * 0.58;
  const h = fontSize * 1.3;
  const left = anchor === 'start' ? x : anchor === 'end' ? x - w : x - w / 2;
  return { x: left, y: y - fontSize * 0.85, width: w, height: h };
}
function boxesOverlap(a, b) {
  return a.x < b.x + b.width && b.x < a.x + a.width &&
         a.y < b.y + b.height && b.y < a.y + a.height;
}
function placeLabels(stations) {
  const occupied = stations.map(s => {
    const r = INTERCHANGES.has(s.name) ? 9 : 6;
    const cx = px(s.x), cy = py(s.y);
    return { x: cx - r, y: cy - r, width: r * 2, height: r * 2 };
  });
  const ordered = [...stations].sort((a, b) =>
    (INTERCHANGES.has(b.name) ? 1 : 0) - (INTERCHANGES.has(a.name) ? 1 : 0));
  const placement = {};
  ordered.forEach(s => {
    const cx = px(s.x), cy = py(s.y);
    const isInterchange = INTERCHANGES.has(s.name);
    const r = isInterchange ? 9 : 6;
    const fontSize = isInterchange ? 9 : 8;
    const ring = (d1, d2) => [
      { dx: 0, dy: d1 + 3, anchor: 'middle' },
      { dx: d2, dy: d2 * 0.6 + 3, anchor: 'start' },
      { dx: -d2, dy: d2 * 0.6 + 3, anchor: 'end' },
      { dx: d1 + 2, dy: 3, anchor: 'start' },
      { dx: -(d1 + 2), dy: 3, anchor: 'end' },
      { dx: d2, dy: -d2 * 0.5, anchor: 'start' },
      { dx: -d2, dy: -d2 * 0.5, anchor: 'end' },
      { dx: 0, dy: -(d1 - 1), anchor: 'middle' },
    ];
    // Try a close ring first, then a wider ring, before giving up and
    // accepting the first candidate's overlap (dense clusters can exhaust
    // both rings; a farther-but-clear label beats a close-but-colliding one).
    const candidates = [...ring(r + 10, r + 6), ...ring(r + 17, r + 13)];
    let chosen = null;
    for (const c of candidates) {
      const lx = cx + c.dx, ly = cy + c.dy;
      const box = estimateBox(s.name, lx, ly, c.anchor, fontSize);
      if (!occupied.some(o => boxesOverlap(box, o))) {
        chosen = { x: lx, y: ly, anchor: c.anchor, fontSize, box };
        break;
      }
    }
    if (!chosen) {
      const c = candidates[0];
      const lx = cx + c.dx, ly = cy + c.dy;
      chosen = { x: lx, y: ly, anchor: c.anchor, fontSize, box: estimateBox(s.name, lx, ly, c.anchor, fontSize) };
    }
    occupied.push(chosen.box);
    placement[s.name] = chosen;
  });
  return placement;
}
const LABEL_PLACEMENT = placeLabels(Object.values(STATIONS));

// One circle + one label per unique station, at its shared coordinate.
Object.values(STATIONS).forEach(s => {
  const x = px(s.x), y = py(s.y);
  const isInterchange = INTERCHANGES.has(s.name);

  g.append('circle')
    .datum(s)
    .attr('class', 'station-circle')
    .attr('cx', x).attr('cy', y)
    .attr('r', isInterchange ? 9 : 6)
    .attr('fill', 'white')
    .attr('stroke', isInterchange ? '#333' : LINES.find(l => l.id === s.lines[0]).color)
    .attr('stroke-width', isInterchange ? 3 : 2)
    .attr('cursor', 'pointer')
    .on('mouseover', function() {
      d3.select(this).attr('fill', '#FFF3CD');
      const memberLines = LINES.filter(l => s.lines.includes(l.id));
      tooltip.style.display = 'block';
      tooltip.innerHTML = `
        <div class="station">${s.name}</div>
        <div style="color:#888;font-size:11px">${memberLines.map(l => l.name).join(', ')}</div>
        ${isInterchange ? '<div style="color:#C9A227;font-size:11px;margin-top:4px">⬡ Interchange - real cross-corridor link</div>' : ''}
        <div style="color:#AAA;font-size:10px;margin-top:4px">Click for books &amp; a text snippet</div>`;
    })
    .on('mousemove', event => {
      tooltip.style.left = (event.clientX + 14) + 'px';
      tooltip.style.top = (event.clientY - 10) + 'px';
    })
    .on('mouseout', function() {
      d3.select(this).attr('fill', 'white');
      tooltip.style.display = 'none';
    })
    .on('click', () => { tooltip.style.display = 'none'; showStationPanel(s.name); });

  if (isInterchange) {
    g.append('circle')
      .datum(s)
      .attr('class', 'station-dot')
      .attr('cx', x).attr('cy', y).attr('r', 3.5)
      .attr('fill', '#333').attr('pointer-events', 'none');
  }

  const lp = LABEL_PLACEMENT[s.name];
  g.append('text')
    .datum(s)
    .attr('class', 'station-label')
    .attr('x', lp.x)
    .attr('y', lp.y)
    .attr('text-anchor', lp.anchor)
    .attr('font-size', lp.fontSize + 'px')
    .attr('font-weight', isInterchange ? '700' : '500')
    .attr('fill', '#222')
    .attr('pointer-events', 'none')
    .text(s.name);
});

// Legend
const legendDiv = document.getElementById('legend');
LINES.forEach(line => {
  const item = document.createElement('div');
  item.className = 'legend-item';
  item.innerHTML = `
    <div class="legend-top"><div class="legend-line" style="background:${line.color}"></div>${line.name}</div>
    <div class="legend-meta">${line.stations.filter(s=>s.home_line===line.id).length} stations · ${line.total_mentions} mentions · ${line.adjacency_backed}/${line.adjacency_total} adjacent stops share a book</div>`;
  item.addEventListener('click', () => {
    activeLine = (activeLine === line.id) ? null : line.id;
    document.querySelectorAll('.legend-item').forEach((el, idx) => {
      el.classList.toggle('inactive', activeLine !== null && LINES[idx].id !== activeLine);
    });
    applyFilters();
  });
  legendDiv.appendChild(item);
});

document.getElementById('btn-reset').addEventListener('click', () => {
  activeLine = null;
  document.querySelectorAll('.legend-item').forEach(el => el.classList.remove('inactive'));
  applyFilters();
});

document.getElementById('search').addEventListener('input', function() {
  searchTerm = this.value.trim().toLowerCase();
  applyFilters();
});
</script>
</body>
</html>
"""


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    total_backed = sum(l["adjacency_backed"] for l in data["lines"])
    total_adj = sum(l["adjacency_total"] for l in data["lines"])
    pct = round(100 * total_backed / total_adj) if total_adj else 0

    html = TEMPLATE.replace("/*__DATA_JSON__*/", json.dumps(data, ensure_ascii=False))
    html = html.replace("__ADJ_BACKED__", str(total_backed))
    html = html.replace("__ADJ_TOTAL__", str(total_adj))
    html = html.replace("__ADJ_PCT__", str(pct))

    if OUT_PATH.exists() and not BACKUP_PATH.exists():
        BACKUP_PATH.write_text(OUT_PATH.read_text())
        print(f"Backed up geography-based version to {BACKUP_PATH}")

    OUT_PATH.write_text(html)
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB); "
          f"{total_backed}/{total_adj} ({pct}%) adjacent stops backed by real co-occurrence")


if __name__ == "__main__":
    main()
