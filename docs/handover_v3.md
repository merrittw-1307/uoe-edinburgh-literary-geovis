# 项目完整迁移说明文档 v3
## A Visual Trace Map of Edinburgh Place Names in Literature
### MSc Dissertation — Merritt Wang (S2887338)
### University of Edinburgh, School of Informatics, 2025–2026
### 生成时间：2026年7月10日（本文档取代 handover_v2.md，v2继续保留作历史存档）

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

### 第二优先级：扩大规模探索（未开始）
- 5作者→全部424作者
- 只选2个作者/2-3本书的变化
- 截图记录pros/cons

### 第三优先级：Live Links（未开始）
- GitHub Pages部署

### 第四优先级：Combined Interface（未开始）

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

*文档生成时间：2026年7月10日*
*项目状态：六个D3可视化的核心待办全部清空，metro.html完成方法论级重建；论文的metro相关章节尚未同步更新（下一步工作）；用户调研仍未启动*
