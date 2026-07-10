# 项目完整迁移说明文档
## A Visual Trace Map of Edinburgh Place Names in Literature
### MSc Dissertation — Merritt Wang (S2887338)
### University of Edinburgh, School of Informatics, 2025–2026
### 生成时间：2026年7月10日

---

## ⚠️ 阅读本文档的AI助手注意事项

1. **默认用中文回复**，除非Merritt用英文写
2. **不要一味同意**，要客观，遇到不合理的地方要指出
3. **读完整份文档**再回复第一条消息
4. 本项目正在进行中，不要从头开始，要接着做
5. Merritt的偏好：doppio咖啡，抽烟，多个纹身，INFJ-T，来自大连/北京，现居爱丁堡

---

## 1. 项目概述

### 这个项目是什么

MSc Computer Science毕业论文项目，爱丁堡大学信息学院，2026年9月毕业。

**核心论点**：文学文本中的地名应该被可视化为**叙事结构**，而不是地理信息。现有工具把地名标注在地图上，但文学意义来自叙事语境，不是坐标。

**两个研究方向**：
- **方向一（Author Spatial Fingerprints）**：每位作者的地名分布能否形成独特的视觉"指纹"，让用户不需要先验知识就能识别作者？
- **方向二（Narrative Topology Networks）**：地名在文学作品中的共现关系是否揭示出与地理拓扑不同的叙事拓扑？

### 关键人员

| 角色 | 姓名 |
|------|------|
| 学生 | Merritt Wang（王铭宇），S2887338 |
| 导师 | Uta Hinrichs（VisHub联合主任） |
| 第二督导 | Nina Pardal |
| GitHub | merrittw-1307 |
| 论文截止 | 2026年8月21日 |

### 技术栈

- **数据库**：PostgreSQL 16（本地，Mac）
- **数据处理**：Python（pandas, sqlalchemy, shapely, matplotlib, networkx）
- **可视化**：D3.js v7（交互式），Leaflet.js 1.9.4（地图）
- **论文**：LaTeX on Overleaf（infthesis.cls模板）
- **版本控制**：GitHub

---

## 2. GitHub仓库

**地址**：https://github.com/merrittw-1307/uoe-edinburgh-literary-geovis

### 本地目录结构

```
/Users/wangmingyu/Downloads/UoE/Dissertation/
├── data/
│   ├── raw/
│   │   ├── sql/
│   │   │   ├── litlong_original.sql      ← 完整dump（145MB，不push到GitHub）
│   │   │   ├── litlong_schema.sql        ← 只有表结构（已push）
│   │   │   └── directus.sql              ← CMS导出
│   │   ├── csv_snapshot/                 ← 4个CSV快照
│   │   └── geodata/
│   │       ├── neighbourhood_partnership_areas.geojson  ← 官方NP Areas
│   │       └── natural_neighbourhoods.geojson           ← 官方Natural Neighbourhoods
│   └── processed/
│       ├── sectors/
│       │   ├── location_sectors_v2.csv   ← 每个地名的官方sector分配（2135条）
│       │   └── location_sectors.csv      ← v1（废弃）
│       ├── dir_1/
│       │   ├── radar/     {py/, d3/, data/}
│       │   ├── barcode/   {py/, d3/, data/}
│       │   └── small_multiples/ {py/, d3/, data/}
│       └── dir_2/
│           ├── network/   {py/, d3/, data/}
│           ├── linear/    {py/, d3/, data/}
│           └── metro/     {py/, d3/, data/}
├── dissertation/
│   └── main/
│       ├── dissertation.tex   ← 论文主文件（已大量填写）
│       ├── mybibfile.bib      ← 参考文献
│       ├── infthesis.cls
│       ├── msccheck.sty
│       └── eushield.sty
├── ethics/                    ← 伦理审批文件（#446635）
├── proposal/                  ← 项目提案和阅读材料
├── report/
│   ├── presentations/         ← 23Jun_VisHub.pptx
│   └── session_reports/       ← HTML格式的会议记录
└── docs/
    ├── handover.md            ← 上一版交接文档
    └── MSc_projectTimeline.docx
```

---

## 3. 数据库

### 连接信息

```
数据库名：litlong_edinburgh
用户：wangmingyu
端口：5432
PostgreSQL版本：16
```

