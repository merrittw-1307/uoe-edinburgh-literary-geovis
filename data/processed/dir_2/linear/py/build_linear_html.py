"""
Rebuilds linear.html from data/linear_enriched.json.

Keeps the existing project convention of embedding data as inline JS (no
fetch/CSV, since file:// blocks XHR). Backs up the previous version to
linear_v1.html before overwriting.
"""
import json
import shutil
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
DATA_PATH = REPO_ROOT / "data/processed/dir_2/linear/data/linear_enriched.json"
OUT_PATH = REPO_ROOT / "data/processed/dir_2/linear/d3/linear.html"
BACKUP_PATH = REPO_ROOT / "data/processed/dir_2/linear/d3/linear_v1.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Narrative Topology — Linear Connection Diagram</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #F8F9FC;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 30px;
  }
  h1 { font-size: 20px; color: #21295C; margin-bottom: 6px; text-align: center; }
  .subtitle { font-size: 13px; color: #888; margin-bottom: 4px; text-align: center; }
  .source { font-size: 10px; color: #BBB; margin-bottom: 22px; text-align: center; font-style: italic; }

  .controls { display: flex; gap: 22px; margin-bottom: 12px; align-items: center; font-size: 13px; color: #555; flex-wrap: wrap; justify-content: center; }
  input[type=range] { width: 120px; }
  input[type=text] {
    border: 1px solid #DADFEE; border-radius: 6px; padding: 5px 10px; font-size: 12px; width: 160px;
  }
  .sort-group { display: flex; align-items: center; gap: 6px; }
  .sort-label { color: #888; }
  .sort-btn {
    border: 1px solid #DADFEE; background: white; color: #555;
    font-size: 12px; padding: 4px 10px; border-radius: 14px; cursor: pointer;
  }
  .sort-btn:hover { border-color: #B0B8D0; }
  .sort-btn.active { background: #21295C; border-color: #21295C; color: white; }

  .hint { font-size: 11px; color: #999; margin-bottom: 14px; text-align: center; min-height: 14px; }

  .legend-row { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; margin-bottom: 12px; max-width: 900px; display: none; }
  .legend-row.visible { display: flex; }
  .legend-chip { display: flex; align-items: center; gap: 4px; font-size: 10px; color: #666; }
  .legend-dot { width: 8px; height: 8px; border-radius: 50%; }

  .main { display: flex; gap: 20px; align-items: flex-start; }
  #chart-scroll { max-width: min(1100px, 90vw); overflow-x: auto; border-radius: 12px; }
  #chart { position: relative; }

  .tooltip {
    position: fixed;
    background: white;
    border: 1px solid #E0E4F0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    display: none;
    z-index: 100;
    max-width: 260px;
  }
  .tooltip .place { font-weight: bold; font-size: 13px; color: #21295C; margin-bottom: 4px; }
  .tt-quote { margin-top: 6px; padding-top: 6px; border-top: 1px solid #EEE; font-style: italic; color: #444; font-size: 11px; line-height: 1.4; }
  .tt-source { font-style: normal; color: #999; }

  #detail-panel {
    min-width: 260px;
    max-width: 300px;
    background: white;
    border: 1px solid #E0E4F0;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    display: none;
    flex-shrink: 0;
  }
  #detail-panel .close-btn { float: right; cursor: pointer; color: #CCC; font-size: 16px; line-height: 1; }
  #detail-panel .close-btn:hover { color: #666; }
  #detail-panel .dp-pair { font-size: 15px; font-weight: bold; color: #21295C; margin-bottom: 2px; }
  #detail-panel .dp-weight { font-size: 12px; color: #888; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #EEE; }
  #detail-panel h4 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #999; margin-bottom: 6px; }
  #detail-panel .book-row {
    font-size: 12px; color: #444; padding: 5px 0; border-bottom: 1px solid #F5F5F5;
    display: flex; justify-content: space-between; gap: 8px;
  }
  #detail-panel .book-title { flex: 1; }
  #detail-panel .book-count { color: #999; flex-shrink: 0; font-size: 11px; text-align: right; }
</style>
</head>
<body>
<h1>Narrative Topology — Linear Connection Diagram</h1>
<div class="subtitle">Place co-occurrence along a linear axis · arc height = distance · arc width = shared-book strength</div>
<div class="source">5 test authors · document-level co-occurrence · click an arc for the books behind it, hover a place for a text snippet</div>

<div class="controls">
  <label>Min weight: <input type="range" id="threshold" min="1" max="28" value="8" step="1"> <span id="thresholdVal">8</span></label>
  <div class="sort-group" id="sortGroup">
    <span class="sort-label">Sort:</span>
    <button class="sort-btn active" data-sort="frequency">Frequency</button>
    <button class="sort-btn" data-sort="sector">Sector</button>
    <button class="sort-btn" data-sort="alpha">A–Z</button>
  </div>
  <input type="text" id="search" placeholder="Search a place…">
</div>
<div class="hint" id="hint"></div>
<div class="legend-row" id="legendRow"></div>

<div class="main">
  <div id="chart-scroll"><div id="chart"></div></div>
  <div id="detail-panel">
    <span class="close-btn" id="close-detail">&#x2715;</span>
    <div class="dp-pair" id="dp-pair"></div>
    <div class="dp-weight" id="dp-weight"></div>
    <h4>Books connecting these places</h4>
    <div id="dp-books"></div>
  </div>
</div>
<div class="tooltip" id="tooltip"></div>

<script>
const DATA = /*__DATA_JSON__*/;
const allNodesRaw = DATA.nodes;
const allEdges = DATA.edges;
const edgeBooks = DATA.edgeBooks;
const placeSentences = DATA.placeSentences;

const sectorColors = {"Forth":"#4A90D9","Leith":"#1C7293","Inverleith":"#2980B9","New Town":"#8E44AD","Almond":"#5D6D7E","Old Town":"#C0392B","Canongate":"#E74C3C","Western Edinburgh":"#7F8C8D","Craigentinny/Duddingston":"#D35400","Portobello/Craigmillar":"#E67E22","South Central":"#27AE60","South West":"#1E8449","Liberton/Gilmerton":"#2ECC71","Pentlands":"#196F3D","Outer Scotland":"#999999"};
const sectorOrder = ["Leith","Inverleith","New Town","Almond","Old Town","Canongate","Craigentinny/Duddingston","Portobello/Craigmillar","South Central","South West","Liberton/Gilmerton","Forth","Western Edinburgh","Pentlands","Outer Scotland"];

const W_MIN = 1100, H = 500;
const marginLeft = 60, marginRight = 60, nodeSpacing = 58;
const axisY = 380;
const maxWeight = d3.max(allEdges, d => d.weight);
const tooltip = document.getElementById('tooltip');
const panel = document.getElementById('detail-panel');

let sortMode = 'frequency';
let searchTerm = '';

function edgeKey(a, b) { return [a, b].slice().sort().join('|||'); }

function orderNodes(nodes) {
  const arr = nodes.slice();
  if (sortMode === 'alpha') {
    arr.sort((a, b) => a.place.localeCompare(b.place));
  } else if (sortMode === 'sector') {
    arr.sort((a, b) => {
      const sa = sectorOrder.indexOf(a.sector), sb = sectorOrder.indexOf(b.sector);
      return (sa < 0 ? 999 : sa) - (sb < 0 ? 999 : sb) || b.total_mentions - a.total_mentions;
    });
  } else {
    arr.sort((a, b) => b.total_mentions - a.total_mentions);
  }
  return arr;
}

function updateLegend() {
  const row = document.getElementById('legendRow');
  if (sortMode !== 'sector') { row.classList.remove('visible'); row.innerHTML = ''; return; }
  const used = new Set(allNodesRaw.map(n => n.sector));
  row.innerHTML = sectorOrder.filter(s => used.has(s)).map(s =>
    `<span class="legend-chip"><span class="legend-dot" style="background:${sectorColors[s] || '#999'}"></span>${s}</span>`
  ).join('');
  row.classList.add('visible');
}

function showBookPanel(source, target, weight) {
  const books = edgeBooks[edgeKey(source, target)] || [];
  document.getElementById('dp-pair').textContent = source + ' ↔ ' + target;
  document.getElementById('dp-weight').textContent = weight + ' shared book' + (weight === 1 ? '' : 's');
  document.getElementById('dp-books').innerHTML = books.length
    ? books.map(b => `<div class="book-row"><span class="book-title">${b.title}</span><span class="book-count">${b.author}</span></div>`).join('')
    : '<div class="book-row"><span class="book-title">No book details available</span></div>';
  panel.style.display = 'block';
}

document.getElementById('close-detail').addEventListener('click', () => panel.style.display = 'none');

function sentenceHtml(place) {
  const s = placeSentences[place];
  if (!s || !s.length) return '';
  const pick = s[0];
  return `<div class="tt-quote">“${pick.text}”<br><span class="tt-source">— ${pick.book}, ${pick.author}</span></div>`;
}

function draw(threshold) {
  d3.select('#chart svg').remove();
  const edges = allEdges.filter(e => e.weight >= threshold);
  const activePlaces = new Set(edges.flatMap(e => [e.source, e.target]));
  let nodes = allNodesRaw.filter(n => activePlaces.has(n.place));
  nodes = orderNodes(nodes);
  const n = nodes.length;

  document.getElementById('hint').textContent = n === 0
    ? 'No connections at this threshold — lower the slider.'
    : `Showing ${n} places · ${edges.length} connections${searchTerm ? ' · highlighting “' + searchTerm + '”' : ''}`;

  updateLegend();
  if (n === 0) return;

  const W = Math.max(W_MIN, marginLeft + marginRight + (n - 1) * nodeSpacing);

  const xScale = d3.scalePoint()
    .domain(nodes.map(d => d.place))
    .range([marginLeft, W - marginRight])
    .padding(0.5);

  const svg = d3.select('#chart')
    .append('svg')
    .attr('width', W)
    .attr('height', H)
    .style('background', '#F4F6FB')
    .style('border-radius', '12px');

  svg.append('line')
    .attr('x1', marginLeft).attr('y1', axisY)
    .attr('x2', W - marginRight).attr('y2', axisY)
    .attr('stroke', '#C0C8D8').attr('stroke-width', 1.5);

  edges.forEach(e => {
    const x1 = xScale(e.source);
    const x2 = xScale(e.target);
    if (x1 === undefined || x2 === undefined) return;

    const midX = (x1 + x2) / 2;
    const dist = Math.abs(x2 - x1);
    const arcH = dist * 0.42;
    const lw = (e.weight / maxWeight) ** 1.5 * 6;
    const alpha = 0.3 + (e.weight / maxWeight) * 0.5;

    const path = `M ${x1} ${axisY} Q ${midX} ${axisY - arcH} ${x2} ${axisY}`;

    svg.append('path')
      .attr('d', path)
      .attr('fill', 'none')
      .attr('stroke', '#21295C')
      .attr('stroke-width', lw)
      .attr('stroke-opacity', alpha)
      .attr('cursor', 'pointer')
      .on('mouseover', function () {
        d3.select(this).attr('stroke', '#B85042').attr('stroke-opacity', 0.9);
        tooltip.style.display = 'block';
        tooltip.innerHTML = `
          <div class="place">${e.source} ↔ ${e.target}</div>
          <div style="color:#888">Co-occurrence weight: <strong style="color:#21295C">${e.weight}</strong></div>
          <div style="color:#AAA;font-size:10px;margin-top:4px">Click for the book list</div>`;
      })
      .on('mousemove', function (event) {
        tooltip.style.left = (event.clientX + 14) + 'px';
        tooltip.style.top = (event.clientY - 10) + 'px';
      })
      .on('mouseout', function () {
        d3.select(this).attr('stroke', '#21295C').attr('stroke-opacity', alpha);
        tooltip.style.display = 'none';
      })
      .on('click', function () {
        tooltip.style.display = 'none';
        showBookPanel(e.source, e.target, e.weight);
      });
  });

  nodes.forEach(d => {
    const x = xScale(d.place);
    const r = Math.log1p(d.total_mentions) * 2.2;
    const dim = searchTerm && !d.place.toLowerCase().includes(searchTerm.toLowerCase());
    const fill = sortMode === 'sector' ? (sectorColors[d.sector] || '#999') : '#B85042';

    svg.append('circle')
      .attr('cx', x).attr('cy', axisY)
      .attr('r', r)
      .attr('fill', fill)
      .attr('fill-opacity', dim ? 0.25 : 1)
      .attr('stroke', 'white')
      .attr('stroke-width', 1.5)
      .attr('cursor', 'pointer')
      .on('mouseover', function () {
        d3.select(this).attr('fill', '#21295C').attr('fill-opacity', 1);
        tooltip.style.display = 'block';
        tooltip.innerHTML = `
          <div class="place">${d.place}</div>
          <div style="color:#888">${d.total_mentions} mentions · ${d.sector}</div>
          ${sentenceHtml(d.place)}`;
      })
      .on('mousemove', function (event) {
        tooltip.style.left = (event.clientX + 14) + 'px';
        tooltip.style.top = (event.clientY - 10) + 'px';
      })
      .on('mouseout', function () {
        d3.select(this).attr('fill', fill).attr('fill-opacity', dim ? 0.25 : 1);
        tooltip.style.display = 'none';
      });

    svg.append('text')
      .attr('x', x)
      .attr('y', axisY + r + 14)
      .attr('text-anchor', 'end')
      .attr('transform', `rotate(-45, ${x}, ${axisY + r + 14})`)
      .attr('font-size', '10px')
      .attr('fill', dim ? '#CCC' : (sortMode === 'sector' ? (sectorColors[d.sector] || '#444') : '#444'))
      .text(d.place);
  });
}

draw(8);

document.getElementById('threshold').addEventListener('input', function () {
  document.getElementById('thresholdVal').textContent = this.value;
  draw(+this.value);
});

document.querySelectorAll('.sort-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    sortMode = this.dataset.sort;
    draw(+document.getElementById('threshold').value);
  });
});

document.getElementById('search').addEventListener('input', function () {
  searchTerm = this.value.trim();
  draw(+document.getElementById('threshold').value);
});
</script>
</body>
</html>
"""


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    data_json = json.dumps(data, ensure_ascii=False)

    if OUT_PATH.exists():
        shutil.copy(OUT_PATH, BACKUP_PATH)
        print(f"Backed up previous version to {BACKUP_PATH}")

    html = TEMPLATE.replace("/*__DATA_JSON__*/", data_json)
    OUT_PATH.write_text(html)
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
