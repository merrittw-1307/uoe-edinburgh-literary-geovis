# 项目完整迁移说明文档 v3
## A Visual Trace Map of Edinburgh Place Names in Literature
### MSc Dissertation — Merritt Wang (S2887338)
### University of Edinburgh, School of Informatics, 2025–2026
### 生成时间：2026年7月10日（本文档取代 handover_v2.md，v2继续保留作历史存档；同日追加并扩充了第15节"规模探索"——现已覆盖全部六个图）

---

## ⚠️ 阅读本文档的AI助手注意事项

1. **默认用中文回复**，除非Merritt用英文写
2. **不要一味同意**，要客观，遇到不合理的地方要指出——今天这次会话里最有价值的进展，就是先诚实指出metro.html的"叙事逻辑"其实是编的、不是数据算出来的，然后才重建它。这个"先质疑再动手"的模式值得延续。
3. **读完整份文档**再回复第一条消息
4. 本项目正在进行中，不要从头开始，要接着做
5. Merritt的偏好：doppio咖啡，抽烟，多个纹身，INFJ-T，来自大连/北京，现居爱丁堡

---

## 0. 与v2相比，这次改了什么（先看这个）

- **六个可视化的交互性大幅补完**：radar/barcode/small_multiples/network/linear 都加上了导师要的"原文句子hover/详情面板"，linear和network的滑块/排序/scale待办也清掉了
- **metro.html 整个方法论重做**：从"手绘地理示意图套了个叙事拓扑的名头"，变成"从403条真实共现数据里用社群检测算出来的5条线"，是这次最大的一块工作，详见第14节
- **论文路径修正**：v2文档里写的 `dissertation/main/` 不存在，实际路径是按日期命名的文件夹，目前最新是 `dissertation/10Jul/dissertation.tex`
- **新增数据管道脚本**：见第2节仓库结构更新
- **规模探索完成**（导师第二优先级任务，分两轮）：六个图全部测了2/5/20/全部作者规模。核心发现：六个图不是共享一个规模上限，是六个不同的失效模式（radar视觉重叠、barcode要滚动、network/linear同根因不同轴、small_multiples唯一有真实计算成本、metro是算法本身失效）。写进论文Limitations两段+新Appendix汇总表。详见第15、15b节

---

## 1. 项目概述

（与v2一致，未变）

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
- **数据处理**：Python 3.11（`/usr/local/bin/python3.11`，非系统自带的3.9）— pandas, sqlalchemy, psycopg2-binary, networkx
- **可视化**：D3.js v7（交互式），Leaflet.js 1.9.4（地图）
- **论文**：LaTeX on Overleaf（infthesis.cls模板）
- **版本控制**：GitHub

---

## 2. GitHub仓库

**地址**：https://github.com/merrittw-1307/uoe-edinburgh-literary-geovis

### 本地目录结构（本次更新部分标注★）

```
/Users/wangmingyu/Downloads/UoE/Dissertation/
├── data/
│   ├── raw/...(未变)
│   └── processed/
│       ├── sectors/location_sectors_v2.csv
│       ├── dir_1/
│       │   ├── radar/
│       │   │   ├── py/
│       │   │   │   ├── generate_dir1_sentences.py  ★新增：算原文句子
│       │   │   │   └── inject_sentences.py         ★新增：注入到radar.html
│       │   │   ├── d3/radar.html, radar_v1.html, radar_v2.html★
│       │   │   └── data/radar_data_v2.csv, dir1_sentences.json★
│       │   ├── barcode/
│       │   │   ├── py/inject_sentences.py ★新增
│       │   │   ├── d3/barcode.html, barcode_v1.html, barcode_v2.html★
│       │   │   └── data/dir1_sentences.json★
│       │   └── small_multiples/
│       │       ├── py/generate_dir1_sentences.py 的输出被这里复用
│       │       ├── d3/small_multiples.html, small_multiples_v1.html, small_multiples_v2.html★
│       │       └── data/small_multiples_enriched.json★
│       └── dir_2/
│           ├── network/
│           │   ├── py/generate_enriched_data.py ★新增：核心共现数据+书目+原句
│           │   ├── d3/network.html, network_v1.html, network_v2.html★
│           │   └── data/network_edges.csv, network_nodes.csv, network_enriched.json★
│           ├── linear/
│           │   ├── py/build_linear_html.py ★新增
│           │   ├── d3/linear.html, linear_v1.html★
│           │   └── data/linear_enriched.json★
│           └── metro/
│               ├── py/
│               │   ├── build_metro_lines.py ★新增：核心！社群检测+布局算法
│               │   └── build_metro_html.py  ★新增：渲染
│               ├── d3/metro.html, metro_v1_geographic.html★（旧的纯手绘地理版备份）
│               └── data/metro_lines.json★
├── dissertation/
│   └── 10Jul/dissertation.tex   ← ⚠️ 不是 main/，是按日期命名的文件夹，目前最新是10Jul
├── .claude/launch.json ★新增：本地静态文件预览服务器配置（python3.11 -m http.server 8743）
└── docs/
    ├── handover_v1.md, handover_v2.md（历史存档）
    └── handover_v3.md ← 本文档
```

