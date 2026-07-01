with open('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples/d3/small_multiples.html', 'r') as f:
    content = f.read()

old_style = """.grid { display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; max-width: 980px; margin: 0 auto; }
  .panel {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    width: 295px;
  }
  .panel-title { font-size: 13px; font-weight: bold; margin-bottom: 10px; text-align: center; }"""

new_style = """.grid { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; max-width: 1400px; margin: 0 auto; }
  .panel {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    width: 420px;
  }
  .panel-title { font-size: 14px; font-weight: bold; margin-bottom: 10px; text-align: center; }
  .zoom-hint { font-size: 10px; color: #AAA; text-align: center; margin-bottom: 6px; }"""

content = content.replace(old_style, new_style)

old_pw = "const PW = 288, PH = 240, PAD = 16;"
new_pw = "const PW = 388, PH = 320, PAD = 20;"
content = content.replace(old_pw, new_pw)

old_panel = """  const panel = document.createElement('div');
  panel.className = 'panel';

  const title = document.createElement('div');
  title.className = 'panel-title';
  title.style.color = color;
  title.textContent = author;
  panel.appendChild(title);

  const svg = d3.select(panel)
    .append('svg')
    .attr('width', PW)
    .attr('height', PH)
    .style('border-radius', '8px');

  // 底图
  drawCityOutline(svg);"""

new_panel = """  const panel = document.createElement('div');
  panel.className = 'panel';

  const title = document.createElement('div');
  title.className = 'panel-title';
  title.style.color = color;
  title.textContent = author;
  panel.appendChild(title);

  const hint = document.createElement('div');
  hint.className = 'zoom-hint';
  hint.textContent = 'scroll to zoom · drag to pan';
  panel.appendChild(hint);

  const svg = d3.select(panel)
    .append('svg')
    .attr('width', PW)
    .attr('height', PH)
    .style('border-radius', '8px')
    .style('cursor', 'grab');

  const zoomG = svg.append('g');

  const zoom = d3.zoom()
    .scaleExtent([1, 8])
    .on('zoom', (event) => {
      zoomG.attr('transform', event.transform);
    });
  svg.call(zoom);

  // 底图画在zoomG里
  const origAppend = svg.append.bind(svg);
  svg.append = (tag) => zoomG.append(tag);"""

content = content.replace(old_panel, new_panel)

old_bubble = """    svg.append('circle')
      .attr('cx', cx).attr('cy', cy)
      .attr('r', r)
      .attr('fill', color)
      .attr('opacity', 0.72)
      .attr('stroke', 'white')
      .attr('stroke-width', 0.8)
      .attr('cursor', 'pointer')"""

new_bubble = """    zoomG.append('circle')
      .attr('cx', cx).attr('cy', cy)
      .attr('r', r)
      .attr('fill', color)
      .attr('opacity', 0.72)
      .attr('stroke', 'white')
      .attr('stroke-width', 0.8)
      .attr('cursor', 'pointer')"""

content = content.replace(old_bubble, new_bubble)

old_restore = "  grid.appendChild(panel);"
new_restore = """  // restore svg.append
  svg.append = origAppend;
  grid.appendChild(panel);"""

content = content.replace(old_restore, new_restore)

with open('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples/d3/small_multiples.html', 'w') as f:
    f.write(content)
print("done")