### 关键数据表

| 表名 | 行数 | 说明 |
|------|------|------|
| api_document | 620 | 文学作品元数据 |
| api_author | 424 | 作者信息 |
| api_document_author | 1,232 | 多对多：作品↔作者 |
| api_location | 2,135 | 地名（text, lat, lon, gazref, ptype） |
| api_locationmention | 50,248 | 核心提及记录（start_word, page_id, sentence_id） |
| api_sentence | 50,248 | 每条提及对应的完整原文句子 |
| api_genre | 29 | 文学类型 |
| api_posmention | 2,085,834 | 词性标注（未使用） |
| **mention_order** | 50,248 | **自定义表**：叙事顺序字段 |

### mention_order表

这是自己建的派生表，字段：
- `id`：外键→api_locationmention
- `document_id`：文档ID
- `location_id`：地名ID
- `word_num`：从start_word提取的整数（"w81489"→81489）
- `mention_order`：在文档内的排名（1=最早）
- `position_pct`：归一化位置（0.0-1.0）

**关键发现**：start_word字段在每个文档内严格单调递增，可以直接推导叙事顺序。

### 重要SQL注意事项

作者名有前后空格，**必须用TRIM**：
```sql
TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author
```

五位测试作者的精确匹配条件：
```sql
WHERE (
    (TRIM(a.forenames) = 'Walter' AND TRIM(a.surname) = 'Scott') OR
    (TRIM(a.forenames) = 'Robert Louis' AND TRIM(a.surname) = 'Stevenson') OR
    (TRIM(a.forenames) = 'Irvine' AND TRIM(a.surname) = 'Welsh') OR
    (TRIM(a.forenames) = 'John Gibson' AND TRIM(a.surname) = 'Lockhart') OR
    (TRIM(a.forenames) = 'Alexander' AND TRIM(a.surname) = 'McCall Smith')
)
```

---

## 4. 五位测试作者

| 作者 | 提及数 | 书数 | 主导sector | 占比 | 颜色 |
|------|--------|------|-----------|------|------|
| Alexander McCall Smith | 7,320 | 17 | New Town | 43.6% | #B85042 |
| Irvine Welsh | 2,634 | 8 | Leith | 44.3% | #1C7293 |
| John Gibson Lockhart | 3,046 | 6 | New Town | 25.9% | #2C5F2D |
| Walter Scott | 2,796 | 12 | Old Town | 32.0% | #C9A227 |
| Robert Louis Stevenson | 1,778 | 16 | Old Town | 20.7% | #7F77DD |

---

## 5. 14个官方Sector划分（核心方法论决策）

### 数据来源

两个官方数据集，均来自City of Edinburgh Council Open Spatial Data Portal（Open Government Licence v3.0）：

1. **Neighbourhood Partnership Areas**（NP Areas）
   - ArcGIS REST API Layer ID: 28
   - URL: `edinburghcouncilmaps.info/arcgis/rest/services/Atlas/Atlas/MapServer/28`
   - 性质：爱丁堡市议会官方行政分区
   - 文件：`data/raw/geodata/neighbourhood_partnership_areas.geojson`

2. **Natural Neighbourhoods**
   - ArcGIS REST API Layer ID: 188
   - URL: `edinburghcouncilmaps.info/arcgis/rest/services/Atlas/Atlas/MapServer/188`
   - 性质：2004年居民咨询创建，2014年公众参与更新的邻里边界
   - 文件：`data/raw/geodata/natural_neighbourhoods.geojson`

### 划分方案

**主框架**：11个NP Areas（去掉City Centre NP）

**City Centre NP细分**：用Natural Neighbourhoods拆分为Old Town、New Town、Canongate三个区域

**论文中的论证**：Old Town和New Town在文学、历史和UNESCO世界遗产上有根本区别，合并会抹除最重要的文学地理区分。

**最终14个sectors**：