### 环境注意事项（新发现，容易踩坑）

- 系统自带的 `python3`（`/usr/bin/python3`，Apple CommandLineTools自带的3.9）**没有装pandas**，而且用它跑 `python3 -m http.server` 会因为sandbox限制报 `PermissionError: os.getcwd()`。
- 真正能用的是 `/usr/local/bin/python3.11`，已经装好 pandas / sqlalchemy / psycopg2-binary / networkx。**以后跑数据脚本请显式用这个路径**，不要直接写`python3`。
- 数据库连接不需要密码（peer auth），`psql -U wangmingyu -d litlong_edinburgh` 或 `sqlalchemy` 的 `postgresql://wangmingyu@localhost:5432/litlong_edinburgh` 都可以直接用。

---

## 3. 数据库

（与v2一致，未变，略）连接信息：`litlong_edinburgh` / `wangmingyu` / 端口5432 / PostgreSQL 16。

### ⚠️ 本次发现的一个预先存在的数据问题（未修复，仅记录）

给5位测试作者的mention数据 JOIN `api_location` 表时，会丢失约35%的行（18,700→12,110），原因是部分`location_id`是悬空外键（`api_location`里找不到对应记录）。`network_data2.py`等原始脚本本来就带这个JOIN，所以这不是本次改动引入的问题，只是核对数据时顺带发现。如果以后要对比不同图之间的"提及数"口径，或者要写方法论的数据质量说明，这个点需要处理。

---

## 4. 五位测试作者

（与v2一致，未变）

| 作者 | 提及数 | 书数 | 主导sector | 占比 |
|------|--------|------|-----------|------|
| Alexander McCall Smith | 7,320 | 17 | New Town | 43.6% |
| Irvine Welsh | 2,634 | 8 | Leith | 44.3% |
| John Gibson Lockhart | 3,046 | 6 | New Town | 25.9% |
| Walter Scott | 2,796 | 12 | Old Town | 32.0% |
| Robert Louis Stevenson | 1,778 | 16 | Old Town | 20.7% |

---

## 5. 14个官方Sector划分

（与v2一致，未变，略——见handover_v2.md第5节）

---

## 6. 关键数据发现（新增第6、7条）

发现1-5与v2一致（作者空间语言个性化、sector分布验证文学史认知、共现粒度用document级别、叙事拓扑≠地理拓扑Leith&Princes St weight=28、Scott广域地理范围）。

**发现6（新增）：地铁图的社群结构揭示了新的叙事分组**。对57个核心地名、403条共现边做modularity社群检测（不设人工分组），自然分出3个大社群+2个可以再细分的子社群，最终5条线：
- McCall Smith的New Town/Scotland Street世界（16站，2786提及）
- 混合线"Leith & Forth Corridor"（23站，1564提及）——没有单一作者主导，混了Stevenson的私人地点（Swanston、Heriot Row）和几位作者共用的历史老城地点
- Scott的历史老城+周边Lothians（14站，826提及）
- Welsh的底层外围地带（12站，494提及）
- **Lockhart的传记地理**（5站，202提及）——Castle Street、Lasswade、University of Edinburgh等，正好是Lockhart写《Life of Walter Scott》时提到的Scott本人住址和活动地点，是一条真正意义上的"传记地理"走廊

**发现7（新增）："Leith"这个词本身跟历史老城的关联比跟Welsh的关联更强**。反直觉——Leith没有落在Welsh的那条线上，而是落进了混合的历史老城线。说明"Leith"作为地名，在5位作者合并统计下，跟Scott/Lockhart的历史叙事关联比跟Welsh的当代叙事关联更强。这个可以直接写进Discussion章节，是一个新的、非预期的发现。

---

## 7. 六个可视化HTML——当前状态（本次全部更新，含新增交互）

### 通用变化

- 所有图的原文句子数据来源统一为一套Python脚本生成的JSON（`generate_enriched_data.py`用于dir_2，`generate_dir1_sentences.py`用于dir_1），**只做数据叠加，没有改动任何已有的百分比/绝对数/书目数字**——这一点很重要，如果以后要改这些图，切记不要在同一次改动里把"加新功能"和"改核心计算逻辑"混在一起。
- 本地预览：`.claude/launch.json`已配置静态服务器，端口8743，根目录是项目根目录，可以直接访问 `http://localhost:8743/data/processed/.../xxx.html`。

### 7.1 radar.html ✅ 完成度更高

新增：详情面板里"Top places in this sector"的每一行现在可以悬停出原文摘录+书名（复用已有的tooltip元素，没加新DOM）。数据来自 `dir1_sentences.json`。

### 7.2 barcode.html ✅ 完成度更高

新增：点击任意条形后，详情面板的书目列表下方多了一行示例原句+出处（`.dp-quote`）。

### 7.3 small_multiples.html ✅ 完成度大幅提升

