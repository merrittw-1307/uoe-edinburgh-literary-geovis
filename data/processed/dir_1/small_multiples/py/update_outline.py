with open('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples/d3/small_multiples.html', 'r') as f:
    content = f.read()

old = """// 简化的爱丁堡轮廓路径（基于真实海岸线近似，Firth of Forth在北侧）
function drawCityOutline(svg) {
  // Firth of Forth 水域（北部）
  svg.append('path')
    .attr('d', `M ${xScale(-3.30)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(55.985)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.30)} ${yScale(55.985)}
                Z`)
    .attr('fill', '#D6E8F0')
    .attr('opacity', 0.7);

  // Firth of Forth 标注
  svg.append('text')
    .attr('x', xScale(-3.18))
    .attr('y', yScale(55.995))
    .attr('text-anchor', 'middle')
    .attr('font-size', '7px')
    .attr('fill', '#7AA8C0')
    .attr('font-style', 'italic')
    .text('Firth of Forth');

  // 城市轮廓（简化）
  svg.append('path')
    .attr('d', `M ${xScale(-3.30)} ${yScale(55.985)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.05)} ${yScale(55.985)}
                L ${xScale(-3.05)} ${yScale(55.88)}
                L ${xScale(-3.30)} ${yScale(55.88)}
                Z`)
    .attr('fill', '#F0EDE8')
    .attr('stroke', '#C9C5BC')
    .attr('stroke-width', 0.8);

  // 几个关键地标标注
  const landmarks = [
    { name: 'Old Town', lat: 55.9490, lon: -3.192 },
    { name: 'New Town', lat: 55.957, lon: -3.200 },
    { name: 'Leith', lat: 55.976, lon: -3.172 },
    { name: "Arthur's Seat", lat: 55.944, lon: -3.162 },
    { name: 'Pentland', lat: 55.895, lon: -3.20 },
  ];
  landmarks.forEach(lm => {
    svg.append('text')
      .attr('x', xScale(lm.lon))
      .attr('y', yScale(lm.lat))
      .attr('text-anchor', 'middle')
      .attr('font-size', '6.5px')
      .attr('fill', '#AAA8A0')
      .text(lm.name);
  });
}"""

