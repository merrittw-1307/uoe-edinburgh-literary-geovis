"""
Rebuilds small_multiples.html from data/small_multiples_enriched.json.

Adds: sector-legend filter (shared across all maps), a sample-sentence line
in each popup, and a "compare 2 authors" mode that swaps the 5-panel grid
for two larger side-by-side maps. lat/lon/mention_count are untouched from
the previous version - only sector/books/sentences were added upstream by
generate_dir1_sentences.py.
"""
import json
from pathlib import Path

REPO_ROOT = Path("/Users/wangmingyu/Downloads/UoE/Dissertation")
DATA_PATH = REPO_ROOT / "data/processed/dir_1/small_multiples/data/small_multiples_enriched.json"
OUT_PATH = REPO_ROOT / "data/processed/dir_1/small_multiples/d3/small_multiples.html"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Author Spatial Fingerprints — Small Multiples v2</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: "Helvetica Neue", Arial, sans-serif;
  background: #F4F6FA;
  padding: 28px 36px;
}
h1 { font-size: 20px; color: #21295C; margin-bottom: 4px; }
.subtitle { font-size: 12px; color: #888; margin-bottom: 4px; }
.source { font-size: 10px; color: #BBB; margin-bottom: 20px; font-style: italic; }

.controls {
  display: flex; gap: 12px; align-items: center;
  flex-wrap: wrap; margin-bottom: 14px;
}
.ctrl-label { font-size: 12px; color: #555; }
.btn {
  padding: 4px 12px; border-radius: 14px;
  border: 1.5px solid #C0C8D8; background: white;
  font-size: 11px; cursor: pointer; color: #333; transition: all 0.15s;
}
.btn:hover { background: #E8EAF6; border-color: #21295C; }
.btn.active { background: #21295C; color: white; border-color: #21295C; }
.sync-btn {
  padding: 4px 14px; border-radius: 14px;
  border: 1.5px solid #C9A227; background: #FFF8E7;
  font-size: 11px; cursor: pointer; color: #856404;
}
.sync-btn.on { background: #C9A227; color: white; border-color: #C9A227; }
select.compare-select {
  padding: 4px 10px; border-radius: 14px; border: 1.5px solid #C0C8D8;
  font-size: 11px; color: #333; background: white;
}

.sector-legend { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 18px; }
.sector-tag {
  font-size: 10px; padding: 3px 10px; border-radius: 10px;
  color: white; cursor: pointer; transition: opacity 0.2s; user-select: none;
}
.sector-tag.muted { opacity: 0.25; }

.compare-row { display: none; gap: 10px; align-items: center; margin-bottom: 14px; }
.compare-row.visible { display: flex; }

.grid {
  display: flex; flex-wrap: wrap;
  gap: 18px; justify-content: center;
}
.panel {
  background: white; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  overflow: hidden;
}
.panel-title {
  font-size: 13px; font-weight: bold;
  padding: 10px 14px 6px;
  display: flex; justify-content: space-between; align-items: center;
}
.panel-stats { font-size: 10px; color: #AAA; font-weight: normal; }

/* Leaflet popup override */
.leaflet-popup-content-wrapper {
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
  padding: 0 !important;
}
.leaflet-popup-content { margin: 0 !important; }
.popup-inner { padding: 10px 14px; font-family: "Helvetica Neue", Arial, sans-serif; max-width: 240px; }
.popup-place { font-size: 14px; font-weight: bold; margin-bottom: 3px; }
.popup-count { font-size: 12px; color: #555; margin-bottom: 6px; }
.popup-pct { font-size: 11px; color: #888; }
.popup-quote { font-style: italic; font-size: 11px; color: #444; margin-top: 6px; padding-top: 6px; border-top: 1px solid #EEE; line-height: 1.4; }
.popup-quote .tt-source { font-style: normal; color: #999; display: block; margin-top: 3px; }
.leaflet-popup-tip-container { display: none; }
</style>
</head>
<body>
<h1>Author Spatial Fingerprints — Small Multiples</h1>
<div class="subtitle">Bubble size = mention frequency (log scale) · click any bubble for details · zoom &amp; pan each map independently</div>
<div class="source">Basemap: © CartoDB Positron, © OpenStreetMap contributors</div>

<div class="controls">
  <span class="ctrl-label">Bubble size:</span>
  <button class="btn active" id="btn-log">Log scale</button>
  <button class="btn" id="btn-linear">Linear scale</button>
  <span class="ctrl-label" style="margin-left:8px">Maps:</span>
  <button class="sync-btn" id="btn-sync">🔗 Sync zoom</button>
  <button class="btn" id="btn-reset">Reset all views</button>
  <span class="ctrl-label" style="margin-left:8px">View:</span>
  <button class="btn active" id="btn-view-all">All 5 authors</button>
  <button class="btn" id="btn-view-compare">Compare 2 authors</button>
</div>

<div class="compare-row" id="compareRow">
  <span class="ctrl-label">Compare:</span>
  <select class="compare-select" id="selectA"></select>
  <span class="ctrl-label">vs</span>
  <select class="compare-select" id="selectB"></select>
</div>

<div class="sector-legend" id="sector-legend"></div>
<div class="grid" id="grid"></div>

<script>
const colors = {
  "Alexander McCall Smith": "#B85042",
  "Irvine Welsh":           "#1C7293",
  "John Gibson Lockhart":   "#2C5F2D",
  "Robert Louis Stevenson": "#7F77DD",
  "Walter Scott":           "#C9A227"
};

const sectorColors = {"Forth":"#4A90D9","Leith":"#1C7293","Inverleith":"#2980B9","New Town":"#8E44AD","Almond":"#5D6D7E","Old Town":"#C0392B","Canongate":"#E74C3C","Western Edinburgh":"#7F8C8D","Craigentinny/Duddingston":"#D35400","Portobello/Craigmillar":"#E67E22","South Central":"#27AE60","South West":"#1E8449","Liberton/Gilmerton":"#2ECC71","Pentlands":"#196F3D","Outer Scotland":"#999999"};
const sectorOrder = ["Leith","Inverleith","New Town","Almond","Old Town","Canongate","Craigentinny/Duddingston","Portobello/Craigmillar","South Central","South West","Liberton/Gilmerton","Forth","Western Edinburgh","Pentlands","Outer Scotland"];

const data = /*__DATA_JSON__*/;

const authorOrder = [
  "Alexander McCall Smith","Irvine Welsh","John Gibson Lockhart",
  "Robert Louis Stevenson","Walter Scott"
];

const LAT_MIN=55.85, LAT_MAX=56.02, LON_MIN=-3.35, LON_MAX=-3.05;
const DEFAULT_CENTER = [55.945, -3.192];
const DEFAULT_ZOOM = 12;

let scaleMode = 'log';
let syncMode = false;
let isSyncing = false;
let viewMode = 'all';
let compareA = authorOrder[0];
let compareB = authorOrder[1];

const usedSectors = sectorOrder.filter(s => Object.values(data).some(places => places.some(p => p.sector === s)));
let activeSectors = new Set(usedSectors);

const maps = {};
const markerLayers = {};

function calcRadius(count, maxCount) {
  if (scaleMode === 'log') {
    return Math.max(Math.log1p(count / maxCount * 100) * 3.8, 3);
  } else {
    return Math.max((count / maxCount) * 22, 3);
  }
}

function buildMarkers(author) {
  const places = data[author].filter(d =>
    d.lat >= LAT_MIN && d.lat <= LAT_MAX &&
    d.lon >= LON_MIN && d.lon <= LON_MAX &&
    activeSectors.has(d.sector)
  );
  const color = colors[author];
  const maxCount = Math.max(...data[author].map(d => d.mention_count));
  const totalMentions = data[author].reduce((s, d) => s + d.mention_count, 0);

  const layer = L.layerGroup();

  places.forEach(d => {
    const r = calcRadius(d.mention_count, maxCount);
    const pct = (d.mention_count / totalMentions * 100).toFixed(1);
    const quote = (d.sentences && d.sentences.length)
      ? `<div class="popup-quote">“${d.sentences[0].text}”<span class="tt-source">— ${d.sentences[0].book}</span></div>`
      : '';
    const marker = L.circleMarker([d.lat, d.lon], {
      radius: r,
      fillColor: color,
      color: 'white',
      weight: 1.5,
      fillOpacity: 0.75
    });

    marker.bindPopup(`
      <div class="popup-inner">
        <div class="popup-place" style="color:${color}">${d.place}</div>
        <div class="popup-count">${d.mention_count} mentions</div>
        <div class="popup-pct">${pct}% of ${author.split(' ').pop()}'s total · ${d.sector}</div>
        ${quote}
      </div>`, {
      closeButton: false,
      offset: [0, -r]
    });

    marker.on('mouseover', function() { this.openPopup(); });
    marker.on('mouseout', function() { this.closePopup(); });
    marker.on('click', function() {
      this.openPopup();
      marker.off('mouseout');
      marker.on('mouseout', function(){});
    });

    layer.addLayer(marker);
  });

  return layer;
}

function refreshMarkers() {
  Object.keys(maps).forEach(author => {
    const map = maps[author];
    if (markerLayers[author]) map.removeLayer(markerLayers[author]);
    markerLayers[author] = buildMarkers(author);
    markerLayers[author].addTo(map);
  });
}

function teardownMaps() {
  Object.values(maps).forEach(map => map.remove());
  for (const k in maps) delete maps[k];
  for (const k in markerLayers) delete markerLayers[k];
}

function buildGrid(authorsToShow, panelW, panelH) {
  teardownMaps();
  document.getElementById('grid').innerHTML = '';

  authorsToShow.forEach(author => {
    const places = data[author].filter(d =>
      d.lat >= LAT_MIN && d.lat <= LAT_MAX && d.lon >= LON_MIN && d.lon <= LON_MAX
    );
    const totalMentions = data[author].reduce((s,d) => s+d.mention_count, 0);
    const color = colors[author];

    const panel = document.createElement('div');
    panel.className = 'panel';
    panel.style.width = panelW + 'px';

    const titleDiv = document.createElement('div');
    titleDiv.className = 'panel-title';
    titleDiv.innerHTML = `
      <span style="color:${color}">${author}</span>
      <span class="panel-stats">${places.length} places · ${totalMentions.toLocaleString()} mentions</span>`;
    panel.appendChild(titleDiv);

    const mapWrap = document.createElement('div');
    mapWrap.style.width = panelW + 'px';
    mapWrap.style.height = panelH + 'px';
    const mapId = 'map-' + author.replace(/\s+/g,'-');
    mapWrap.id = mapId;
    panel.appendChild(mapWrap);
    document.getElementById('grid').appendChild(panel);

    const map = L.map(mapId, {
      center: DEFAULT_CENTER,
      zoom: DEFAULT_ZOOM,
      zoomControl: true,
      attributionControl: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd', maxZoom: 18
    }).addTo(map);

    maps[author] = map;

    map.on('moveend zoomend', function() {
      if (!syncMode || isSyncing) return;
      isSyncing = true;
      const center = map.getCenter();
      const zoom = map.getZoom();
      authorsToShow.forEach(a => {
        if (a !== author) maps[a].setView(center, zoom, {animate: false});
      });
      isSyncing = false;
    });
  });

  refreshMarkers();
}

// Sector legend
const legendDiv = document.getElementById('sector-legend');
usedSectors.forEach(s => {
  const tag = document.createElement('div');
  tag.className = 'sector-tag';
  tag.style.background = sectorColors[s] || '#999';
  tag.textContent = s;
  tag.dataset.sector = s;
  tag.addEventListener('click', () => {
    if (activeSectors.has(s)) {
      activeSectors.delete(s);
      tag.classList.add('muted');
    } else {
      activeSectors.add(s);
      tag.classList.remove('muted');
    }
    refreshMarkers();
  });
  legendDiv.appendChild(tag);
});

// Compare selects
const selectA = document.getElementById('selectA');
const selectB = document.getElementById('selectB');
authorOrder.forEach(a => {
  selectA.appendChild(new Option(a, a, a === compareA, a === compareA));
  selectB.appendChild(new Option(a, a, a === compareB, a === compareB));
});
selectA.addEventListener('change', () => { compareA = selectA.value; buildGrid([compareA, compareB], 640, 460); });
selectB.addEventListener('change', () => { compareB = selectB.value; buildGrid([compareA, compareB], 640, 460); });

buildGrid(authorOrder, 420, 310);

// Controls
document.getElementById('btn-log').addEventListener('click', () => {
  scaleMode = 'log';
  document.getElementById('btn-log').classList.add('active');
  document.getElementById('btn-linear').classList.remove('active');
  refreshMarkers();
});
document.getElementById('btn-linear').addEventListener('click', () => {
  scaleMode = 'linear';
  document.getElementById('btn-linear').classList.add('active');
  document.getElementById('btn-log').classList.remove('active');
  refreshMarkers();
});
document.getElementById('btn-sync').addEventListener('click', function() {
  syncMode = !syncMode;
  this.classList.toggle('on', syncMode);
  this.textContent = syncMode ? '🔗 Sync on' : '🔗 Sync zoom';
});
document.getElementById('btn-reset').addEventListener('click', () => {
  Object.keys(maps).forEach(a => maps[a].setView(DEFAULT_CENTER, DEFAULT_ZOOM));
});
document.getElementById('btn-view-all').addEventListener('click', () => {
  viewMode = 'all';
  document.getElementById('btn-view-all').classList.add('active');
  document.getElementById('btn-view-compare').classList.remove('active');
  document.getElementById('compareRow').classList.remove('visible');
  buildGrid(authorOrder, 420, 310);
});
document.getElementById('btn-view-compare').addEventListener('click', () => {
  viewMode = 'compare';
  document.getElementById('btn-view-compare').classList.add('active');
  document.getElementById('btn-view-all').classList.remove('active');
  document.getElementById('compareRow').classList.add('visible');
  buildGrid([compareA, compareB], 640, 460);
});
</script>
</body>
</html>
"""


def main() -> None:
    data = json.loads(DATA_PATH.read_text())
    data_json = json.dumps(data, ensure_ascii=False)
    html = TEMPLATE.replace("/*__DATA_JSON__*/", data_json)
    OUT_PATH.write_text(html)
    print(f"Wrote {OUT_PATH} ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