新增三项（导师要求的sector筛选+对比模式+原文句子，全部做了）：
- Sector图例筛选：点击某sector标签，5张地图同时隐藏/显示该sector的气泡
- **"Compare 2 authors"模式**：切换后从5张小地图变成2张更大的地图（640×460），两个下拉菜单选作者；切换回"All 5 authors"会正确销毁旧Leaflet实例再重建（测过反复切换不会有残留/报错）
- 气泡popup里加了一条示例原句

### 7.4 network.html ✅ 完成

新增：
- 点击节点→右侧详情面板：sector、总提及数（或占比）、top5真实共现地名、书目列表（带次数）、一条示例原句
- 节点大小切换：Absolute（原log刻度）/ Percentage（面积比例sqrt编码）
- 底层数据从"预先裁剪过的96条边/28个地名"扩展成"全量403条边/57个地名"——之前slider拉到1也看不到新东西，现在是真的全量

### 7.5 linear.html ✅ 完成，导师提的四项待办全部清空

- slider min改成1（原来是6）
- 排序切换：频率 / sector（带图例）/ 字母序
- 点击弧线→右侧面板显示该地名对共享的书目列表
- 悬停地名→tooltip加原文摘录
- 顺手加了搜索框（不在原始待办里，但符合"自主探索"的要求）
- 底层数据同network.html，扩展成全量403边/57地名

### 7.6 metro.html ✅✅ 本次核心工作，方法论级别重做

**旧版本的问题**（已诚实指出并解决，不是数据不够，是设计偷懒）：
1. 旧的8条线是手画的地理示意图，套了"叙事拓扑"的名头，但实际验证发现：67对"同线相邻站点"里只有15对（22%）有真实书目共现支撑
2. 换乘、交叉全靠人工拍脑袋，不是从数据算出来的

**新版本管道**（两个脚本，见`data/processed/dir_2/metro/py/`）：

1. **`build_metro_lines.py`**——核心算法脚本：
   - 用403条共现边（57个地名）做modularity社群检测（`networkx.community.greedy_modularity_communities`，权重阈值3），大社群（>18站）递归再聚类
   - 没有强连接落进任何社群的孤立地名，折叠进它在全量数据里连接最强的社群
   - 每条线内部用最近邻链排序站点顺序，保证"同线相邻"=真实强共现
   - 换乘检测：权重≥10的跨社群边，让该站点也出现在另一条线上
   - 线路命名：自动算——如果某作者贡献了≥55%的书目提及量就叫"XX's Edinburgh"，否则用最高频两个地名命名
   - **布局**：`networkx.spring_layout`（共现权重做弹簧引力）算出连续坐标，量化到22×15网格，碰撞检测把重叠的站点螺旋式挪开，**每个站点全图只有一个坐标**（不是每条线各算各的）——这样两条线真的共享同一个换乘点时，画出来会真的交汇，不是靠虚线连
   - **可复现性**：Python的哈希随机化会导致社群内部排序每次略有不同（社群归属不变，只是站内顺序抖动），跑的时候要加 `PYTHONHASHSEED=0`
   - 输出：`data/metro_lines.json`，含每条线的站点顺序+坐标+`adjacency_backed`/`adjacency_total`诊断指标

2. **`build_metro_html.py`**——渲染脚本：
   - **Octilinear折线**：真实地铁图的线段角度只能是0°/45°/90°（Beck的核心规则）。两个网格点之间如果不满足这个角度，就插一个"先斜再直"的折点（dog-leg），不是直接连一条怪角度的斜线
   - **贪心标签避让**：每个站名先试8个方向（上下左右+四个斜角）×2个距离圈，量一下候选框会不会跟已放好的其他站名/圆点重叠，选第一个不冲突的位置。57个站里从10对重叠降到2对（都在最密集的换乘枢纽区）
   - 点击站点→详情面板：所属线路（多chip）、sector、总提及、top5共现、书目、原句
   - 点击线路（图上或图例）→隔离显示，图例显示该线"相邻站点真实共现支撑率"
   - 搜索框高亮

**结果（可以直接写进论文方法论/评估章节）**：
- **46/52（88%）相邻站点有真实共现支撑**，对比旧版本的15/67（22%）
- 各线细分：Smith's Edinburgh 13/14 (93%)、Leith & Forth Corridor 9/11 (82%)、Scott's Edinburgh 9/12 (75%)、Welsh's Edinburgh 11/11 (100%)、Lockhart's Edinburgh 4/4 (100%)
- 12个真实换乘站：Arthur's Seat, Bruntsfield, Canongate, Dundas Street, Holyrood, **Leith**, Morningside, New Town, **Princes Street**, Queen Street, Stockbridge, The Meadows——Leith和Princes Street都是换乘站，直接对应"weight=28"这个核心发现

**旧版本备份在** `metro_v1_geographic.html`，建议在论文里做一个before/after对比图，这本身就是很好的方法论素材。

---

## 8. 论文当前状态

**⚠️路径更正**：不是 `dissertation/main/`，实际是 `dissertation/10Jul/dissertation.tex`（按日期命名的文件夹，每次导出新版本会建一个新日期文件夹，目前10Jul是最新的）。