| Sector | 数据来源 | 地名数（精确匹配） |
|--------|---------|----------------|
| Old Town | Natural Neighbourhoods | 296 |
| South Central | NP Areas | 255 |
| New Town | Natural Neighbourhoods | 217 |
| Leith | NP Areas | 152 |
| Inverleith | NP Areas | 140 |
| Craigentinny/Duddingston | NP Areas | 73 |
| Pentlands | NP Areas | 66 |
| Canongate | Natural Neighbourhoods | 64 |
| Almond | NP Areas | 64 |
| South West | NP Areas | 44 |
| Western Edinburgh | NP Areas | 43 |
| Portobello/Craigmillar | NP Areas | 38 |
| Liberton/Gilmerton | NP Areas | 36 |
| Forth | NP Areas | 27 |
| Outer Scotland（排除） | — | 232 |

### 分配方法

- **精确匹配**：point-in-polygon（shapely），1480个地名（69%）
- **最近邻分配**：在爱丁堡边界框内但落在多边形缝隙的地名，423个（20%）
- **边界框**：lat 55.82-56.02，lon -3.40 to -2.85
- **Outer Scotland**：232个（11%），不参与sector分析

### 引用格式

> "Copyright City of Edinburgh Council, contains Ordnance Survey data © Crown copyright"

---

## 6. 关键数据发现

### 发现1：作者空间语言高度个性化
五位测试作者中，**零个地名被3位或以上作者共同提及**，仅18个被恰好2位共同提及。→ 每位作者构建了几乎完全私人化的文学爱丁堡。

**设计决策影响**：个别地名不能作为雷达图轴（大多数轴对大多数作者是零），必须用city sectors作为轴。

### 发现2：Sector分布与文学史认知一致
数据驱动的结果与已知文学地理认知完全吻合——这是数据pipeline正确的有力验证。

### 发现3：共现粒度必须用document级别
- Sentence级别：0个共现对（每个句子最多含1个地名）
- Page级别：最多92个地名共现（太粗，hairball）
- **Document级别：403对（weight≥2），选定为合适粒度**

### 发现4：叙事拓扑≠地理拓扑
最强共现对：**Leith & Princes Street（weight=28）**——地理上相距约2.5km，但在28部不同文学作品中共同出现。这是核心论点RQ2的最有力数据证据。

### 发现5：Walter Scott的广域地理范围
Scott的数据包含Forth（lat 56.05）、Haddington（lon -2.80）等远郊地点。在Small Multiples中固定显示范围为爱丁堡核心区（lat 55.85-56.02，lon -3.35 to -3.05）。

---

## 7. 六个可视化HTML——当前状态详细说明

### 文件路径规律

```
data/processed/dir_1/{radar|barcode|small_multiples}/d3/{文件名}.html
data/processed/dir_2/{network|linear|metro}/d3/{文件名}.html
```

所有HTML文件：
- 数据直接内嵌为JavaScript数组（不依赖外部CSV）
- 双击即可在浏览器打开（不需要本地服务器）
- 每次修改前备份旧版本（如radar_v1.html）

---

### 7.1 radar.html（方向一，主要设计）✅ 完成度高

**功能**：
- 14个官方sector轴，D3 lineRadial + curveLinearClosed
- Y轴缩放到数据最大值（0.436），不是1.0
- 悬停任意顶点→显示sector百分比
- 点击任意顶点→右侧详情面板（该sector下的top8地名+top5书目）
- 点击legend→显示/隐藏某位作者
- 双击legend→单独显示某位作者

**数据文件**：`radar/data/radar_data_v2.csv`（14个sector列）

**待改进**：
- 加入api_sentence原文句子hover（最高优先级）

---

### 7.2 barcode.html（方向一，次要设计）✅ 完成度最高

**功能**：
- 每位作者一行竖条，每条=一个地名
- **独立Y轴**（per-author）：每位作者缩放到自己的最大值（解决Welsh/Leith 44%压缩其他作者的问题）
- 界面有黄色警告说明Y轴不可跨行比较
- 按sector排序（北→南），同一sector地名相邻
- 底部颜色条带标注sector（宽度足够时显示文字）
- 三种排序切换：By sector / By frequency / Alphabetical
- 两种scale切换：Percentage / Absolute count
- 地名搜索框（高亮匹配的条形）
- 点击sector图例→筛选/隐藏该sector
- 点击任意条形→右侧详情面板（地名、sector、提及数、书目列表）

**数据文件**：`barcode/data/barcode_data_v2.csv`

**待改进**：
- 加入api_sentence原文句子

---

