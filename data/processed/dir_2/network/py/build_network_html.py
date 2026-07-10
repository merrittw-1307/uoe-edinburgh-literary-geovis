"""
Rebuilds network.html from data/network_enriched.json.

Adds: click node -> detail panel (top co-occurrences, book list, sample
sentence) and an absolute/percentage node-size toggle. Backs up the
previous version to network_v2.html before overwriting (network_v1.html is
already an older backup from a prior iteration).
"""
import json
import shutil
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
DATA_PATH = REPO_ROOT / "data/processed/dir_2/network/data/network_enriched.json"
OUT_PATH = REPO_ROOT / "data/processed/dir_2/network/d3/network.html"
BACKUP_PATH = REPO_ROOT / "data/processed/dir_2/network/d3/network_v2.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Narrative Topology Network</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background: #F8F9FC;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
  }
  h1 { font-size: 20px; color: #21295C; margin-bottom: 6px; text-align: center; }
  .subtitle { font-size: 13px; color: #888; margin-bottom: 16px; text-align: center; }
  .controls { display: flex; gap: 20px; margin-bottom: 16px; align-items: center; font-size: 13px; color: #555; flex-wrap: wrap; justify-content: center; }
  input[type=range] { width: 120px; }
  .toggle-group { display: flex; align-items: center; gap: 6px; }
  .toggle-btn {
    border: 1px solid #DADFEE; background: white; color: #555;
    font-size: 12px; padding: 4px 10px; border-radius: 14px; cursor: pointer;
  }
  .toggle-btn:hover { border-color: #B0B8D0; }
  .toggle-btn.active { background: #21295C; border-color: #21295C; color: white; }
  .hint { font-size: 11px; color: #999; margin-bottom: 12px; text-align: center; }

  .main { display: flex; gap: 20px; align-items: flex-start; }
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
    min-width: 200px;
  }
  .tooltip .place { font-weight: bold; font-size: 13px; color: #21295C; margin-bottom: 4px; }

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
  #detail-panel .np-place { font-size: 16px; font-weight: bold; color: #21295C; margin-bottom: 2px; }
  #detail-panel .np-meta { font-size: 12px; color: #888; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #EEE; }
  #detail-panel h4 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #999; margin-bottom: 6px; margin-top: 10px; }
  #detail-panel .co-row, #detail-panel .book-row {
    font-size: 12px; color: #444; padding: 4px 0; border-bottom: 1px solid #F5F5F5;
    display: flex; justify-content: space-between; gap: 8px;
  }
  #detail-panel .book-title, #detail-panel .co-place { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #detail-panel .book-count, #detail-panel .co-weight { color: #999; flex-shrink: 0; font-size: 11px; }
  #detail-panel .np-quote { margin-top: 10px; font-style: italic; color: #444; font-size: 11px; line-height: 1.4; padding-top: 8px; border-top: 1px solid #EEE; }
  #detail-panel .tt-source { font-style: normal; color: #999; }
</style>
</head>
<body>
<h1>Narrative Topology Network</h1>
<div class="subtitle">Place co-occurrence across literary works · drag nodes · scroll to zoom · click a node for details</div>
<div class="controls">
  <label>Min co-occurrence weight: <input type="range" id="threshold" min="1" max="28" value="8" step="1"> <span id="thresholdVal">8</span></label>
  <div class="toggle-group" id="scaleGroup">
    <span>Node size:</span>
    <button class="toggle-btn active" data-scale="absolute">Absolute</button>
    <button class="toggle-btn" data-scale="percentage">Percentage</button>
  </div>
</div>
<div class="hint" id="hint"></div>

<div class="main">
  <div id="chart"></div>
  <div id="detail-panel">
    <span class="close-btn" id="close-detail">&#x2715;</span>
    <div class="np-place" id="np-place"></div>
    <div class="np-meta" id="np-meta"></div>
    <h4>Top co-occurring places</h4>
    <div id="np-cooccur"></div>
    <h4>Books mentioning this place</h4>
    <div id="np-books"></div>
    <div class="np-quote" id="np-quote"></div>
  </div>
</div>
<div class="tooltip" id="tooltip"></div>

<script>
const DATA = /*__DATA_JSON__*/;
const allNodes = DATA.nodes;
const allEdges = DATA.edges;
const placeBooks = DATA.placeBooks;
const placeSentences = DATA.placeSentences;

const W = 900, H = 700;
const maxWeight = d3.max(allEdges, d => d.weight);
const totalMentionsAll = d3.sum(allNodes, d => d.total_mentions);
const tooltip = document.getElementById('tooltip');
const panel = document.getElementById('detail-panel');

let scaleMode = 'absolute';

const svg = d3.select('#chart')
  .append('svg')
  .attr('width', W)
  .attr('height', H)
  .style('background', '#F4F6FB')
  .style('border-radius', '12px');

const g = svg.append('g');

svg.call(d3.zoom()
  .scaleExtent([0.3, 3])
  .on('zoom', e => g.attr('transform', e.transform)));

function nodeRadius(d) {
  if (scaleMode === 'percentage') {
    return Math.sqrt(d.total_mentions / totalMentionsAll) * 260 + 3;
  }
  return Math.log1p(d.total_mentions) * 2.8;
}

function mentionsLabel(d) {
  return scaleMode === 'percentage'
    ? (d.total_mentions / totalMentionsAll * 100).toFixed(1) + '% of shown mentions'
    : d.total_mentions + ' total mentions';
}

function topCooccurrences(d, simEdges) {
  return simEdges
    .filter(e => (e.source.place || e.source) === d.place || (e.target.place || e.target) === d.place)
    .sort((a, b) => b.weight - a.weight)
    .slice(0, 5)
    .map(e => {
      const sp = e.source.place || e.source;
      const tp = e.target.place || e.target;
      return { place: sp === d.place ? tp : sp, weight: e.weight };
    });
}

function closePanel() { panel.style.display = 'none'; }
document.getElementById('close-detail').addEventListener('click', closePanel);

function showNodePanel(d, connected) {
  document.getElementById('np-place').textContent = d.place;
  document.getElementById('np-meta').textContent = `${d.sector} · ${mentionsLabel(d)}`;
  document.getElementById('np-cooccur').innerHTML = connected.length
    ? connected.map(c => `<div class="co-row"><span class="co-place">${c.place}</span><span class="co-weight">${c.weight}</span></div>`).join('')
    : '<div class="co-row"><span class="co-place">No co-occurrences at this threshold</span></div>';
  const books = placeBooks[d.place] || [];
  document.getElementById('np-books').innerHTML = books.length
    ? books.map(b => `<div class="book-row"><span class="book-title">${b.title}</span><span class="book-count">${b.mentions}×</span></div>`).join('')
    : '<div class="book-row"><span class="book-title">No book details available</span></div>';
  const s = placeSentences[d.place];
  document.getElementById('np-quote').innerHTML = (s && s.length)
    ? `“${s[0].text}”<br><span class="tt-source">— ${s[0].book}, ${s[0].author}</span>`
    : '';
  panel.style.display = 'block';
}

function draw(threshold) {
  g.selectAll('*').remove();

  const edges = allEdges.filter(e => e.weight >= threshold);
  const activePlaces = new Set(edges.flatMap(e => [e.source, e.target]));
  const activeNodes = allNodes
    .filter(n => activePlaces.has(n.place))
    .map(n => ({...n}));

  document.getElementById('hint').textContent = activeNodes.length
    ? `Showing ${activeNodes.length} places · ${edges.length} connections`
    : 'No connections at this threshold — lower the slider.';

  const simEdges = edges.map(e => ({...e}));

  const simulation = d3.forceSimulation(activeNodes)
    .force('link', d3.forceLink(simEdges)
      .id(d => d.place)
      .distance(d => 280 / d.weight * 8)
      .strength(0.7))
    .force('charge', d3.forceManyBody().strength(-400))
    .force('center', d3.forceCenter(W / 2, H / 2))
    .force('collision', d3.forceCollide(d => nodeRadius(d) + 18));

  const link = g.append('g')
    .selectAll('line')
    .data(simEdges)
    .join('line')
    .attr('stroke', '#A26769')
    .attr('stroke-opacity', 0.45)
    .attr('stroke-width', d => (d.weight / maxWeight) ** 2 * 12);

  const node = g.append('g')
    .selectAll('circle')
    .data(activeNodes)
    .join('circle')
    .attr('r', d => nodeRadius(d))
    .attr('fill', '#21295C')
    .attr('stroke', 'white')
    .attr('stroke-width', 1.5)
    .attr('opacity', 0.9)
    .attr('cursor', 'pointer')
    .call(d3.drag()
      .on('start', (event, d) => {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x; d.fy = d.y;
      })
      .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
      .on('end', (event, d) => {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null; d.fy = null;
      }))
    .on('mouseover', function (event, d) {
      d3.select(this).attr('fill', '#B85042');
      const connected = topCooccurrences(d, simEdges);
      tooltip.style.display = 'block';
      tooltip.innerHTML = `
        <div class="place">${d.place}</div>
        <div style="color:#888;font-size:11px;margin-bottom:6px">${mentionsLabel(d)} · ${d.sector}</div>
        <div style="font-size:11px;color:#555;margin-bottom:3px">Top co-occurrences:</div>
        ${connected.map(c => `<div style="display:flex;justify-content:space-between;gap:16px;margin-top:3px"><span>${c.place}</span><span style="color:#21295C;font-weight:bold">${c.weight}</span></div>`).join('')}
        <div style="color:#AAA;font-size:10px;margin-top:6px">Click for books &amp; a text snippet</div>`;
    })
    .on('mousemove', function (event) {
      tooltip.style.left = (event.clientX + 14) + 'px';
      tooltip.style.top = (event.clientY - 10) + 'px';
    })
    .on('mouseout', function () {
      d3.select(this).attr('fill', '#21295C');
      tooltip.style.display = 'none';
    })
    .on('click', function (event, d) {
      tooltip.style.display = 'none';
      showNodePanel(d, topCooccurrences(d, simEdges));
    });

  const label = g.append('g')
    .selectAll('text')
    .data(activeNodes)
    .join('text')
    .attr('text-anchor', 'middle')
    .attr('font-size', '10px')
    .attr('fill', '#333')
    .attr('font-weight', '500')
    .attr('pointer-events', 'none')
    .text(d => d.place);

  simulation.on('tick', () => {
    link
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y);

    node
      .attr('cx', d => d.x)
      .attr('cy', d => d.y);

    label
      .attr('x', d => d.x)
      .attr('y', d => d.y + nodeRadius(d) + 12);
  });
}

draw(8);

document.getElementById('threshold').addEventListener('input', function () {
  document.getElementById('thresholdVal').textContent = this.value;
  draw(+this.value);
});

document.querySelectorAll('.toggle-btn').forEach(btn => {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    scaleMode = this.dataset.scale;
    draw(+document.getElementById('threshold').value);
  });
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