**当前已完成的章节**（截至v2交接时的状态，v2里的描述仍然准确）：Ch1-3基本完成，Ch4部分完成（Combined Interface留TODO），Ch5 Study Design完成/Results留TODO，Ch6两节完成，Ch7框架完成，Appendix B完成。

**⚠️本次会话结束后需要做但还没做的事**：论文里关于metro-style map的所有描述（Design章节~L243-247、Literature Review里引用Nöllenburg & Wolff的段落~L160、Implementation章节~L346-348、Design Summary表格~L267、Limitations里的"Manual metro-map layout"条目~L439）**全部是旧版本的描述（8条手绘线），需要重写成新的数据驱动方法论**。另外Limitations里的"Source text integration"条目（~L443，说原文句子"尚未整合"）现在已经不成立了，因为原文句子已经整合进全部6个图了，需要改写或删掉。

---

## 9. 导师反馈记录（更新）

| 图表 | 导师要求 | 完成情况 |
|------|---------|---------|
| 雷达图 | 区域划分要找权威来源 | ✅ 已改为官方NP Areas + Natural Neighbourhoods |
| 条形码 | 不用log，用百分比；横轴按区域排序 | ✅ 已改为独立Y轴线性scale，按sector排序 |
| 小图表网格 | 可用真实地图 | ✅ 已改为CartoDB Positron |
| 网络图 | 最小值改为1 | ✅ 已改 |
| 所有图 | 加低层级交互信息（书名、原文句子） | ✅ **全部6个图都已完成**（radar/barcode/small_multiples/network/linear/metro） |
| 线性图 | slider最小值、书名 | ✅ 已改 |
| 地铁图 | Merritt说还没完全理解 | ✅ **已重新设计为数据驱动版本，方法论上可以完整解释和答辩** |

---

## 10. 后续任务流程（更新）

### 已完成（本次会话）
- [x] 六个图全部加入"低层级交互信息"（原文句子/书名）
- [x] linear.html 全部待办清空
- [x] network.html 详情面板+scale切换
- [x] small_multiples.html sector筛选+双作者对比
- [x] metro.html 方法论级重做（数据驱动线路+真实换乘+octilinear布局+标签避让）

### 第一优先级：论文同步
- [ ] 重写Design章节的metro-map小节（数据驱动方法论）
- [ ] 重写Literature Review里Nöllenburg & Wolff那段（从"手动布局的理由"改为"启发式自动布局怎么做的"）
- [ ] 更新Implementation章节metro小节+Design Summary表格
- [ ] 更新/删除Limitations里"Manual metro-map layout"和"Source text integration"两条
- [ ] Discussion章节加一段：地铁图验证结果（88% vs 22%）+ "Leith更靠近历史老城线"这个新发现
- [ ] Appendix加一个表：5条线的名称/站数/adjacency_backed百分比

### 第二优先级：扩大规模探索 ✅ 已完成（详见第15节）
- [x] 5作者→全部408位（有地名数据的）作者——radar + network两个代表图
- [x] 只选2个作者/2-3本书的变化
- [x] 截图+决策log记录pros/cons（`data/processed/scale_exploration/NOTES.md`）
- [x] 结果写进论文（Limitations + Discussion）

### 第三优先级：Live Links（未开始）
- GitHub Pages部署

### 第四优先级：Combined Interface ✅ 框架搭建完成（详见第16节），实时功能未开始

### 第五优先级：用户调研（未开始，⚠️见下方时间线提醒）

**时间线提醒（延续v2里提过的观察）**：今天是7月10日，截止8月21日，剩6周。用户调研（招募+跑session+分析）应该尽快启动，不要等前面几项全部做完再排期。

---

## 11-13. （与v2一致，未变，略）

见 `handover_v2.md` 第11节"重要技术决策记录"、第12节"新对话开始时需要提供的文件"、第13节"已完成工作总结"。

---

## 14. 本次会话的关键技术决策记录

### 为什么metro.html要重做而不是只加交互

用户先问"为什么现在的地图不好看，是不是数据不够"，核查后发现根本原因是设计偷懒（每条线单独一条车道，换乘靠虚线连），不是数据问题。用户选择了"数据驱动重建"这个最大工作量的选项，而不是"保留现状只加交互"或"诚实标注为人工策展"。这个决策优先级：**方法论正确性 > 视觉稳定性/工作量**。

### 社群检测阈值的选择过程

- 尝试了threshold=3/4/5/6，权重阈值越高，图越碎（threshold 5-6时31个社群，大部分是孤立单点）。threshold=3时得到3个大社群（22/14/12）+9个孤立点，是最干净的分割
- 22节点的大社群继续用递归子聚类拆成3个（16/7/7），拆出来的子群刚好对应Scott历史叙事、Lockhart传记地理、Stevenson私人地点——这不是我预设的，是数据自己分出来的

### 换乘阈值的选择

- 一开始用weight≥6，得到28个换乘站（57个里差不多一半），太密，图会很乱
- 改成weight≥10，得到12个换乘站，更符合"换乘应该是少数重要枢纽"的直觉，也更好读