new = """function drawCityOutline(svg) {
  // Firth of Forth 水域
  svg.append('path')
    .attr('d', `M ${xScale(-3.30)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(56.01)}
                L ${xScale(-3.05)} ${yScale(55.985)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.30)} ${yScale(55.985)}
                Z`)
    .attr('fill', '#D6E8F0').attr('opacity', 0.7);

  svg.append('text')
    .attr('x', xScale(-3.18)).attr('y', yScale(55.995))
    .attr('text-anchor', 'middle').attr('font-size', '7px')
    .attr('fill', '#7AA8C0').attr('font-style', 'italic')
    .text('Firth of Forth');

  // 城市底色
  svg.append('path')
    .attr('d', `M ${xScale(-3.30)} ${yScale(55.985)}
                Q ${xScale(-3.22)} ${yScale(55.990)}
                  ${xScale(-3.17)} ${yScale(55.982)}
                Q ${xScale(-3.12)} ${yScale(55.975)}
                  ${xScale(-3.05)} ${yScale(55.985)}
                L ${xScale(-3.05)} ${yScale(55.88)}
                L ${xScale(-3.30)} ${yScale(55.88)} Z`)
    .attr('fill', '#F0EDE8').attr('stroke', '#C9C5BC').attr('stroke-width', 0.8);

  // Arthur's Seat — 小山丘轮廓
  const asx = xScale(-3.162), asy = yScale(55.9441);
  svg.append('ellipse')
    .attr('cx', asx).attr('cy', asy)
    .attr('rx', 7).attr('ry', 5)
    .attr('fill', '#C8BFA8').attr('opacity', 0.85);
  svg.append('path')
    .attr('d', `M ${asx-7} ${asy} Q ${asx} ${asy-10} ${asx+7} ${asy}`)
    .attr('fill', '#B8AA90').attr('opacity', 0.7);
  svg.append('text')
    .attr('x', asx).attr('y', asy + 9)
    .attr('text-anchor', 'middle').attr('font-size', '6px')
    .attr('fill', '#7A6E5A').attr('font-weight', 'bold')
    .text("Arthur's Seat");

  // Pentland Hills — 산릉선
  const phx = xScale(-3.20), phy = yScale(55.893);
  const peaks = [[-18,0],[-10,-7],[0,-10],[10,-7],[18,-4],[26,-8],[34,-5],[42,0]];
  const peakPath = peaks.map((p,i) => `${i===0?'M':'L'} ${phx+p[0]} ${phy+p[1]}`).join(' ') + ` L ${phx+42} ${phy} L ${phx-18} ${phy} Z`;
  svg.append('path')
    .attr('d', peakPath)
    .attr('fill', '#B8C4A0').attr('opacity', 0.75);
  svg.append('text')
    .attr('x', phx + 12).attr('y', phy + 10)
    .attr('text-anchor', 'middle').attr('font-size', '6px')
    .attr('fill', '#6A7A50').attr('font-weight', 'bold')
    .text('Pentland Hills');

  // Edinburgh Castle — 小方块符号
  const ecx = xScale(-3.2009), ecy = yScale(55.9487);
  svg.append('rect')
    .attr('x', ecx-4).attr('y', ecy-6)
    .attr('width', 8).attr('height', 6)
    .attr('fill', '#9A8A7A').attr('opacity', 0.8);
  svg.append('rect')
    .attr('x', ecx-5).attr('y', ecy-8)
    .attr('width', 3).attr('height', 3)
    .attr('fill', '#8A7A6A').attr('opacity', 0.8);
  svg.append('rect')
    .attr('x', ecx+2).attr('y', ecy-8)
    .attr('width', 3).attr('height', 3)
    .attr('fill', '#8A7A6A').attr('opacity', 0.8);
  svg.append('text')
    .attr('x', ecx).attr('y', ecy + 6)
    .attr('text-anchor', 'middle').attr('font-size', '5.5px')
    .attr('fill', '#6A5A4A')
    .text('Castle');

  // Holyrood Palace — 小菱形
  const hx = xScale(-3.1735), hy = yScale(55.9498);
  svg.append('polygon')
    .attr('points', `${hx},${hy-5} ${hx+4},${hy} ${hx},${hy+5} ${hx-4},${hy}`)
    .attr('fill', '#A89878').attr('opacity', 0.75);
  svg.append('text')
    .attr('x', hx).attr('y', hy + 9)
    .attr('text-anchor', 'middle').attr('font-size', '5.5px')
    .attr('fill', '#6A5A4A')
    .text('Holyrood');

  // Water of Leith — 구불구불한 선
  svg.append('path')
    .attr('d', `M ${xScale(-3.29)} ${yScale(55.930)}
                Q ${xScale(-3.24)} ${yScale(55.935)}
                  ${xScale(-3.21)} ${yScale(55.945)}
                Q ${xScale(-3.18)} ${yScale(55.955)}
                  ${xScale(-3.185)} ${yScale(55.965)}
                Q ${xScale(-3.19)} ${yScale(55.975)}
                  ${xScale(-3.172)} ${yScale(55.980)}`)
    .attr('fill', 'none')
    .attr('stroke', '#A8C8D8')
    .attr('stroke-width', 1.5)
    .attr('opacity', 0.6);
  svg.append('text')
    .attr('x', xScale(-3.21)).attr('y', yScale(55.960))
    .attr('font-size', '5.5px').attr('fill', '#7AA8C0')
    .attr('font-style', 'italic').attr('transform', `rotate(-25, ${xScale(-3.21)}, ${yScale(55.960)})`)
    .text('Water of Leith');

  // 区域标注
  const labels = [
    { name: 'Old Town', lat: 55.9490, lon: -3.192 },
    { name: 'New Town', lat: 55.957, lon: -3.200 },
    { name: 'Leith', lat: 55.976, lon: -3.172 },
    { name: 'Morningside', lat: 55.927, lon: -3.215 },
    { name: 'Stockbridge', lat: 55.958, lon: -3.212 },
  ];
  labels.forEach(lm => {
    svg.append('text')
      .attr('x', xScale(lm.lon)).attr('y', yScale(lm.lat))
      .attr('text-anchor', 'middle').attr('font-size', '6px')
      .attr('fill', '#AAA8A0').attr('opacity', 0.8)
      .text(lm.name);
  });
}"""

content = content.replace(old, new)
with open('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples/d3/small_multiples.html', 'w') as f:
    f.write(content)
print("done")