### 7.3 small_multiples.html（方向一，第三设计）✅ 完成度较高

**功能**：
- 五个并排面板，每个是独立的Leaflet.js地图
- CartoDB Positron底图（需要网络）
- Bubble大小=提及频率（默认log scale，可切换linear）
- 点击/悬停气泡→popup显示地名+提及数+占比
- 同步缩放模式（锁定五个面板到相同视角）
- 重置视图按钮
- 坐标范围固定为爱丁堡核心区（lat 55.85-56.02，lon -3.35 to -3.05）

**使用的是Leaflet CircleMarker**（不是D3 SVG overlay，因为overlay的坐标计算有bug）

**待改进**：
- sector筛选功能
- 原文句子
- 作者对比模式（选择2个作者并排）

---

### 7.4 network.html（方向二，主要设计）✅ 基本完成

**功能**：
- 力导向网络图，D3 forceSimulation
- 节点大小=log1p(total_mentions) * 2.8
- 边宽=(weight/maxWeight)² * 12（平方归一化）
- **Weight threshold slider：范围1-28**（已改为从1开始）
- 悬停节点→显示top5共现地名+权重
- 拖拽节点（D3 drag + fx/fy pinning）
- 缩放平移（D3 zoom）
- 节点标签在节点正下方（y = node.y + radius + 12）

**力模拟参数**：
- forceLink：distance=280/weight*8，strength=0.7
- forceManyBody：-400
- forceCollide：nodeRadius+18
- forceCenter：canvas中心

**待改进**：
- 点击节点→显示详情面板（书名+原文句子）
- scale切换（绝对数/百分比）

---

### 7.5 linear.html（方向二，次要设计）⚠️ 需要改进

**当前功能**：
- 地名沿水平轴排列（按总提及频率排序，左→右）
- 贝塞尔弧线连接共现地名对
- 弧高=水平距离*0.42
- 笔画宽=(weight/maxWeight)^1.5 * 6
- 悬停弧线→显示source↔target+weight
- 悬停节点→显示总提及数
- **Weight threshold slider：范围6-28**（⚠️ 未改为从1开始）

**待改进**（按优先级）**：
1. **slider最小值改为1**（导师明确要求）
2. 加排序切换（按频率/按sector/按字母）
3. 点击弧线→显示该共现对的书名列表
4. 加入原文句子

---

### 7.6 metro.html（方向二，示意性设计）⚠️ 交互最少

**当前功能**：
- 8条线路，50+站点，手动网格布局（unit=58px）
- 换乘站：双圆圈标记
- 悬停站点→显示站点名+所属线路
- 缩放平移（D3 zoom）

**8条线路**：
- North Line（#1C7293）：Granton→Leith→Princes Street→Cramond
- Old Town Line（#B85042）：Grassmarket→High Street→Canongate→Holyrood
- South Line（#2C5F2D）：Colinton→Morningside→The Meadows→Musselburgh
- East-West Line（#C9A227）：Corstorphine→Haymarket→Princes Street→Portobello
- Circle Line（#7F77DD）：Tollcross→Bruntsfield→Old Town→Princes Street→West End
- North-South Line（#A26769）：Leith→New Town→Grassmarket→Morningside→Fairmilehead
- Outer Line（#4A4A4A）：Balerno→Craigmillar→Prestonpans
- West Line（#FF6B35）：Cramond→Murrayfield→Lothian Road→Princes Street

**地铁图的叙事逻辑**（新对话需要向Merritt解释）：
- 灵感来自Harry Beck 1933年的伦敦地铁图设计理念
- Beck的地铁图用**功能性拓扑**替代地理准确性——乘客需要的是"坐哪条线、在哪换乘"，而不是地理位置
- 这个地铁图同样替换地理拓扑为**叙事拓扑**：每条"线路"代表一个叙事走廊（文学上有关联的地点群组）
- 站点是地名，线路是叙事连接，换乘站是在多个叙事走廊中都出现的枢纽地点
- 线路分组逻辑：按地理方位+文学主题（如Old Town Line连接历史旧城的核心地点）
- **关键**：站点位置≠地理位置，是手动设计的便于阅读的网格布局

**待改进**：
- 向Merritt完整解释地铁图叙事逻辑
- 点击站点→显示该地名在哪些书里出现
- 点击线路→高亮该线路+显示线路主题说明
- 加filter功能（按线路显示/隐藏）

