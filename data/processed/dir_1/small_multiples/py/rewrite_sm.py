html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Author Spatial Fingerprints — Small Multiples</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: "Helvetica Neue", Arial, sans-serif;
    background: #F8F9FC;
    padding: 40px;
  }
  h1 { font-size: 20px; color: #21295C; margin-bottom: 6px; text-align: center; }
  .subtitle { font-size: 13px; color: #888; margin-bottom: 30px; text-align: center; }
  .grid {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    justify-content: center;
    max-width: 1400px;
    margin: 0 auto;
  }
  .panel {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    width: 420px;
  }
  .panel-title { font-size: 14px; font-weight: bold; margin-bottom: 4px; text-align: center; }
  .zoom-hint { font-size: 10px; color: #AAA; text-align: center; margin-bottom: 8px; }
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
    min-width: 160px;
  }
  .tooltip .place { font-weight: bold; font-size: 13px; margin-bottom: 3px; }
</style>
</head>
<body>
<h1>Author Spatial Fingerprints — Small Multiples</h1>
<div class="subtitle">Edinburgh city centre · bubble size = mention frequency · scroll to zoom · drag to pan</div>
<div class="grid" id="grid"></div>
<div class="tooltip" id="tooltip"></div>

<script>
const colors = {
  "Alexander McCall Smith": "#B85042",
  "Irvine Welsh":           "#1C7293",
  "John Gibson Lockhart":   "#2C5F2D",
  "Robert Louis Stevenson": "#7F77DD",
  "Walter Scott":           "#C9A227"
};

const LON_MIN = -3.30, LON_MAX = -3.05;
const LAT_MIN = 55.88, LAT_MAX = 56.01;
const PW = 388, PH = 320, PAD = 20;

const xScale = d3.scaleLinear().domain([LON_MIN, LON_MAX]).range([PAD, PW - PAD]);
const yScale = d3.scaleLinear().domain([LAT_MIN, LAT_MAX]).range([PH - PAD, PAD]);

function drawCityOutline(g) {
  // Firth of Forth
  g.append("path")
    .attr("d", `M ${xScale(-3.30)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(55.985)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.30)} ${yScale(55.985)} Z`)
    .attr("fill", "#D6E8F0").attr("opacity", 0.7);

  g.append("text")
    .attr("x", xScale(-3.18)).attr("y", yScale(55.995))
    .attr("text-anchor", "middle").attr("font-size", "7px")
    .attr("fill", "#7AA8C0").attr("font-style", "italic")
    .text("Firth of Forth");

  // 城市底色
  g.append("path")
    .attr("d", `M ${xScale(-3.30)} ${yScale(55.985)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.05)} ${yScale(55.985)}
                L ${xScale(-3.05)} ${yScale(55.88)}
                L ${xScale(-3.30)} ${yScale(55.88)} Z`)
    .attr("fill", "#F0EDE8").attr("stroke", "#C9C5BC").attr("stroke-width", 0.8);

  // Arthur\'s Seat
  const asx = xScale(-3.162), asy = yScale(55.9441);
  g.append("ellipse")
    .attr("cx", asx).attr("cy", asy)
    .attr("rx", 9).attr("ry", 6)
    .attr("fill", "#C8BFA8").attr("opacity", 0.85);
  g.append("path")
    .attr("d", `M ${asx-9} ${asy} Q ${asx} ${asy-13} ${asx+9} ${asy}`)
    .attr("fill", "#B8AA90").attr("opacity", 0.7);
  g.append("text")
    .attr("x", asx).attr("y", asy + 11)
    .attr("text-anchor", "middle").attr("font-size", "6px")
    .attr("fill", "#7A6E5A").attr("font-weight", "bold")
    .text("Arthur\'s Seat");

  // Pentland Hills
  const phx = xScale(-3.20), phy = yScale(55.893);
  const peaks = [[-22,0],[-14,-8],[0,-12],[12,-8],[22,-5],[32,-9],[42,-6],[52,0]];
  const peakPath = peaks.map((p,i) => `${i===0?"M":"L"} ${phx+p[0]} ${phy+p[1]}`).join(" ") + ` L ${phx+52} ${phy} L ${phx-22} ${phy} Z`;
  g.append("path")
    .attr("d", peakPath)
    .attr("fill", "#B8C4A0").attr("opacity", 0.75);
  g.append("text")
    .attr("x", phx + 15).attr("y", phy + 11)
    .attr("text-anchor", "middle").attr("font-size", "6px")
    .attr("fill", "#6A7A50").attr("font-weight", "bold")
    .text("Pentland Hills");

  // Edinburgh Castle
  const ecx = xScale(-3.2009), ecy = yScale(55.9487);
  g.append("rect").attr("x", ecx-5).attr("y", ecy-7).attr("width", 10).attr("height", 7)
    .attr("fill", "#9A8A7A").attr("opacity", 0.8);
  g.append("rect").attr("x", ecx-6).attr("y", ecy-10).attr("width", 4).attr("height", 4)
    .attr("fill", "#8A7A6A").attr("opacity", 0.8);
  g.append("rect").attr("x", ecx+2).attr("y", ecy-10).attr("width", 4).attr("height", 4)
    .attr("fill", "#8A7A6A").attr("opacity", 0.8);
  g.append("text").attr("x", ecx).attr("y", ecy + 8)
    .attr("text-anchor", "middle").attr("font-size", "5.5px")
    .attr("fill", "#6A5A4A").text("Castle");

  // Holyrood
  const hx = xScale(-3.1735), hy = yScale(55.9498);
  g.append("polygon")
    .attr("points", `${hx},${hy-6} ${hx+5},${hy} ${hx},${hy+6} ${hx-5},${hy}`)
    .attr("fill", "#A89878").attr("opacity", 0.75);
  g.append("text").attr("x", hx).attr("y", hy + 11)
    .attr("text-anchor", "middle").attr("font-size", "5.5px")
    .attr("fill", "#6A5A4A").text("Holyrood");

  // Water of Leith
  g.append("path")
    .attr("d", `M ${xScale(-3.29)} ${yScale(55.930)}
                Q ${xScale(-3.24)} ${yScale(55.935)}
                  ${xScale(-3.21)} ${yScale(55.945)}
                Q ${xScale(-3.18)} ${yScale(55.955)}
                  ${xScale(-3.185)} ${yScale(55.965)}
                Q ${xScale(-3.19)} ${yScale(55.975)}
                  ${xScale(-3.172)} ${yScale(55.980)}`)
    .attr("fill", "none").attr("stroke", "#A8C8D8")
    .attr("stroke-width", 1.5).attr("opacity", 0.6);

  // 区域标注
  const labels = [
    { name: "Old Town",    lat: 55.9490, lon: -3.192 },
    { name: "New Town",    lat: 55.957,  lon: -3.200 },
    { name: "Leith",       lat: 55.976,  lon: -3.172 },
    { name: "Morningside", lat: 55.927,  lon: -3.215 },
    { name: "Stockbridge", lat: 55.958,  lon: -3.212 },
  ];
  labels.forEach(lm => {
    g.append("text")
      .attr("x", xScale(lm.lon)).attr("y", yScale(lm.lat))
      .attr("text-anchor", "middle").attr("font-size", "6px")
      .attr("fill", "#AAA8A0").attr("opacity", 0.8)
      .text(lm.name);
  });
}

const data = {"Alexander McCall Smith":[{"place":"Scotland Street","lat":55.9599,"lon":-3.1951,"mention_count":482},{"place":"Dundas Street","lat":55.9576,"lon":-3.1995,"mention_count":244},{"place":"Moray Place","lat":55.9541541,"lon":-3.2090472,"mention_count":240},{"place":"Drummond Place","lat":55.9582,"lon":-3.195,"mention_count":190},{"place":"Cumberland Bar","lat":55.9589954,"lon":-3.1970753,"mention_count":160},{"place":"Queen Street","lat":55.9546,"lon":-3.2002,"mention_count":140},{"place":"India Street","lat":55.9559,"lon":-3.2059,"mention_count":136},{"place":"New Town","lat":55.9583198,"lon":-3.1992422,"mention_count":128},{"place":"Princes Street","lat":55.9526,"lon":-3.193,"mention_count":116},{"place":"Bruntsfield","lat":55.9366176,"lon":-3.2073772,"mention_count":106},{"place":"The Meadows","lat":55.9453058,"lon":-3.1909968,"mention_count":92},{"place":"Leith","lat":55.9757865,"lon":-3.1680197,"mention_count":88},{"place":"Morningside","lat":55.9274145,"lon":-3.2106492,"mention_count":86},{"place":"Stockbridge","lat":55.957963,"lon":-3.2094115,"mention_count":84},{"place":"Heriot Row","lat":55.9553,"lon":-3.2023,"mention_count":76},{"place":"Howe Street","lat":55.9564,"lon":-3.2023,"mention_count":70},{"place":"Clarence Street","lat":55.9592,"lon":-3.2059,"mention_count":70},{"place":"Jenners","lat":55.9526388,"lon":-3.1941058,"mention_count":60},{"place":"Braid Hills Hotel","lat":55.916927,"lon":-3.212583,"mention_count":58}],"Irvine Welsh":[{"place":"Leith","lat":55.9757865,"lon":-3.1680197,"mention_count":650},{"place":"Southside","lat":55.9385275,"lon":-3.1736702,"mention_count":62},{"place":"Tollcross","lat":55.9444904,"lon":-3.2035205,"mention_count":60},{"place":"Leith Walk","lat":55.9618,"lon":-3.1804,"mention_count":56},{"place":"Wester Hailes","lat":55.9138214,"lon":-3.2803841,"mention_count":44},{"place":"Niddrie","lat":55.9313817,"lon":-3.1221785,"mention_count":40},{"place":"West End","lat":55.9528781,"lon":-3.2107041,"mention_count":36},{"place":"Princes Street","lat":55.9526,"lon":-3.193,"mention_count":32},{"place":"Lochend","lat":55.9621503,"lon":-3.157605,"mention_count":32},{"place":"Waverley Station","lat":55.951727,"lon":-3.191506,"mention_count":32},{"place":"Montgomery Street","lat":55.9594,"lon":-3.1774,"mention_count":30},{"place":"Pilrig","lat":55.9680589,"lon":-3.1817222,"mention_count":30},{"place":"Gorgie","lat":55.93574,"lon":-3.2414663,"mention_count":24},{"place":"Lothian Road","lat":55.9476,"lon":-3.2062,"mention_count":22},{"place":"Pilton","lat":55.9709468,"lon":-3.2462305,"mention_count":22},{"place":"Ocean Drive","lat":55.9803,"lon":-3.1746,"mention_count":22},{"place":"The Meadows","lat":55.9453058,"lon":-3.1909968,"mention_count":18}],"John Gibson Lockhart":[{"place":"Canongate","lat":55.9523547,"lon":-3.1761031,"mention_count":108},{"place":"Castle Street","lat":55.9521,"lon":-3.2033,"mention_count":98},{"place":"Leith","lat":55.9757865,"lon":-3.1680197,"mention_count":48},{"place":"Lasswade","lat":55.88295,"lon":-3.118962,"mention_count":40},{"place":"Holyrood","lat":55.9498473,"lon":-3.183502,"mention_count":34},{"place":"University of Edinburgh","lat":55.942677,"lon":-3.188891,"mention_count":28},{"place":"Princes Street","lat":55.9526,"lon":-3.193,"mention_count":28},{"place":"Musselburgh","lat":55.9421202,"lon":-3.0538516,"mention_count":22},{"place":"Hanover Street","lat":55.9535,"lon":-3.1973,"mention_count":22},{"place":"Old Town","lat":55.9471293,"lon":-3.2002511,"mention_count":20},{"place":"Arthur\'s Seat","lat":55.9441043,"lon":-3.1618477,"mention_count":18},{"place":"Royal Society of Edinburgh","lat":55.953386,"lon":-3.196522,"mention_count":18},{"place":"St Giles","lat":55.9493396,"lon":-3.1905294,"mention_count":18},{"place":"Calton Hill","lat":55.9556726,"lon":-3.1824089,"mention_count":16},{"place":"Portobello","lat":55.9528635,"lon":-3.1145573,"mention_count":16},{"place":"High Street","lat":55.9501,"lon":-3.1882,"mention_count":16},{"place":"New Town","lat":55.9583198,"lon":-3.1992422,"mention_count":16}],"Robert Louis Stevenson":[{"place":"Leith","lat":55.9757865,"lon":-3.1680197,"mention_count":56},{"place":"Princes Street","lat":55.9526,"lon":-3.193,"mention_count":46},{"place":"Cramond","lat":55.9705707,"lon":-3.3065489,"mention_count":36},{"place":"Swanston","lat":55.8956657,"lon":-3.2181884,"mention_count":32},{"place":"High Street","lat":55.9501,"lon":-3.1882,"mention_count":32},{"place":"Calton Hill","lat":55.9556726,"lon":-3.1824089,"mention_count":30},{"place":"Arthur\'s Seat","lat":55.9441043,"lon":-3.1618477,"mention_count":28},{"place":"Heriot Row","lat":55.9553,"lon":-3.2023,"mention_count":26},{"place":"Old Town","lat":55.9471293,"lon":-3.2002511,"mention_count":26},{"place":"New Town","lat":55.9583198,"lon":-3.1992422,"mention_count":26},{"place":"Greyfriars","lat":55.9468,"lon":-3.1914,"mention_count":24},{"place":"Swanston Cottage","lat":55.89504,"lon":-3.221463,"mention_count":24},{"place":"Edinburgh Castle","lat":55.94867,"lon":-3.200924,"mention_count":22},{"place":"Silvermills","lat":55.9593,"lon":-3.2041,"mention_count":20},{"place":"Pilrig","lat":55.9680589,"lon":-3.1817222,"mention_count":20},{"place":"St Giles","lat":55.9493396,"lon":-3.1905294,"mention_count":18},{"place":"Randolph Crescent","lat":55.951934,"lon":-3.211707,"mention_count":16}],"Walter Scott":[{"place":"Canongate","lat":55.9523547,"lon":-3.1761031,"mention_count":132},{"place":"Leith","lat":55.9757865,"lon":-3.1680197,"mention_count":104},{"place":"Holyrood","lat":55.9498473,"lon":-3.183502,"mention_count":94},{"place":"Scottish Parliament","lat":55.951976,"lon":-3.175371,"mention_count":68},{"place":"West Port","lat":55.9464,"lon":-3.1999,"mention_count":52},{"place":"Dalkeith","lat":55.8943342,"lon":-3.0713975,"mention_count":52},{"place":"High Street","lat":55.9501,"lon":-3.1882,"mention_count":42},{"place":"Grassmarket","lat":55.9474,"lon":-3.196,"mention_count":36},{"place":"Liberton","lat":55.9130118,"lon":-3.1662543,"mention_count":34},{"place":"Holyrood Park","lat":55.9430696,"lon":-3.1767594,"mention_count":32},{"place":"Arthur\'s Seat","lat":55.9441043,"lon":-3.1618477,"mention_count":30},{"place":"Luckenbooths","lat":55.949755,"lon":-3.191029,"mention_count":26},{"place":"Tolbooth","lat":55.949616,"lon":-3.191541,"mention_count":26},{"place":"Cowgate","lat":55.9487,"lon":-3.1876,"mention_count":24},{"place":"Musselburgh","lat":55.9421202,"lon":-3.0538516,"mention_count":24},{"place":"Pentland","lat":55.882923,"lon":-3.177727,"mention_count":24}]};

const tooltip = document.getElementById("tooltip");
const grid = document.getElementById("grid");

const authorOrder = [
  "Alexander McCall Smith",
  "Irvine Welsh",
  "John Gibson Lockhart",
  "Robert Louis Stevenson",
  "Walter Scott"
];

authorOrder.forEach(author => {
  const allPlaces = data[author];
  const places = allPlaces.filter(d =>
    d.lat >= LAT_MIN && d.lat <= LAT_MAX &&
    d.lon >= LON_MIN && d.lon <= LON_MAX
  );
  const color = colors[author];
  const maxCount = d3.max(allPlaces, d => d.mention_count);

  const panel = document.createElement("div");
  panel.className = "panel";

  const title = document.createElement("div");
  title.className = "panel-title";
  title.style.color = color;
  title.textContent = author;
  panel.appendChild(title);

  const hint = document.createElement("div");
  hint.className = "zoom-hint";
  hint.textContent = "scroll to zoom · drag to pan";
  panel.appendChild(hint);

  const svg = d3.select(panel)
    .append("svg")
    .attr("width", PW)
    .attr("height", PH)
    .style("border-radius", "8px")
    .style("cursor", "grab");

  const zoomG = svg.append("g");

  svg.call(d3.zoom()
    .scaleExtent([1, 10])
    .on("zoom", (event) => {
      zoomG.attr("transform", event.transform);
    }));

  // 底图
  drawCityOutline(zoomG);

  // 气泡
  places.forEach(d => {
    const r = Math.log1p(d.mention_count / maxCount * 100) * 2.8;
    const cx = xScale(d.lon);
    const cy = yScale(d.lat);

    zoomG.append("circle")
      .attr("cx", cx).attr("cy", cy)
      .attr("r", r)
      .attr("fill", color)
      .attr("opacity", 0.72)
      .attr("stroke", "white")
      .attr("stroke-width", 0.8)
      .attr("cursor", "pointer")
      .on("mouseover", function(event) {
        d3.select(this).attr("opacity", 1).attr("r", r + 3);
        tooltip.style.display = "block";
        tooltip.innerHTML = `
          <div class="place" style="color:${color}">${d.place}</div>
          <div style="color:#888">${d.mention_count} mentions</div>`;
      })
      .on("mousemove", function(event) {
        tooltip.style.left = (event.clientX + 14) + "px";
        tooltip.style.top  = (event.clientY - 10) + "px";
      })
      .on("mouseout", function() {
        d3.select(this).attr("opacity", 0.72).attr("r", r);
        tooltip.style.display = "none";
      });
  });

  grid.appendChild(panel);
});
</script>
</body>
</html>'''

with open('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples/d3/small_multiples.html', 'w') as f:
    f.write(html)
print("done")