### 布局：为什么放弃"一线一车道"改成共享坐标

用户反馈"五条直线不好看，不像真的地铁"——如果每条线单独分配一条水平车道，换乘站在物理上不是同一个点，只能用虚线示意，看起来假。改成用`spring_layout`给每个站点算一个全图唯一的坐标后，两条线真的会在换乘点交汇/交叉，视觉上才像真的地铁网。

### Octilinear角度规范化

用户反馈"线路歪歪扭扭"——网格坐标直连的直线角度是任意的。加了一个"先斜再直"的折点算法（dog-leg），把每段线都规范成0°/45°/90°，这是Beck地铁图设计的核心规则之一，之前漏掉了。

### 标签重叠

用户反馈"站名字体重叠"——加了贪心标签避让（8方向×2距离圈候选，避开已放置的标签和圆点）。10对重叠降到2对，剩下的都在最密集的单个换乘枢纽区，跟真实地铁图偶尔需要手动微调标签的情况类似。

### 可复现性陷阱

第一次跑`build_metro_lines.py`两次，结果站点顺序不一样（社群归属没变，只是站内排序抖动）——原因是Python的hash随机化影响了`greedy_modularity_communities`内部的set/dict遍历顺序。修复：所有涉及`set()`遍历的地方改用`sorted()`，并要求用`PYTHONHASHSEED=0`跑脚本才能拿到字节级一致的输出。这个坑值得记录，因为如果以后要重新生成这个数据集用于论文里的图表，必须固定这个环境变量，否则每次生成的地图会有细微不同（虽然核心结论/社群归属不变）。

---

## 15. 规模探索（导师第二优先级任务，本次会话补充）

### 范围决策（第一轮）

Merritt第一次明确要求：只挑两个代表图（radar代表方向一、network代表方向二），不是六个图都做；同时要求"留痕"（决策过程要能查）、"不要覆盖历史版本"、"效果好才更新论文"。三条都照办了：

- 新建了独立目录 `data/processed/scale_exploration/`，完全不碰 `dir_1/radar/`、`dir_2/network/` 里现有的5作者版本
- 新文件：`radar_scale_explore.html`、`network_scale_explore.html`（两个全新的探索工具，不是截图，是真的可交互）
- 决策过程和最终发现全部写在 `data/processed/scale_exploration/NOTES.md`，比这里更详细，是主要的方法论记录
- 效果判断为"好"（发现了非预期的、量化的、可以直接写进论文的规律），已经更新论文和这份手册

### 两个工具怎么做的

**radar_scale_explore.html**：数据来自新脚本 `generate_all_authors_radar_data.py`，把原来锁死5位作者的SQL去掉WHERE条件，跑全部424位作者（408位有地名数据）。**先做了正确性校验**：拿这个新脚本算出来的5位作者数值，跟论文Appendix里已发表的5个百分比逐一对比，全部精确匹配到小数点后3位，才敢往下继续。工具本身：4个预设按钮（2/5/20/全部）+ 搜索框自由加人 + hover隔离某个作者的多边形。

**network_scale_explore.html**：数据来自 `generate_all_authors_network_data.py`，导出全部12,243条(author, place, document)原始记录（不预先聚合），**在浏览器里用JS实时计算**"每作者取top15地名→document级别共现"，这样选择任意作者子集时图会实时重算，不是预设几个固定画面。多加了一个"按书"模式：选2-3本具体的书，直接用这几本书的地名共现（不做top15过滤，因为书本身就已经是小范围了）。

### 发现（已写进论文，也是最有价值的部分）

**radar图**：合法性随作者数单调下降——20人时多边形已经叠得分不清形状，408人时完全是一团乱麻，验证了Limitations章节里本来只是"存疑"的判断。但发现一个缓解手段：hover隔离功能在408人规模下依然有效（测试过，能把目标作者的多边形从背景噪音里拎出来），代价是从"一次看全部"退化成"一次看一个"——不是完全失效，是优雅退化。这个更precise的说法已经写进Limitations。

**network图（这个发现更有意思，非预期）**：密度不是随作者数单调变化的，是U型的，而且两头密的原因完全不同：
- 2位作者/2-3本书时密：document级别共现在小样本下会退化成"只要在同一本书里出现过就算共现"——这几乎是所有地名对的默然状态。实测3本书（McCall Smith两本+Welsh一本）在weight≥1时密度51%，提高到weight≥2立刻掉到33个地名、423对，而且几乎全是McCall Smith自己两本书之间的（他的Scotland Street世界反复出现），跟Welsh的书完全没有交集——这正好是"发现1"（作者间几乎零共享地名）在book级别的具体体现
- 408位作者时稀：加作者加的是节点，不是真实的跨作者边，因为大部分作者之间词汇不重叠（还是发现1）
- **5位作者的原始选择正好卡在中间**：既不会像2人/2-3本书那样"什么都trivially连起来"，也不会像408人那样"基本不连"，这个中间态可能是原来选5位作者时凭直觉做对了、但没有明说的理由