---

## 8. 论文当前状态

**平台**：Overleaf（已分享给导师Uta Hinrichs）

**已完成的章节**（可直接粘贴到Overleaf）：
- Chapter 1 Introduction：全部完成
- Chapter 2 Literature Review：全部完成
- Chapter 3 Design：全部完成（含sector划分完整论证、六个图的设计决策）
- Chapter 4 Implementation：数据管道+五个可视化技术细节完成，Combined Interface留TODO
- Chapter 5 Evaluation：Study Design完成，Results/Discussion留TODO
- Chapter 6 Discussion：Narrative Topology + Author Spatial Languages两节完成
- Chapter 7 Conclusion：框架完成，RQ具体答案留TODO
- Appendix B：数据库schema表、sector定义表、作者统计表、共现top10表

**留TODO的部分**：
- Abstract（等用户调研结果）
- Ethics审批日期
- Acknowledgements
- Combined Interface章节
- Evaluation结果章节
- Conclusion里RQ1/RQ2的具体答案

**参考文献（mybibfile.bib）已有**：
- anderson2016（LitLong项目）
- nollenburg2006（地铁图算法）
- westphal2011（Geocriticism）
- tally2013（Spatiality）
- moretti2005（Graphs, Maps, Trees）
- stange2015（Novel City Maps，最关键参考）
- shneiderman1996（信息寻求原则）
- tufte1983（小图表原则）
- fruchterman1991（力导向布局算法）
- beck1933（伦敦地铁图）
- drucker2011（人文数据可视化）

---

## 9. 导师反馈记录

### 最新一轮反馈（本周）

| 图表 | 导师要求 | 完成情况 |
|------|---------|---------|
| 雷达图 | 区域划分要找权威来源 | ✅ 已改为官方NP Areas + Natural Neighbourhoods |
| 条形码 | 不用log，用百分比；横轴按区域排序 | ✅ 已改为独立Y轴线性scale，按sector排序 |
| 小图表网格 | 可用真实地图 | ✅ 已改为CartoDB Positron |
| 网络图 | 最小值改为1 | ✅ 已改 |
| 所有图 | 加低层级交互信息（书名、原文句子） | 部分完成，原文句子待加 |
| 线性图 | （同上） | ⚠️ slider最小值未改，书名未加 |
| 地铁图 | Merritt说还没完全理解 | ❌ 待完善 |

### 本周任务清单（导师布置）

- [x] Start adding text to dissertation
- [x] Research authoritative grouping of locations by district
- [x] Mid-term progress report（已提交到Learn，已发邮件）
- [ ] Bring in more low-level info on interaction（books, text snippets）
- [ ] Explore scale（5 authors→all; 2 authors; 2-3 books）
- [ ] Take screenshots, document pros and cons
- [ ] Start documenting AI use（Uta的form）
- [ ] Send Uta live links to sketches
- [ ] Think about feedback session design

---

## 10. 后续任务流程（按优先级）

### 第一优先级：完善现有可视化

**① linear.html**（最紧急）
- slider最小值改为1
- 加排序切换
- 点击弧线显示书名
- 原文句子hover

**② network.html**
- 点击节点显示详情面板（书名+原文句子）
- scale切换

**③ 所有图——原文句子功能**
- 从api_sentence提取数据
- 嵌入所有D3文件
- 这是导师说的"text snippets of individual location mentions"

**④ metro.html**
- 向Merritt解释叙事逻辑
- 加互动

**⑤ small_multiples.html**
- sector筛选
- 两作者对比模式

### 第二优先级：扩大规模探索

- 5作者→全部424作者（加下拉选择器）
- 只选2个作者时的变化
- 只选2-3本特定书时的变化
- 每种情况截图记录pros/cons

### 第三优先级：Live Links

- GitHub Pages部署
- 发给Uta可以直接在浏览器打开的链接

### 第四优先级：Combined Interface

- 整合所有可视化的单页面应用
- 作者选择下拉菜单
- 方向一/方向二切换
- 原文句子hover

### 第五优先级：用户调研

- 导师说中期报告后再做
- 两组参与者：领域专家 + 普通公众
- 已有伦理审批（#446635）

