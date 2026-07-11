"""
Builds combined_interface.html from the four scale-exploration author-level
JSON datasets (radar, barcode, small_multiples, network/linear share one).

Replaces the iframe-scaffold version: radar, barcode, small_multiples,
network and linear now render live in-page, driven by one shared
selectedAuthors array (the author selector) and one shared focusedAuthor
value (cross-view linking: click an author's shape/row/panel in a
Fingerprints view, then switch to Topology to see their places highlighted).

Metro is the one exception -- its lines depend on offline community
detection (see build_metro_lines.py), so it stays an <iframe> that swaps
between the two precomputed snapshots (5-author canonical, 20-author) based
on how many authors are currently selected, rather than recomputing live.

The outer detail panel is driven by all_authors_sentences.json (see
generate_all_authors_sentences.py), keyed by (author, place) for each
author's own top-15 places -- exactly the set reachable through the live
views, so no unreachable data is shipped.
"""
import json
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
SCALE_DATA = REPO_ROOT / "data/processed/scale_exploration/data"
COMBINED_DATA = REPO_ROOT / "data/processed/combined/data"
OUT_PATH = REPO_ROOT / "data/processed/combined/d3/combined_interface.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Combined Interface — Fingerprints &amp; Topology</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    font-family: "Helvetica Neue", Arial, sans-serif;
    background: #F8F9FC;
    color: #2C2C2A;
    display: flex;
    flex-direction: column;
  }

  header {
    background: #21295C;
    color: white;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
  }
  header h1 { font-size: 16px; font-weight: bold; margin-right: auto; }
  header .byline { font-size: 11px; color: #C7CBE8; margin-right: 24px; }
  .dir-tabs { display: flex; gap: 8px; }
  .dir-tab {
    background: rgba(255,255,255,0.08);
    color: #E6E8F5;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 6px;
    padding: 7px 16px;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .dir-tab:hover { background: rgba(255,255,255,0.16); }
  .dir-tab.active { background: #C9A227; color: #21295C; border-color: #C9A227; font-weight: bold; }

  .status-banner {
    background: #E9F7EF;
    border-bottom: 1px solid #C5E8D3;
    color: #1E5C3A;
    font-size: 12px;
    padding: 8px 24px;
    line-height: 1.5;
  }
  .status-banner strong { color: #0F3D24; }

  .body-wrap { flex: 1; display: flex; min-height: 0; }

  .side-panel {
    width: 280px;
    flex-shrink: 0;
    background: white;
    border-right: 1px solid #E0E4F0;
    padding: 18px 16px;
    overflow-y: auto;
  }
  .side-section { margin-bottom: 22px; }
  .side-section h3 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #888;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #E0E4F0;
  }
  .viz-option {
    display: block;
    width: 100%;
    text-align: left;
    background: #F8F9FC;
    border: 1px solid #E0E4F0;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 8px;
    cursor: pointer;
    font-size: 13px;
    color: #2C2C2A;
    transition: all 0.15s;
  }
  .viz-option:hover { border-color: #21295C; }
  .viz-option.active { background: #21295C; color: white; border-color: #21295C; font-weight: bold; }
  .viz-option .role { display: block; font-size: 11px; color: inherit; opacity: 0.7; font-weight: normal; margin-top: 2px; }

  .preset-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 8px; }
  .preset-btn {
    border: 1.5px solid #C0C8D8; background: white; border-radius: 14px;
    padding: 4px 10px; font-size: 11px; cursor: pointer; color: #333;
  }
  .preset-btn:hover { border-color: #21295C; background: #E8EAF6; }
  .preset-btn.active { background: #21295C; color: white; border-color: #21295C; }
  .clear-btn {
    border: 1.5px solid #B85042; color: #B85042; background: white; border-radius: 14px;
    padding: 4px 10px; font-size: 11px; cursor: pointer; margin-bottom: 10px;
  }
  .clear-btn:hover { background: #FBEAE8; }
  #author-search-wrap { position: relative; margin-bottom: 10px; }
  #author-search-wrap input[type=text] {
    width: 100%; border: 1px solid #C0C8D8; border-radius: 14px; padding: 5px 10px; font-size: 11px;
  }
  #author-suggestions {
    position: absolute; left: 0; right: 0; background: white; border: 1px solid #E0E4F0; border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12); max-height: 180px; overflow-y: auto; z-index: 50; display: none; font-size: 11px;
  }
  #author-suggestions div { padding: 5px 10px; cursor: pointer; }
  #author-suggestions div:hover { background: #F0F2FA; }
  .chip-list { display: flex; flex-wrap: wrap; gap: 5px; }
  .chip {
    display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px;
    background: #EEF0FA; color: #21295C; border-radius: 10px; padding: 3px 8px;
  }
  .chip.focus { background: #FFF4D6; color: #856404; border: 1px solid #C9A227; }
  .chip-x { cursor: pointer; color: #AAA; font-size: 10px; }
  .chip-x:hover { color: #B85042; }
  .chip-empty { font-size: 11px; color: #AAA; font-style: italic; }
  .focus-hint { font-size: 10.5px; color: #888; margin-top: 8px; line-height: 1.4; }

  .scale-link {
    display: block; font-size: 12px; color: #21295C; text-decoration: none;
    padding: 8px 10px; background: #EEF0FA; border-radius: 6px; margin-top: 4px;
  }
  .scale-link:hover { background: #E0E4F0; }

  .main-view { flex: 1; display: flex; flex-direction: column; min-width: 0; }
  .view-header {
    padding: 10px 20px; background: white; border-bottom: 1px solid #E0E4F0;
    font-size: 13px; color: #666;
  }
  .view-header .active-name { color: #21295C; font-weight: bold; }
  .status-text { font-size: 11px; color: #999; margin-top: 2px; }
  #extra-controls { display: none; align-items: center; gap: 8px; font-size: 12px; color: #555; margin-top: 6px; }
  #extra-controls input[type=range] { width: 140px; }

  .viz-host { flex: 1; overflow: auto; padding: 18px 20px; }
  .viz-panel { display: none; }
  .viz-panel.active { display: block; }

  .radar-main, .net-main { display: flex; gap: 18px; align-items: flex-start; }
  .legend {
    display: flex; flex-direction: column; gap: 3px; max-height: 600px; overflow-y: auto;
    min-width: 200px; max-width: 240px; border: 1px solid #E0E4F0; border-radius: 10px; padding: 8px; background: white;
  }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #333; padding: 3px 6px; border-radius: 6px; cursor: pointer; }
  .legend-item:hover { background: #F0F2FA; }
  .legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }
  .legend-remove { margin-left: auto; color: #CCC; font-size: 12px; }
  .legend-remove:hover { color: #B85042; }

  .author-row {
    margin-bottom: 14px; padding: 8px 10px; background: white; border-radius: 8px;
    border: 1.5px solid #E8EAF0; cursor: pointer; transition: all 0.15s;
  }
  .author-row.focused { border-color: #C9A227; box-shadow: 0 0 0 2px rgba(201,162,39,0.25); }
  .author-row.dimmed { opacity: 0.4; }
  .author-header { display: flex; align-items: baseline; gap: 10px; margin-bottom: 4px; }
  .author-label { font-size: 12.5px; font-weight: bold; color: #21295C; }
  .author-meta { font-size: 10px; color: #AAA; }
  .bars { display: flex; align-items: flex-end; height: 60px; gap: 2px; }
  .bar-wrap { display: flex; flex-direction: column; align-items: center; width: 46px; flex-shrink: 0; }
  .bar { width: 100%; border-radius: 2px 2px 0 0; }
  .bar-label { font-size: 8px; color: #888; margin-top: 2px; max-width: 46px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

  .sm-grid { display: flex; flex-wrap: wrap; gap: 12px; }
  .sm-panel {
    background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    overflow: hidden; width: 220px; cursor: pointer; border: 1.5px solid transparent; transition: all 0.15s;
  }
  .sm-panel.focused { border-color: #C9A227; box-shadow: 0 0 0 2px rgba(201,162,39,0.25); }
  .sm-panel.dimmed { opacity: 0.4; }
  .sm-panel-title { font-size: 11px; font-weight: bold; padding: 6px 8px 3px; color: #21295C; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .sm-panel-stats { font-size: 9px; color: #AAA; padding: 0 8px 4px; }
  .sm-map-wrap { width: 220px; height: 160px; }
  .leaflet-popup-content-wrapper { border-radius: 6px !important; font-size: 11px; }

  #linear-chart-scroll { max-width: 100%; overflow-x: auto; border-radius: 12px; }

  .metro-note {
    font-size: 11px; color: #856404; background: #FFF8E7; border-left: 3px solid #C9A227;
    padding: 7px 10px; border-radius: 0 6px 6px 0; margin-bottom: 10px; max-width: 760px;
  }
  #metro-iframe { width: 100%; height: 640px; border: none; border-radius: 10px; }

  .tooltip {
    position: fixed; background: white; border: 1px solid #E0E4F0; border-radius: 8px;
    padding: 8px 12px; font-size: 12px; color: #333; pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1); display: none; z-index: 100; max-width: 240px;
  }

  .detail-panel {
    width: 260px; flex-shrink: 0; background: white; border-left: 1px solid #E0E4F0;
    padding: 18px 16px; overflow-y: auto; font-size: 12px; color: #666; line-height: 1.6;
  }
  .detail-panel h3 {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #888;
    margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #E0E4F0;
  }
  .detail-panel .info-block { background: #F8F9FC; border-radius: 8px; padding: 10px; margin-bottom: 14px; }
  .detail-panel .todo-block { background: #F8F9FC; border: 1px dashed #C7CBE8; border-radius: 8px; padding: 10px; margin-bottom: 14px; }
  .detail-panel code { background: #EEF0FA; padding: 1px 4px; border-radius: 3px; font-size: 11px; }
  .todo-tag { display: inline-block; font-size: 10px; background: #FFF8E7; color: #856404; border-radius: 4px; padding: 2px 6px; }
  .done-tag { display: inline-block; font-size: 10px; background: #E9F7EF; color: #1E5C3A; border-radius: 4px; padding: 2px 6px; }
  .dp-name { font-size: 14px; font-weight: bold; color: #21295C; margin-bottom: 2px; }
  .dp-meta { font-size: 11px; color: #888; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #EEE; }
  .detail-panel h4 { font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.04em; color: #999; margin: 10px 0 5px; }
  .dp-row { font-size: 11.5px; color: #444; padding: 3px 0; border-bottom: 1px solid #F5F5F5; display: flex; justify-content: space-between; gap: 8px; }
  .dp-row .dp-lbl { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .dp-row .dp-val { color: #999; flex-shrink: 0; font-size: 11px; }
  .dp-quote { margin-top: 8px; padding-top: 6px; border-top: 1px dashed #E0E4F0; font-style: italic; color: #444; font-size: 11px; line-height: 1.4; }
  .dp-quote .dp-src { font-style: normal; color: #999; display: block; margin-top: 3px; }
  .dp-empty { font-size: 11px; color: #AAA; font-style: italic; }
</style>
</head>
<body>

<header>
  <h1>Combined Interface</h1>
  <div class="byline">Merritt Wang (S2887338) &middot; Ch.4 &ldquo;Combined Interface&rdquo; deliverable</div>
  <div class="dir-tabs">
    <button class="dir-tab active" data-dir="fingerprints">Fingerprints</button>
    <button class="dir-tab" data-dir="topology">Topology</button>
  </div>
</header>

<div class="status-banner">
  <strong>Author selector, cross-view linking, and the outer detail panel are all live.</strong>
  Radar, bar-code, small multiples, network and linear all re-render from the shared author selection below
  using the same client-side computation as the scale-exploration tools. Click an author's shape/row/panel in a
  Fingerprints view, then switch to Topology, to see their places highlighted there (and vice-versa is not yet built).
  Hover any place, bar, node, or panel to see a real example sentence from <code>api_sentence</code> in the right-hand
  detail panel. The metro map is the one exception &mdash; its lines depend on offline community detection, so it swaps
  between precomputed 5- and 20-author snapshots rather than recomputing live, and does not feed the detail panel.
</div>

<div class="body-wrap">

  <div class="side-panel">
    <div class="side-section">
      <h3>Visualisation</h3>
      <div id="viz-picker-list"></div>
    </div>

    <div class="side-section">
      <h3>Authors <span class="done-tag">live</span></h3>
      <div class="preset-row" id="author-presets">
        <button class="preset-btn" data-preset="2">2</button>
        <button class="preset-btn active" data-preset="5">5 (baseline)</button>
        <button class="preset-btn" data-preset="20">Top 20</button>
        <button class="preset-btn" data-preset="50">Top 50</button>
      </div>
      <div id="author-search-wrap">
        <input type="text" id="author-search" placeholder="Add an author&hellip;" autocomplete="off">
        <div id="author-suggestions"></div>
      </div>
      <button class="clear-btn" id="btn-clear-authors">Clear all</button>
      <div class="chip-list" id="author-chips"></div>
    </div>

    <div class="side-section">
      <h3>Cross-view Focus <span class="done-tag">live</span></h3>
      <div id="focus-chip"></div>
      <div class="focus-hint">Click an author's shape (radar), row (bar-code) or map panel (small multiples) to focus them &mdash; then switch to Topology to see their places highlighted.</div>
    </div>

    <div class="side-section">
      <h3>Scale Exploration</h3>
      <a class="scale-link" href="../../scale_exploration/d3/radar_scale_explore.html">Radar &mdash; 2 to 408 authors &rarr;</a>
      <a class="scale-link" href="../../scale_exploration/d3/network_scale_explore.html" style="margin-top:6px;">Network &mdash; 2 to 408 authors &rarr;</a>
      <a class="scale-link" href="../../../../index.html" style="margin-top:6px;">&#x21A9; back to all six (static)</a>
    </div>
  </div>

  <div class="main-view">
    <div class="view-header">
      <div>Now viewing: <span class="active-name" id="active-name">Radar Chart</span></div>
      <div class="status-text" id="status-text"></div>
      <div id="extra-controls"></div>
    </div>
    <div class="viz-host">

      <div class="viz-panel active" id="panel-radar">
        <div class="radar-main">
          <div id="radar-chart"></div>
          <div class="legend" id="radar-legend"></div>
        </div>
      </div>

      <div class="viz-panel" id="panel-barcode">
        <div id="barcode-rows"></div>
      </div>

      <div class="viz-panel" id="panel-small_multiples">
        <div class="sm-grid" id="sm-grid"></div>
      </div>

      <div class="viz-panel" id="panel-network">
        <div class="net-main">
          <div id="network-chart"></div>
        </div>
      </div>

      <div class="viz-panel" id="panel-linear">
        <div id="linear-chart-scroll"><div id="linear-chart"></div></div>
      </div>

      <div class="viz-panel" id="panel-metro">
        <div class="metro-note" id="metro-note"></div>
        <iframe id="metro-iframe" src="../../dir_2/metro/d3/metro.html"></iframe>
      </div>

    </div>
    <div class="tooltip" id="tooltip"></div>
  </div>

  <div class="detail-panel">
    <h3>Detail Panel <span class="done-tag">live</span></h3>
    <div class="info-block" id="detail-live">
      <div class="dp-empty">Hover a place, bar, node, or panel to see an example sentence from <code>api_sentence</code>.</div>
    </div>
    <h3>Cross-view Linking</h3>
    <div class="info-block">
      <span class="done-tag">implemented</span>
      <p style="margin-top:6px;">Click an author in a Fingerprints view to focus them (gold highlight). Switch to a Topology view: that
      author's top-15 places are highlighted gold among the current selection's combined graph, others dimmed. Clear the focus chip
      on the left to reset. The metro map does not participate (see note below).</p>
    </div>
    <h3>Data Reuse</h3>
    <p>Radar, bar-code, small multiples, network and linear all read live from the same four scale-exploration JSON bundles
    (<code>all_authors_radar.json</code>, <code>all_authors_barcode.json</code>, <code>all_authors_small_multiples.json</code>,
    <code>all_authors_network.json</code>), covering any subset of the 408 authors with location data. The detail panel adds a
    fifth bundle, <code>all_authors_sentences.json</code>, sampled directly from <code>api_sentence</code> for each author's own
    top-15 places.</p>
  </div>

</div>

<script>
const ALL_AUTHORS_RADAR = /*__RADAR_JSON__*/;
const ALL_AUTHORS_BARCODE = /*__BARCODE_JSON__*/;
const ALL_AUTHORS_SM = /*__SM_JSON__*/;
const NETWORK_RAW = /*__NETWORK_JSON__*/;
const ALL_AUTHORS_SENTENCES = /*__SENTENCES_JSON__*/;

const radarByName = {}; ALL_AUTHORS_RADAR.forEach(a => radarByName[a.author] = a);
const barcodeByName = {}; ALL_AUTHORS_BARCODE.forEach(a => barcodeByName[a.author] = a);
const smByName = {}; ALL_AUTHORS_SM.forEach(a => smByName[a.author] = a);
const MENTIONS = NETWORK_RAW.mentions;
const DOCUMENTS = NETWORK_RAW.documents;
const ALL_AUTHOR_NAMES = [...ALL_AUTHORS_RADAR].sort((a,b) => b.total_mentions - a.total_mentions).map(a => a.author);

const SECTORS = ["Almond","Canongate","Craigentinny/Duddingston","Forth","Inverleith","Leith","Liberton/Gilmerton","New Town","Old Town","Pentlands","Portobello/Craigmillar","South Central","South West","Western Edinburgh"];
const sectorColors = {"Forth":"#4A90D9","Leith":"#1C7293","Inverleith":"#2980B9","New Town":"#8E44AD","Almond":"#5D6D7E","Old Town":"#C0392B","Canongate":"#E74C3C","Western Edinburgh":"#7F8C8D","Craigentinny/Duddingston":"#D35400","Portobello/Craigmillar":"#E67E22","South Central":"#27AE60","South West":"#1E8449","Liberton/Gilmerton":"#2ECC71","Pentlands":"#196F3D","Outer Scotland":"#999999"};

const directions = {
  fingerprints: [
    { id: 'radar', name: 'Radar Chart', role: 'Primary design' },
    { id: 'barcode', name: 'Bar-code Fingerprint', role: 'Secondary design' },
    { id: 'small_multiples', name: 'Small Multiples', role: 'Tertiary design' }
  ],
  topology: [
    { id: 'network', name: 'Force-Directed Network', role: 'Primary design' },
    { id: 'linear', name: 'Linear Connection Diagram', role: 'Secondary design' },
    { id: 'metro', name: 'Metro-Style Map', role: 'Illustrative design' }
  ]
};

let currentDir = 'fingerprints';
let currentViz = 'radar';
let selectedAuthors = [];
let focusedAuthor = null;
let networkThreshold = 1;
let linearThreshold = 2;
let networkSim = null;
let smMaps = [];

function colorForAuthor(name, idx) { const hue = (idx * 47) % 360; return `hsl(${hue}, 65%, 45%)`; }
function nodeRadius(mentions) { return Math.max(Math.log1p(mentions) * 2.6, 3); }
function setStatus(text) { document.getElementById('status-text').textContent = text; }
function showTooltip(html, ev) {
  const t = document.getElementById('tooltip');
  t.style.display = 'block'; t.innerHTML = html;
  t.style.left = (ev.clientX + 14) + 'px'; t.style.top = (ev.clientY - 10) + 'px';
}
function moveTooltip(ev) {
  const t = document.getElementById('tooltip');
  t.style.left = (ev.clientX + 14) + 'px'; t.style.top = (ev.clientY - 10) + 'px';
}
function hideTooltip() { document.getElementById('tooltip').style.display = 'none'; }

/* ---- outer detail panel (api_sentence-backed) ---- */
function sectorForPlace(place) {
  const row = MENTIONS.find(m => m.place === place);
  return row ? row.sector : null;
}
function clearDetail() {
  document.getElementById('detail-live').innerHTML = '<div class="dp-empty">Hover a place, bar, node, or panel to see an example sentence from <code>api_sentence</code>.</div>';
}
function showDetailForPlace(place, authors) {
  const seen = new Set();
  const sentences = [];
  authors.forEach(author => {
    const list = (ALL_AUTHORS_SENTENCES[author] || {})[place];
    if (list) list.forEach(s => { if (!seen.has(s.text)) { seen.add(s.text); sentences.push({...s, author}); } });
  });
  const bookCounts = {};
  MENTIONS.filter(m => m.place === place && authors.includes(m.author)).forEach(m => {
    bookCounts[m.doc_title] = (bookCounts[m.doc_title] || 0) + m.mentions;
  });
  const bookList = Object.entries(bookCounts).sort((a,b) => b[1]-a[1]).slice(0, 5);
  const sector = sectorForPlace(place);

  const host = document.getElementById('detail-live');
  host.innerHTML =
    `<div class="dp-name">${place}</div>` +
    `<div class="dp-meta">${sector ? sector + ' &middot; ' : ''}${authors.length===1 ? authors[0] : authors.length+' authors in view'}</div>` +
    (bookList.length ? `<h4>Books mentioning this place</h4>` + bookList.map(([title,count]) => `<div class="dp-row"><span class="dp-lbl">${title}</span><span class="dp-val">${count}</span></div>`).join('') : '') +
    (sentences.length ? `<h4>Example sentence</h4>` + sentences.slice(0,2).map(s => `<div class="dp-quote">&ldquo;${s.text}&rdquo;<span class="dp-src">${s.book} &middot; ${s.author}</span></div>`).join('') : '<div class="dp-empty" style="margin-top:8px;">No sample sentence found for this pair.</div>');
}
function showDetailForAuthor(name) {
  const rec = barcodeByName[name];
  if (!rec || !rec.places.length) { clearDetail(); return; }
  showDetailForPlace(rec.places[0].place, [name]);
}

function dragBehavior(sim) {
  return d3.drag()
    .on('start', (ev,d) => { if (!ev.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
    .on('drag', (ev,d) => { d.fx=ev.x; d.fy=ev.y; })
    .on('end', (ev,d) => { if (!ev.active) sim.alphaTarget(0); d.fx=null; d.fy=null; });
}

/* ---- shared topology graph builder (network + linear) ---- */
function topPlacesPerAuthor(rows, topN) {
  const byAuthorPlace = {};
  rows.forEach(r => { const k = r.author+'|||'+r.place; byAuthorPlace[k] = (byAuthorPlace[k]||0) + r.mentions; });
  const byAuthor = {};
  Object.entries(byAuthorPlace).forEach(([key, mentions]) => {
    const [author, place] = key.split('|||');
    (byAuthor[author] = byAuthor[author] || []).push({place, mentions});
  });
  const active = new Set();
  Object.values(byAuthor).forEach(list => list.sort((a,b) => b.mentions-a.mentions).slice(0, topN).forEach(x => active.add(x.place)));
  return active;
}
function buildGraph(authors) {
  const rows0 = MENTIONS.filter(m => authors.includes(m.author));
  const activePlaces = topPlacesPerAuthor(rows0, 15);
  const rows = rows0.filter(r => activePlaces.has(r.place));
  const nodeMentions = {};
  rows.forEach(r => { nodeMentions[r.place] = (nodeMentions[r.place]||0) + r.mentions; });
  const byDoc = {};
  rows.forEach(r => { (byDoc[r.document_id] = byDoc[r.document_id] || new Set()).add(r.place); });
  const edgeWeight = {};
  Object.values(byDoc).forEach(set => {
    const places = [...set].sort();
    for (let i=0;i<places.length;i++) for (let j=i+1;j<places.length;j++) {
      const key = places[i]+'|||'+places[j];
      edgeWeight[key] = (edgeWeight[key]||0)+1;
    }
  });
  const nodes = Object.entries(nodeMentions).map(([place, mentions]) => ({place, mentions}));
  const edges = Object.entries(edgeWeight).map(([key, weight]) => { const [source,target]=key.split('|||'); return {source, target, weight}; });
  return {nodes, edges};
}
function focusPlacesFor(name) {
  if (!name) return new Set();
  const rows = MENTIONS.filter(m => m.author === name);
  return topPlacesPerAuthor(rows, 15);
}

/* ---- author selector ---- */
function presetAuthors(kind) {
  if (kind === '2') return ['Alexander McCall Smith', 'Irvine Welsh'];
  if (kind === '5') return ['Alexander McCall Smith','Irvine Welsh','John Gibson Lockhart','Walter Scott','Robert Louis Stevenson'];
  if (kind === '20') return ALL_AUTHOR_NAMES.slice(0, 20);
  if (kind === '50') return ALL_AUTHOR_NAMES.slice(0, 50);
  return [];
}
function renderAuthorChips() {
  const el = document.getElementById('author-chips');
  el.innerHTML = '';
  selectedAuthors.forEach(name => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.innerHTML = `${name} <span class="chip-x" data-name="${name}">&#x2715;</span>`;
    chip.querySelector('.chip-x').addEventListener('click', (e) => {
      e.stopPropagation();
      setSelectedAuthors(selectedAuthors.filter(n => n !== name));
    });
    el.appendChild(chip);
  });
}
function renderFocusChip() {
  const host = document.getElementById('focus-chip');
  if (!focusedAuthor) {
    host.innerHTML = `<span class="chip-empty">None focused yet</span>`;
    return;
  }
  host.innerHTML = `<span class="chip focus">${focusedAuthor} <span class="chip-x" id="focus-clear">&#x2715;</span></span>`;
  document.getElementById('focus-clear').addEventListener('click', () => { focusedAuthor = null; renderFocusChip(); renderActive(); });
}
function setSelectedAuthors(names) {
  selectedAuthors = [...new Set(names)];
  if (focusedAuthor && !selectedAuthors.includes(focusedAuthor)) focusedAuthor = null;
  renderAuthorChips();
  renderFocusChip();
  renderActive();
}
function toggleFocus(name) {
  focusedAuthor = (focusedAuthor === name) ? null : name;
  renderFocusChip();
  renderActive();
}

document.querySelectorAll('#author-presets .preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#author-presets .preset-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    setSelectedAuthors(presetAuthors(btn.dataset.preset));
  });
});
document.getElementById('btn-clear-authors').addEventListener('click', () => {
  document.querySelectorAll('#author-presets .preset-btn').forEach(b => b.classList.remove('active'));
  setSelectedAuthors([]);
});
const authorSearch = document.getElementById('author-search');
const authorSuggestions = document.getElementById('author-suggestions');
authorSearch.addEventListener('input', () => {
  const term = authorSearch.value.trim().toLowerCase();
  if (!term) { authorSuggestions.style.display = 'none'; return; }
  const matches = ALL_AUTHOR_NAMES.filter(a => a.toLowerCase().includes(term) && !selectedAuthors.includes(a)).slice(0, 15);
  authorSuggestions.innerHTML = matches.map(a => `<div data-name="${a}">${a}</div>`).join('');
  authorSuggestions.style.display = matches.length ? 'block' : 'none';
});
authorSuggestions.addEventListener('click', (e) => {
  const name = e.target.closest('div')?.dataset.name;
  if (name) {
    document.querySelectorAll('#author-presets .preset-btn').forEach(b => b.classList.remove('active'));
    setSelectedAuthors([...selectedAuthors, name]);
    authorSearch.value = ''; authorSuggestions.style.display = 'none';
  }
});

/* ---- nav ---- */
const pickerEl = document.getElementById('viz-picker-list');
const dirTabs = document.querySelectorAll('.dir-tab');
function renderPicker() {
  let html = '';
  directions[currentDir].forEach(v => {
    const activeClass = v.id === currentViz ? ' active' : '';
    html += `<button class="viz-option${activeClass}" data-viz="${v.id}">${v.name}<span class="role">${v.role}</span></button>`;
  });
  pickerEl.innerHTML = html;
  pickerEl.querySelectorAll('.viz-option').forEach(btn => btn.addEventListener('click', () => selectViz(btn.dataset.viz)));
}
function selectViz(vizId) {
  currentViz = vizId;
  document.querySelectorAll('.viz-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + vizId).classList.add('active');
  const meta = directions[currentDir].find(v => v.id === vizId);
  if (meta) document.getElementById('active-name').textContent = meta.name;
  renderPicker();
  renderActive();
}
function selectDir(dirId) {
  currentDir = dirId;
  dirTabs.forEach(t => t.classList.toggle('active', t.dataset.dir === dirId));
  selectViz(directions[dirId][0].id);
}
dirTabs.forEach(t => t.addEventListener('click', () => selectDir(t.dataset.dir)));

function updateExtraControls() {
  const el = document.getElementById('extra-controls');
  if (currentViz === 'network' || currentViz === 'linear') {
    const val = currentViz === 'network' ? networkThreshold : linearThreshold;
    el.style.display = 'flex';
    el.innerHTML = `<label>Min co-occurrence weight: <input type="range" id="threshold-slider" min="1" max="10" value="${val}" step="1"> <span id="threshold-val">${val}</span></label>`;
    document.getElementById('threshold-slider').addEventListener('input', function () {
      const v = +this.value;
      if (currentViz === 'network') { networkThreshold = v; } else { linearThreshold = v; }
      document.getElementById('threshold-val').textContent = v;
      if (currentViz === 'network') renderNetwork(); else renderLinear();
    });
  } else {
    el.style.display = 'none';
    el.innerHTML = '';
  }
}

function renderActive() {
  updateExtraControls();
  clearDetail();
  if (currentViz === 'radar') renderRadar();
  else if (currentViz === 'barcode') renderBarcode();
  else if (currentViz === 'small_multiples') renderSmallMultiples();
  else if (currentViz === 'network') renderNetwork();
  else if (currentViz === 'linear') renderLinear();
  else if (currentViz === 'metro') renderMetro();
}

/* ---- radar ---- */
function renderRadar() {
  const chartEl = document.getElementById('radar-chart');
  chartEl.innerHTML = '';
  const legend = document.getElementById('radar-legend');
  legend.innerHTML = '';
  const names = selectedAuthors.filter(n => radarByName[n]);
  setStatus(`Showing ${names.length} author${names.length===1?'':'s'} of 408` + (focusedAuthor ? ` · focused: ${focusedAuthor}` : ''));

  const W=640, H=640, cx=W/2, cy=H/2, R=240;
  const angleStep = (2*Math.PI)/SECTORS.length;
  const angle = i => i*angleStep - Math.PI/2;
  const svg = d3.select(chartEl).append('svg').attr('width', W).attr('height', H);
  const g = svg.append('g').attr('transform', `translate(${cx},${cy})`);

  const maxVal = names.length ? Math.max(...names.map(name => Math.max(...SECTORS.map(s => radarByName[name].sector_pct[s])))) : 0.1;
  [1,2,3,4,5].forEach(l => {
    g.append('circle').attr('r', R*l/5).attr('fill','none').attr('stroke','#D0D8E8').attr('stroke-width',0.8);
    g.append('text').attr('x',4).attr('y',-R*l/5+3).attr('font-size','9px').attr('fill','#AAA').text(Math.round(maxVal*l/5*100)+'%');
  });
  SECTORS.forEach((s,i) => {
    const a = angle(i);
    g.append('line').attr('x1',0).attr('y1',0).attr('x2',R*Math.cos(a)).attr('y2',R*Math.sin(a)).attr('stroke','#C0C8D8').attr('stroke-width',0.8);
    const lx=(R+30)*Math.cos(a), ly=(R+30)*Math.sin(a);
    g.append('text').attr('x',lx).attr('y',ly).attr('text-anchor','middle').attr('dominant-baseline','central').attr('font-size','9px').attr('fill','#333').attr('font-weight','600').text(s);
  });

  const line = d3.lineRadial().radius(d => Math.max(d,0)/maxVal*R).angle((d,i) => i*angleStep).curve(d3.curveLinearClosed);
  const hasFocus = !!focusedAuthor;
  const baseOpacity = names.length>30?0.35:names.length>10?0.6:0.85;
  const baseFillOpacity = names.length>30?0.02:names.length>10?0.05:0.08;

  names.forEach((name, idx) => {
    const rec = radarByName[name];
    const vals = SECTORS.map(s => rec.sector_pct[s]);
    const color = colorForAuthor(name, idx);
    const isFocused = focusedAuthor === name;
    const strokeOpacity = hasFocus ? (isFocused?1:0.15) : baseOpacity;
    const fillOpacity = hasFocus ? (isFocused?baseFillOpacity*3:baseFillOpacity*0.3) : baseFillOpacity;

    g.append('path').datum(vals).attr('d', line).attr('fill', color).attr('fill-opacity', fillOpacity).attr('stroke','none');
    g.append('path').datum(vals).attr('d', line).attr('fill','none')
      .attr('stroke', color).attr('stroke-width', isFocused?3.2:1.8).attr('stroke-opacity', strokeOpacity)
      .attr('cursor','pointer')
      .on('click', () => toggleFocus(name))
      .on('mouseover', (ev) => { showTooltip(`<strong style="color:${color}">${name}</strong><br>${rec.total_mentions} mentions &middot; ${rec.works} works<br>Dominant: ${rec.dominant_sector} (${(rec.dominant_pct*100).toFixed(1)}%)`, ev); showDetailForAuthor(name); })
      .on('mousemove', moveTooltip)
      .on('mouseout', hideTooltip);

    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `<span class="legend-dot" style="background:${color}"></span><span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${name}</span><span class="legend-remove" data-name="${name}">&#x2715;</span>`;
    item.addEventListener('click', () => toggleFocus(name));
    item.querySelector('.legend-remove').addEventListener('click', (e) => { e.stopPropagation(); setSelectedAuthors(selectedAuthors.filter(n => n !== name)); });
    legend.appendChild(item);
  });
}

/* ---- barcode ---- */
function renderBarcode() {
  const container = document.getElementById('barcode-rows');
  container.innerHTML = '';
  const names = selectedAuthors.filter(n => barcodeByName[n]);
  setStatus(`Showing ${names.length} author row(s) of 408` + (focusedAuthor ? ` · focused: ${focusedAuthor}` : ''));
  names.forEach(name => container.appendChild(buildBarcodeRow(name)));
}
function buildBarcodeRow(name) {
  const rec = barcodeByName[name];
  const row = document.createElement('div');
  row.className = 'author-row';
  if (focusedAuthor) row.classList.add(focusedAuthor === name ? 'focused' : 'dimmed');
  row.addEventListener('click', () => toggleFocus(name));
  const header = document.createElement('div');
  header.className = 'author-header';
  header.innerHTML = `<span class="author-label">${name}</span><span class="author-meta">${rec.total_mentions} total mentions &middot; showing top ${rec.places.length}</span>`;
  row.appendChild(header);
  const bars = document.createElement('div');
  bars.className = 'bars';
  rec.places.forEach(p => {
    const wrap = document.createElement('div'); wrap.className = 'bar-wrap';
    const bar = document.createElement('div'); bar.className = 'bar';
    bar.style.height = Math.max(p.pct_of_top15*100, 2) + '%';
    bar.style.background = sectorColors[p.sector] || '#999';
    bar.addEventListener('mouseover', (ev) => { showTooltip(`<strong>${p.place}</strong><br><span style="color:${sectorColors[p.sector]||'#999'}">&#9679; ${p.sector}</span><br>${p.abs} mentions (${(p.pct_of_top15*100).toFixed(1)}% of top 15)`, ev); showDetailForPlace(p.place, [name]); });
    bar.addEventListener('mousemove', moveTooltip);
    bar.addEventListener('mouseout', hideTooltip);
    const label = document.createElement('div'); label.className = 'bar-label'; label.textContent = p.place;
    wrap.appendChild(bar); wrap.appendChild(label); bars.appendChild(wrap);
  });
  row.appendChild(bars);
  return row;
}

/* ---- small multiples ---- */
function renderSmallMultiples() {
  const grid = document.getElementById('sm-grid');
  grid.innerHTML = '';
  smMaps.forEach(m => m.remove());
  smMaps = [];
  const names = selectedAuthors.filter(n => smByName[n]);
  setStatus(`${names.length} live Leaflet map instance(s)` + (focusedAuthor ? ` · focused: ${focusedAuthor}` : ''));
  names.forEach(name => smMaps.push(buildSmPanel(smByName[name])));
}
function buildSmPanel(rec) {
  const panel = document.createElement('div');
  panel.className = 'sm-panel';
  if (focusedAuthor) panel.classList.add(focusedAuthor === rec.author ? 'focused' : 'dimmed');
  panel.addEventListener('click', () => toggleFocus(rec.author));
  const title = document.createElement('div'); title.className = 'sm-panel-title'; title.textContent = rec.author;
  panel.appendChild(title);
  const stats = document.createElement('div'); stats.className = 'sm-panel-stats';
  stats.textContent = `${rec.places.length} places · ${rec.total_mentions} mentions`;
  panel.appendChild(stats);
  const mapWrap = document.createElement('div'); mapWrap.className = 'sm-map-wrap';
  const id = 'sm-map-' + Math.random().toString(36).slice(2);
  mapWrap.id = id;
  panel.appendChild(mapWrap);
  document.getElementById('sm-grid').appendChild(panel);

  const map = L.map(id, { center: [55.945, -3.192], zoom: 12, zoomControl: false, attributionControl: false });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { subdomains: 'abcd', maxZoom: 18 }).addTo(map);
  const maxCount = Math.max(...rec.places.map(p => p.mentions));
  rec.places.forEach(p => {
    const r = Math.max(Math.log1p(p.mentions/maxCount*100)*3, 3);
    L.circleMarker([p.lat, p.lon], { radius: r, fillColor: '#B85042', color: 'white', weight: 1, fillOpacity: 0.75 })
      .bindPopup(`<strong>${p.place}</strong><br>${p.mentions} mentions`, { closeButton: false })
      .on('mouseover', function () { this.openPopup(); showDetailForPlace(p.place, [rec.author]); })
      .on('mouseout', function () { this.closePopup(); })
      .addTo(map);
  });
  return map;
}

/* ---- network ---- */
function renderNetwork() {
  const chart = document.getElementById('network-chart');
  chart.innerHTML = '';
  const {nodes, edges} = buildGraph(selectedAuthors);
  const activeEdges = edges.filter(e => e.weight >= networkThreshold);
  const activePlaceNames = new Set(activeEdges.flatMap(e => [e.source, e.target]));
  const activeNodes = nodes.filter(n => activePlaceNames.has(n.place)).map(n => ({...n}));
  const focusSet = focusPlacesFor(focusedAuthor);

  setStatus(`${selectedAuthors.length} author(s) selected · ${activeNodes.length} places · ${activeEdges.length} co-occurrence pairs (of ${edges.length} at weight >= 1)` + (focusedAuthor ? ` · highlighting ${focusedAuthor}'s places` : ''));

  const W=760, H=560;
  const svg = d3.select(chart).append('svg').attr('width', W).attr('height', H).style('background','#F4F6FB').style('border-radius','12px');
  const g = svg.append('g');
  svg.call(d3.zoom().scaleExtent([0.3,3]).on('zoom', e => g.attr('transform', e.transform)));
  if (networkSim) networkSim.stop();
  if (activeNodes.length === 0) return;

  const simEdges = activeEdges.map(e => ({...e}));
  const maxWeight = Math.max(...simEdges.map(e => e.weight), 1);
  networkSim = d3.forceSimulation(activeNodes)
    .force('link', d3.forceLink(simEdges).id(d => d.place).distance(d => 260/d.weight*6).strength(0.6))
    .force('charge', d3.forceManyBody().strength(-350))
    .force('center', d3.forceCenter(W/2, H/2))
    .force('collision', d3.forceCollide(d => nodeRadius(d.mentions)+14));

  const link = g.append('g').selectAll('line').data(simEdges).join('line')
    .attr('stroke', d => { const f = focusSet.has(d.source.place||d.source) || focusSet.has(d.target.place||d.target); return focusedAuthor ? (f?'#C9A227':'#A26769') : '#A26769'; })
    .attr('stroke-opacity', d => { const f = focusSet.has(d.source.place||d.source) || focusSet.has(d.target.place||d.target); return focusedAuthor ? (f?0.75:0.12) : 0.45; })
    .attr('stroke-width', d => (d.weight/maxWeight)**2*12);

  const node = g.append('g').selectAll('circle').data(activeNodes).join('circle')
    .attr('r', d => nodeRadius(d.mentions))
    .attr('fill', d => focusedAuthor ? (focusSet.has(d.place)?'#C9A227':'#21295C') : '#21295C')
    .attr('stroke','white').attr('stroke-width',1.5)
    .attr('opacity', d => focusedAuthor ? (focusSet.has(d.place)?1:0.3) : 0.9)
    .attr('cursor','pointer')
    .call(dragBehavior(networkSim))
    .on('mouseover', function (ev,d) {
      d3.select(this).attr('fill','#B85042');
      const connected = simEdges.filter(e => (e.source.place||e.source)===d.place || (e.target.place||e.target)===d.place)
        .sort((a,b) => b.weight-a.weight).slice(0,5)
        .map(e => { const sp=e.source.place||e.source, tp=e.target.place||e.target; return {place: sp===d.place?tp:sp, weight:e.weight}; });
      showTooltip(`<div style="font-weight:bold;color:#21295C">${d.place}</div><div style="color:#888;font-size:11px;margin-bottom:6px">${d.mentions} mentions in current selection</div>` +
        connected.map(c => `<div style="display:flex;justify-content:space-between;gap:16px"><span>${c.place}</span><span style="color:#21295C;font-weight:bold">${c.weight}</span></div>`).join(''), ev);
      showDetailForPlace(d.place, selectedAuthors);
    })
    .on('mousemove', moveTooltip)
    .on('mouseout', function (ev,d) { d3.select(this).attr('fill', focusedAuthor ? (focusSet.has(d.place)?'#C9A227':'#21295C') : '#21295C'); hideTooltip(); });

  const label = g.append('g').selectAll('text').data(activeNodes).join('text')
    .attr('text-anchor','middle').attr('font-size','10px')
    .attr('fill', d => focusedAuthor ? (focusSet.has(d.place)?'#21295C':'#AAA') : '#333')
    .attr('font-weight','500').attr('pointer-events','none').text(d => d.place);

  networkSim.on('tick', () => {
    link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);
    node.attr('cx',d=>d.x).attr('cy',d=>d.y);
    label.attr('x',d=>d.x).attr('y',d=>d.y+nodeRadius(d.mentions)+12);
  });
}

/* ---- linear ---- */
function renderLinear() {
  const scrollHost = document.getElementById('linear-chart');
  scrollHost.innerHTML = '';
  const {nodes, edges} = buildGraph(selectedAuthors);
  const activeEdges = edges.filter(e => e.weight >= linearThreshold);
  const activePlaceNames = new Set(activeEdges.flatMap(e => [e.source, e.target]));
  let activeNodes = nodes.filter(n => activePlaceNames.has(n.place)).sort((a,b) => b.mentions-a.mentions);
  const n = activeNodes.length;
  const focusSet = focusPlacesFor(focusedAuthor);

  setStatus(`${selectedAuthors.length} author(s) selected · ${n} places · ${activeEdges.length} connections (of ${edges.length} at weight >= 1)` + (focusedAuthor ? ` · highlighting ${focusedAuthor}'s places` : ''));
  if (n === 0) return;

  const marginLeft=60, marginRight=60, nodeSpacing=46, axisY=380, H=500;
  const W = Math.max(1100, marginLeft+marginRight+(n-1)*nodeSpacing);
  const xScale = d3.scalePoint().domain(activeNodes.map(d => d.place)).range([marginLeft, W-marginRight]).padding(0.5);
  const maxWeight = Math.max(...activeEdges.map(e => e.weight), 1);

  const svg = d3.select(scrollHost).append('svg').attr('width', W).attr('height', H).style('background','#F4F6FB').style('border-radius','12px');
  svg.append('line').attr('x1',marginLeft).attr('y1',axisY).attr('x2',W-marginRight).attr('y2',axisY).attr('stroke','#C0C8D8').attr('stroke-width',1.5);

  activeEdges.forEach(e => {
    const x1 = xScale(e.source), x2 = xScale(e.target);
    if (x1===undefined || x2===undefined) return;
    const midX=(x1+x2)/2, dist=Math.abs(x2-x1), arcH=dist*0.42;
    const lw = (e.weight/maxWeight)**1.5*6;
    const isFocusEdge = focusSet.has(e.source) || focusSet.has(e.target);
    const alpha = focusedAuthor ? (isFocusEdge?0.8:0.1) : (0.3+(e.weight/maxWeight)*0.5);
    const strokeColor = (focusedAuthor && isFocusEdge) ? '#C9A227' : '#21295C';
    svg.append('path').attr('d', `M ${x1} ${axisY} Q ${midX} ${axisY-arcH} ${x2} ${axisY}`)
      .attr('fill','none').attr('stroke', strokeColor).attr('stroke-width', lw).attr('stroke-opacity', alpha).attr('cursor','pointer')
      .on('mouseover', function (ev) { d3.select(this).attr('stroke','#B85042').attr('stroke-opacity',0.9); showTooltip(`<div style="font-weight:bold;color:#21295C">${e.source} &harr; ${e.target}</div><div style="color:#888">Weight: <strong style="color:#21295C">${e.weight}</strong></div>`, ev); })
      .on('mousemove', moveTooltip)
      .on('mouseout', function () { d3.select(this).attr('stroke', strokeColor).attr('stroke-opacity', alpha); hideTooltip(); });
  });

  activeNodes.forEach(d => {
    const x = xScale(d.place), r = Math.log1p(d.mentions)*2.2;
    const isFocusNode = focusSet.has(d.place);
    const fill = focusedAuthor ? (isFocusNode?'#C9A227':'#B85042') : '#B85042';
    const opacity = focusedAuthor ? (isFocusNode?1:0.3) : 1;
    svg.append('circle').attr('cx',x).attr('cy',axisY).attr('r',r).attr('fill',fill).attr('opacity',opacity).attr('stroke','white').attr('stroke-width',1.5).attr('cursor','pointer')
      .on('mouseover', function (ev) { d3.select(this).attr('fill','#21295C'); showTooltip(`<div style="font-weight:bold;color:#21295C">${d.place}</div><div style="color:#888">${d.mentions} mentions</div>`, ev); showDetailForPlace(d.place, selectedAuthors); })
      .on('mousemove', moveTooltip)
      .on('mouseout', function () { d3.select(this).attr('fill', fill); hideTooltip(); });
    svg.append('text').attr('x',x).attr('y',axisY+r+14).attr('text-anchor','end')
      .attr('transform', `rotate(-45, ${x}, ${axisY+r+14})`).attr('font-size','10px')
      .attr('fill', focusedAuthor ? (isFocusNode?'#21295C':'#AAA') : '#444').text(d.place);
  });
}

/* ---- metro (precomputed snapshot swap, not live) ---- */
function renderMetro() {
  const iframe = document.getElementById('metro-iframe');
  const note = document.getElementById('metro-note');
  const n = selectedAuthors.length;
  const useSnapshot20 = n > 10;
  const src = useSnapshot20 ? '../../scale_exploration/d3/metro_scale_explore_20authors.html' : '../../dir_2/metro/d3/metro.html';
  if (iframe.getAttribute('data-src') !== src) {
    iframe.src = src;
    iframe.setAttribute('data-src', src);
  }
  note.textContent = useSnapshot20
    ? `${n} authors selected — metro lines cannot be recomputed live (community detection runs offline), showing the closest precomputed snapshot: the 20-author configuration.`
    : `${n} author(s) selected — showing the canonical 5-author metro map (closest precomputed snapshot; not live-linked to the author selector or the focus highlight).`;
  setStatus('Metro map: precomputed snapshot, independent of the shared author selector above.');
}

/* ---- bootstrap ---- */
renderPicker();
renderFocusChip();
setSelectedAuthors(presetAuthors('5'));
</script>

</body>
</html>
"""


def main():
    radar = json.loads((SCALE_DATA / "all_authors_radar.json").read_text())
    barcode = json.loads((SCALE_DATA / "all_authors_barcode.json").read_text())
    small_multiples = json.loads((SCALE_DATA / "all_authors_small_multiples.json").read_text())
    network = json.loads((SCALE_DATA / "all_authors_network.json").read_text())
    sentences = json.loads((COMBINED_DATA / "all_authors_sentences.json").read_text())

    html = TEMPLATE
    html = html.replace("/*__RADAR_JSON__*/", json.dumps(radar, ensure_ascii=False))
    html = html.replace("/*__BARCODE_JSON__*/", json.dumps(barcode, ensure_ascii=False))
    html = html.replace("/*__SM_JSON__*/", json.dumps(small_multiples, ensure_ascii=False))
    html = html.replace("/*__NETWORK_JSON__*/", json.dumps(network, ensure_ascii=False))
    html = html.replace("/*__SENTENCES_JSON__*/", json.dumps(sentences, ensure_ascii=False))

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(html)
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