### 第一轮论文改动位置

- Limitations "Five-author prototype" 段落——把"是否scale是个open question"改写成有具体数据支撑的答案（hover隔离能救场，但要接受"一次一个"的代价）
- Discussion "Author Spatial Languages" 节——新增一段，把network密度的U型发现和"发现1"（作者词汇不重叠）显式连起来

### 第一轮数据管道注意事项

`generate_all_authors_radar_data.py` 和 `generate_all_authors_network_data.py` 都在 `data/processed/scale_exploration/py/`，跑完会自动做正确性校验打印在终端（radar脚本会对比5个已发表数值）。这两个探索工具用的是完全独立的数据管道，没有复用`dir_2/network/py/generate_enriched_data.py`（那个是锁定5作者的），所以5作者配置下两边算出来的边数会有小差异（403 vs 实测的~403附近），差异来源已经在NOTES.md里写清楚了，不是bug。

---

## 15b. 规模探索第二轮——剩下四个图（同日，Merritt追加要求）

Merritt紧接着要求把剩下四个图（barcode、small_multiples、linear、metro）也做完，同样的四个规模档位（2/5/20/全部），同样要留痕、不覆盖历史版本。这一轮最大的收获：**六个图不是共享一个"规模上限"问题，是六个各不相同的失效模式**，这个发现本身比任何单个数字都重要。

### 四个新工具怎么做的

- **barcode_scale_explore.html**：数据脚本`generate_all_authors_barcode_data.py`，每位作者展示自己的top15地名（不是原版固定的39地名共享列——408个差异巨大的作者没法共享一套列名）。实测了才知道：408行渲染只要20ms，完全不卡，问题纯粹是页面变成45,274px高（约50屏），"一眼对比两个作者"这个卖点没了，但不是渲不出来。
- **linear_scale_explore.html**：直接复用network那份12,243行原始数据，同样的JS实时共现计算，换成弧线+横轴的画法。发现一个容易看错的现象：408作者时SVG宽度是29,790px，但截图只看得到最左边一小段（跟20作者截图长得几乎一样），因为容器是横向滚动的，最左边总是提及数最高的那几个地名——不是没更新，是画对了但没人会滚动29,790px去看完。
- **small_multiples_scale_explore.html**：这个是唯一真的测了"计算成本"而不是"好不好看"的——每个面板是真实的Leaflet地图实例，会真的请求网络贴图。实测：5→50位作者时每个面板初始化成本基本不变（1-3ms），但50→408时骤降3.6倍（408位作者时1.47秒，直接测的不是推算的）。这是六个图里唯一一个"规模太大真的会让浏览器卡顿"的，其他五个都只是"不好看"或"要滚动"。
- **metro的方法不一样**：社群检测+弹簧布局+octilinear修正都是networkx的批处理运算，没法简单搬到浏览器里实时跑，所以这个是Python批处理脚本（`metro_scale_test.py`），不是live网页。复用了`build_metro_lines.py`里的函数（import，没有复制粘贴逻辑），在2/5/20/50位作者规模下重跑一遍，另外渲染了一个20作者的完整HTML（`metro_scale_explore_20authors.html`）截图用。

### 发现（已写进论文）

- **barcode**：失效方式是"要滚动"，不是"渲不出来"或"看不清"——跟radar（视觉重叠）和network/linear（同一个根因：一条轴上塞所有东西，只是横轴纵轴不同）都不一样。
- **small_multiples**：唯一一个有真实计算成本的图，而且是非线性的（50→408时每面板成本涨3.6倍）——是六个图里唯一"规模太大可能真卡死"的。
- **metro**：社群检测算法本身在规模变大后会失效，不只是画面变乱。50位作者时，有一条线膨胀到75个站——因为`greedy_modularity_communities`判断这一大块内部连接太紧密、不该再拆，即使已经超过18站的上限。同时adjacency-backed比例单调下降：96%(2人)→92.5%(5人)→84.4%(20人)→72.5%(50人)。**顺带发现**：拿这套通用管道重新算5作者配置，算出来也是5条线，但McCall Smith的内容拆成了两条（跟正式版metro.html的5条线不完全一样）——不是bug，是两边用独立算出来的共现图，边权重有细微差异，社群检测对这种差异很敏感，这本身也是一个值得写进论文的真实局限。

### 第二轮论文改动位置

- Limitations "Five-author prototype, tested at scale" 段落——从只讲radar扩展成六个图各自的失效模式概述，指向新的Appendix表格
- Limitations "Metro-map layout is heuristic" 段落——把"重新跑管道可能会产生不同分组"从推测改成了有具体数据的确认（20人→8条线，50人→11条线+75站超大线）
- 新增Appendix "Scale Exploration Summary"（`tab:scale-summary`）——一张表总结六个图各自的失效模式，方便审阅人一眼扫过去

### 如果以后要重新生成这批数据