---

## 11. 重要技术决策记录

### 数据嵌入策略
所有D3 HTML文件把数据直接嵌入为JavaScript数组，不依赖外部CSV。原因：浏览器在file://协议下会阻止读取本地文件（d3.csv()会静默失败）。

### 共现粒度选择
- Sentence级别：0对（太细）
- Page级别：最多92个/页（太粗）
- **Document级别：403对（选定）**

### 条形码Y轴决策
- 问题：Welsh的Leith（44%）是极端值，共用Y轴会压缩所有其他作者
- 解决：per-author独立Y轴
- 代价：不能跨行比较高度
- 界面中有黄色警告说明

### 网络图边宽缩放
- v1：weight*0.3 → 线条粗细无差异
- v2：sqrt缩放 → 略有改善
- **v3：(weight/maxWeight)² * 12 → 选定，效果清晰**

### 地铁图布局
手动构建，不使用算法。原因：算法化的示意性地铁图布局是已知的NP-hard图绘制问题（Nöllenburg & Wolff, 2006），留为未来工作。

### Small Multiples底图
v1：手绘SVG抽象地图（Arthur's Seat, Pentland Hills等地标）
**v2：CartoDB Positron真实底图（Leaflet.js）** ← 当前版本

### Sector划分
v1：手动定义6个lat/lon坐标边界（不权威）
**v2：14个官方Edinburgh Council polygon（point-in-polygon）** ← 当前版本

---

## 12. 新对话开始时需要让Merritt提供的文件

如果需要查看或修改某个HTML，让Merritt上传对应文件：
- `radar.html`（`dir_1/radar/d3/`）
- `barcode.html`（`dir_1/barcode/d3/`）
- `small_multiples.html`（`dir_1/small_multiples/d3/`）
- `network.html`（`dir_2/network/d3/`）
- `linear.html`（`dir_2/linear/d3/`）
- `metro.html`（`dir_2/metro/d3/`）
- `dissertation.tex`（`dissertation/main/`）

如果需要运行Python脚本，数据库在本地，连接命令：
```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')
```

Python脚本保存在各自的`py/`目录下（之前在/tmp/下，已经move到项目目录）。

---

## 13. 已完成的所有主要工作总结

| 工作 | 完成时间 | 状态 |
|------|---------|------|
| PostgreSQL数据库搭建 | 早期 | ✅ |
| mention_order自定义表 | 早期 | ✅ |
| 6个Python原型可视化 | 第一轮 | ✅ |
| 官方sector划分（14个） | 本周 | ✅ |
| radar.html D3交互版 | 本周 | ✅ |
| barcode.html D3交互版 | 本周 | ✅ |
| small_multiples.html D3+Leaflet版 | 本周 | ✅ |
| network.html D3版（slider改为1-28） | 本周 | ✅ |
| linear.html D3版 | 本周 | ⚠️ |
| metro.html D3版 | 本周 | ⚠️ |
| 论文框架+大量填写 | 本周 | ✅ |
| mybibfile.bib完整参考文献 | 本周 | ✅ |
| 中期报告（progress report） | 本周 | ✅ 已提交 |
| GitHub push | 本周 | ✅ |
| Python脚本归档 | 本周 | ✅ |

---

*文档生成时间：2026年7月10日*
*项目状态：中期报告已提交，六个D3可视化基本完成，论文大量章节已填写，用户调研待进行*

---

## 14. 早期关键决策记录（从历史会话中补充）

### 可视化方案的筛选过程（8个候选→6个最终方案）

**最初8个候选方案：**

方向一（指纹类）：
1. 雷达图 ✅ → 选入
2. 小图表网格 ✅ → 选入
3. 色彩地图轮廓（Color Map Silhouette）❌ → 淘汰（爱丁堡市区地名集中，作者间区分度不足）
4. 条形码指纹 ✅ → 选入

方向二（拓扑类）：
5. 力导向网络图 ✅ → 选入
6. 地铁图拓扑 ✅ → 选入
7. 弦图（Chord Diagram）❌ → 淘汰（弧线过多会视觉拥挤；且弦图暗示循环对称结构）
8. 邻接矩阵热力图（Adjacency Matrix Heatmap）❌ → 淘汰（对普通用户不友好，看起来像数据表格）