四个新脚本都在`data/processed/scale_exploration/py/`：`generate_all_authors_barcode_data.py`、`generate_all_authors_small_multiples_data.py`（这个要重新JOIN `api_location`拿lat/lon，跟其他脚本不共用）、`metro_scale_test.py`（批处理分析，用`importlib`直接import了`build_metro_lines.py`，不是复制代码）、`render_metro_scale_snapshot.py`（渲染20作者截图用，同样import了`build_metro_lines.py`和`build_metro_html.py`）。metro相关的两个脚本记得也要`PYTHONHASHSEED=0`跑，原因跟正式版一样（社群检测的tie-breaking依赖哈希顺序）。

---

## 16. 2026年7月11日会话：论文内容补充 + PIS/Consent阻塞 + Combined Interface框架

Merritt提供了伦理审批日期（5月13日），并明确指示：跟用户调研相关的内容先放一放，下周针对性开始；这期间把其他能做的内容最大限度完成。随后又追加要求把剩下两项（PIS/Consent Form插入 + Combined Interface）同时推进。

### 论文内容补充（不依赖用户调研的部分，全部完成）

- 伦理批准日期填入前置页（13 May 2026）
- Acknowledgements草稿（标注为DRAFT，提醒Merritt审阅补充个人化感谢内容）
- Abstract v1草稿：写全问题/数据/两个研究问题/方法/六个设计/用户调研，RQ2部分用已有数据支撑的发现（Leith/Princes St权重28，metro 22%→88%），结尾留一句TODO等RQ1结果
- Conclusion的RQ2回答：直接给"Yes"结论，引用metro重做（§sec:metro-redesign）和规模探索附录（§app:scale）的数据，RQ1继续留空等用户调研
- Appendix A的Task Questions和Survey Questions全部写完整（原来是TODO）：Task 1（5选1指纹识别+置信度+理由）、Task 2（叙事/地理关系判断+远近判断+可选理由）、任务后排序；Survey背景4项+反思4项开放题。顺手修正了3处`Section~\ref{chap:eval}`应为`Chapter~\ref{chap:eval}`的引用错误（chap:eval是章节级label）
- 每次编辑后手动核对了大括号/环境配对（`\begin`/`\end`计数），因为本地没有LaTeX编译环境

### PIS / Consent Form —— 仍阻塞，非我能自主处理

检查了`ethics/PIS_Informatics_LitLong.docx`和`ethics/Participant_Consent_Informatics_LitLong.docx`（用macOS自带`textutil -convert txt`读取，没装新软件）。**两份都是三个学生共用的"雨伞"申请模板，没有个人化**：
- PIS开头就是"this is part of an 'umbrella' ethics application that includes all MSc students..."，里面写着`Researcher collecting data: [Yvonne Preiss, Jiaki Zhang, Merritt Wang; to be edited accordingly]`和`reference number XXXXX [edit accordingly]`
- Consent Form里有多处`[delete as appropriate]`的Yes/No选项（比如是否同意录音）没有勾定

这些是Merritt自己的协议决定（保留哪几位学生的名字、勾哪个录音选项、填哪个reference number），我没有代她填写。已经明确告知她："把这两份docx改成你自己单独的版本（研究者只写你自己，勾好该删的选项，reference number填446635），发给我文件我再帮你转PDF插进Appendix A；或者你自己导出PDF发我，我直接接进`\includepdf`。" Appendix A里两处`\includepdf`调用位置已经搭好，等文件一到可以直接插入。

**过程中的插曲**：本机磁盘一度严重不足（377Mi可用/926Gi，99%已用），导致`brew install pandoc`失败，也让`osascript`驱动Word导出PDF超时失败（"AppleEvent timed out"）。没有继续重试或强制退出Word（怕影响她其他未保存的文档），只是把这个风险明确报告给她。会话过程中磁盘空间回升到4.6Gi可用，可能是她自己清理了，也可能是波动——不能假设已经彻底解决。

### Combined Interface —— 框架搭建完成

新文件：`data/processed/combined/d3/combined_interface.html`。做法：不是重新实现六套渲染逻辑，而是把六个现成的canonical HTML（未做任何修改）用`<iframe>`嵌入一个统一的导航外壳里，一次只显示一个iframe。外壳提供：
- 顶部两个方向的tab（Fingerprints / Topology）
- 左侧面板：切换方向内的三个子可视化（radio-button风格）
- 主视图：对应的iframe
- 右侧detail面板：说明每个子可视化自己已经有效的hover/click详情面板，外层共享的detail面板是后续工作

原计划里的两项——作者选择器/参数滑块、跨视图联动（选中一个作者时另一个方向同步高亮其地名）——用虚线边框+"planned"标签明确标注为未实现，不做假装能用的占位符（半成品交互比明显标注"未实现"更容易误导人）。已确认规模探索阶段生成的四份JSON（`all_authors_radar.json`/`all_authors_network.json`/`all_authors_barcode.json`/`all_authors_small_multiples.json`）已经包含任意作者子集（最多全部424位）的实时可算数据，是未来接入作者选择器时的现成数据源；metro图因为社群检测是离线批处理，计划改成在几个预生成的快照（5/20/50作者）之间切换，不做实时重算。

浏览器测试：方向tab切换、子可视化切换、六个iframe各自渲染正常（radar/barcode/network/metro截图均确认交互正常），控制台无报错。根目录`index.html`底部加了一条链接指向这个框架页。

论文`\section{Combined Interface}`（`\label{sec:combined-interface}`）已从纯TODO注释改写成实际描述，说明了iframe方案的取舍、两项"planned"功能延后的理由、以及后续实现路径。

---

## 16b. 同日会话追加：作者选择器 + 跨视图联动接入（Merritt要求"把剩下两项接进去"）

Merritt在框架搭建完成后紧接着要求把之前标为"planned"的两项——作者选择器、跨视图联动——真正接进Combined Interface，不再是占位符。

### 做法：从iframe换成同页面实时渲染（metro除外）

新增build脚本`data/processed/combined/py/build_combined_interface.py`，覆盖重写了`combined_interface.html`（之前的iframe版本被完全替换，不是增量修改）。核心变化：
- radar、barcode、small_multiples、network、linear **五个图不再用iframe**，改成直接在同一个页面里用D3/Leaflet实时渲染，全部读同一个共享的`selectedAuthors`数组。渲染逻辑是从`scale_exploration/d3/`里对应的五个探索工具（`radar_scale_explore.html`等）搬过来的——**没有重新发明**，是把已经在规模探索阶段测试过的client-side计算逻辑（每作者取top15地名→document级别共现）原样复用，只是把"各自独立的`selected`变量"统一成一个共享变量。
- **metro保持iframe**，因为社群检测是Python离线批处理，没法在浏览器里按键实时跑。做法：根据当前选中作者数量，在两个预生成快照之间切换iframe的`src`——≤10人显示`dir_2/metro/d3/metro.html`（正式版5作者），>10人显示`scale_exploration/d3/metro_scale_explore_20authors.html`（20作者快照）。界面上明确写清楚这个限制，不假装metro也在实时联动。
- 作者选择器：预设按钮2/5（默认）/20/50 + 搜索框自由加人 + 移除chip，跟规模探索工具同一套UI模式，放在左侧共享面板，不是每个图各自一份。
- 跨视图联动：加了一个共享的`focusedAuthor`变量。在Fingerprints任一视图里点击某个作者的图形（radar的多边形/barcode的整行/small_multiples的整个面板），会切换该作者的focus状态（金色高亮，其余变暗）；切到Topology任一视图（network/linear）时，会临时计算这个作者自己的top15地名集合，把当前选择组合图里匹配的节点/边染成金色、其余变暗——这正是原计划里"选中一个作者时另一个方向同步高亮其地名"的字面实现。左侧面板始终显示当前focus状态（chip+清除按钮），换方向、换图时这个状态是持续的。

### 数据校验

用四份数据集之前就确认过（本节前半段第16节记录）：radar/barcode/small_multiples三份的408位作者名单完全一致，跟network数据集的作者名单也完全一致（Python逐一比对`set`相等，无差异）——这保证了同一个`selectedAuthors`数组能在四个不同数据集之间无缝查找，不会出现"在这个图里能找到这个作者，换个图就查不到"的问题。

### 浏览器测试（实际操作验证，非假设）

- 默认5作者radar正常渲染；点击某个作者多边形后金色高亮生效，其余多边形变暗
- 切到Topology→Network：状态文字确认"highlighting Alexander McCall Smith's places"，截图确认该作者的地名节点/边渲染成金色，其余灰色变暗——**跨视图联动实际生效**，不是文字描述
- 切到Linear：同样的金色高亮逻辑正确生效
- 切到Metro，选中人数从5改成20：`metro-note`文字从"showing canonical 5-author map"变成"showing 20-author snapshot"，iframe src确认切换——快照阈值逻辑正确
- 切回Fingerprints→Barcode/Small Multiples：focus状态（金色边框+其余变暗）在两个视图之间都正确保持
- 搜索框输入"Muriel"→建议列表正确弹出"Muriel Spark"→点击后正确加入选择
- 全程刷新页面测试冷启动（默认5作者、无focus），控制台全程无报错

### 论文改动

`\section{Combined Interface}`第二次改写：从"两项功能待续、标注planned"改成描述实际实现——共享`selectedAuthors`+`focusedAuthor`状态、五图复用规模探索的计算逻辑、metro维持iframe快照切换并在界面上如实说明限制、唯一还没做的是跨图共享的原文句子detail面板（各图已有自己的hover detail，这个是"锦上添花"而非"功能缺口"）。

---

*文档生成时间：2026年7月11日（第16、16b节新增，其余章节沿用7月10日版本）*
*项目状态：六个D3可视化的核心待办全部清空，六个图的规模探索全部完成并已写入论文；Combined Interface的作者选择器和跨视图联动已实际接入并测试通过（metro维持快照切换，未做实时联动）；伦理日期/Acknowledgements/Abstract v1/Conclusion RQ2/Task&Survey Questions均已完成；PIS/Consent Form插入仍阻塞（等待Merritt提供个人化版本）；用户调研相关内容按Merritt指示暂缓，下周针对性开始*