**线性连接图是怎么来的**：弦图淘汰后，保留了其"连线显示共现"的逻辑，但改为线性横轴排列（而非圆形）。导师明确指出圆形暗示循环结构，不适合有明确开头结尾的文学叙事，因此改为线性。

---

### 条形码图scale演变过程

**v1：对数scale（log）**
- 问题：log scale视觉上不直观，用户难以理解两倍差距意味着什么
- 导师反馈：不要用log

**v2：线性scale，共用Y轴**
- 问题：Welsh的Leith（44%）是极端值，共用Y轴下其他所有作者的分布被压扁到几乎看不见

**v3（最终）：线性scale，per-author独立Y轴**
- 每位作者的Y轴缩放到自己的最大值
- 代价：不同作者的条形高度不能直接比较
- 界面中加了黄色警告框明确告知用户
- 理由：指纹看的是形状（within-author分布），不是跨作者量级比较

---

### 网络图边宽缩放演变过程

**v1：width = weight * 0.3（线性）**
- 问题：所有边看起来粗细差不多，没有视觉层级

**v2：width = sqrt(weight/maxWeight) * 8**
- 问题：略有改善但强连接仍然不够突出

**v3（最终）：width = (weight/maxWeight)² * 12（平方归一化）**
- 强连接比弱连接在视觉上有明显的量级差异
- 既能看出强连接，又保持弱连接可见

---

### 五位测试作者的选择依据

从424位作者中选出5位，基于三个标准：
1. **时间跨度大**：Scott/Lockhart是19世纪，Stevenson是维多利亚晚期，Welsh和McCall Smith是当代
2. **风格对比明显**：Welsh写Leith底层，Stevenson写Old Town哥特风，Scott写历史，McCall Smith写现代轻松爱丁堡
3. **数据量足够**：每人都有1000+次提及，雷达图不会因数据太稀疏而失真

---

### Reader-plot方向的放弃决策

最初曾考虑第三个方向：**Reader-plot时间轴**——横轴代表叙事进程，记录一位作者在书中先写哪个地方、后写哪个地方。

- `mention_order`表的`position_pct`字段为此方向已做好数据准备
- 放弃原因：这个方向需要用户理解"叙事时间"的概念，门槛较高；加上前两个方向已经足够完整，三个方向反而会分散论文焦点
- 现状：数据已备好，列为"未来工作"（Future Work章节已提及）

---

### 文学沉默（Literary Silences）方向的放弃决策

最初第四个方向：展示爱丁堡哪些区域在文学中从未被提及（"文学沉默"的可视化）。

- 概念来自Moretti的"literary silences"
- 放弃原因：需要完整的爱丁堡城市人口/区域分布数据作为对比基准，且LitLong数据集本身的覆盖面有限（620部作品，选取有偏差），在没有全覆盖的数据基础上谈"沉默"存在方法论问题
- 现状：在论文Discussion章节作为局限性提及

---

### 弦图vs线性连接图的选择

弦图（Chord Diagram）：
- 优点：全局视角强，能一眼看出"枢纽"地名
- 缺点：弧线一多就视觉拥挤；暗示循环对称结构

线性连接图（选定）：
- 优点：线性轴不暗示循环，地名按频率排列有意义
- 缺点：两端地名之间的弧线会很高，可能遮挡
- 导师明确指示：不用弦图，改用线性排列

---

### 地图底图的演变

Small Multiples v1：手绘SVG抽象地图（Arthur's Seat、Pentland Hills等地标轮廓）
- 问题：看起来不真实，用户难以定位

Small Multiples v2（当前）：CartoDB Positron真实地图底图（Leaflet.js）
- 导师反馈："can use real map"
- 选择Positron而非标准OSM：因为Positron颜色极简（接近白色），气泡在上面显眼，不会被地图背景淹没

---

### 数据嵌入策略的决定

所有D3 HTML文件把数据直接嵌入为JavaScript数组，不依赖外部CSV。

原因：浏览器在`file://`协议下会阻止读取本地文件（CORS policy），`d3.csv()`调用会静默失败，不给任何报错。发现这个问题是在第一次做D3原型时花了很长时间调试的。

解决方案：Python生成数据后直接写入HTML文件的`<script>`标签里。

