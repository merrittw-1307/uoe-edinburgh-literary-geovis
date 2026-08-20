# 项目记录:A Visual Trace Map of Edinburgh Place Names in Literature

**作者**:Merritt Wang (S2887338)
**学位**:MSc, School of Informatics, University of Edinburgh
**导师**:Dr. Uta Hinrichs
**仓库**:`github.com/merrittw-1307/uoe-edinburgh-literary-geovis`
**提交时间**:2026-08-20 23:39:18(截止时间为2026-08-21中午12:00,提前12小时完成)
**提交回执号**:`20268597CEDFD62E71A0EAB24985D1692C8C67B1`

> **说明**:项目真正的起点是2026年3月导师发布的项目brief,比git仓库建立(7月1日)早了约3个多月。这一早期阶段(选题、设计草图、需求讨论)是在其他对话窗口/会话中完成的,不在本次对话的可见范围内——以下"阶段零"和"阶段一(前半)"是基于仓库里留存的文件(`proposal/`、`report/session_reports/`等,均带原始创建日期)重建的,不是我亲历的记录;7月10日之后的部分则同时基于git提交历史与本次对话内容整理,更完整可靠。

---

## 一、项目周期与工作量总览

| 指标 | 数值 |
|---|---|
| 项目真实起点 | 2026-03-23(导师发布项目brief)—— 距提交约 **5个月** |
| Git仓库跨度 | 2026-07-01 至 2026-08-20,共 **51天**(实际编码/写作阶段) |
| Git提交总数 | **84次** |
| 核心开发/写作强度较高的天 | 8/4(16次)、8/5(20次)、8/9(10次)、8/20(19次,含最后冲刺) |
| 追踪代码文件总数 | 188个 |
| Python代码 | 41个文件,约 **6,572行** |
| D3.js/HTML可视化文件 | 24个文件,约 **7,609行** |
| 代码总行数(py+html+js+tex) | 约 **16,043行** |
| 仓库追踪内容总大小 | 约60MB(不含被gitignore的145MB原始SQL dump) |
| 论文正文(dissertation.tex) | 793行LaTeX源码,约 **13,800词**(粗略统计,不含公式/命令) |
| 论文最终页数 | 正文40页(含8章)+ 参考文献(19条)+ 附录(Study Material、Data and Implementation) |
| 自动化测试 | 4个pytest测试文件,验证发布数据与论文陈述的一致性,接入CI |

---

## 二、项目背景与核心问题

**研究问题**:
- **RQ1(作者空间指纹)**:一个作者在爱丁堡各区域的地名提及分布,能否可视化为可识别的"空间指纹"?
- **RQ2(叙事拓扑)**:文学作品中地名的共现关系,能否揭示出一种区别于地理拓扑的"叙事拓扑"?

**数据基础**:LitLong Edinburgh数据库(Palimpsest项目,University of Edinburgh)——620部文学作品(1687–2015)、2,135个地名、50,248条地名提及记录、424位作者。

**六个可视化原型**:
- Direction 1(作者空间指纹):Radar chart(主)、Bar-code fingerprint(次)、Small multiples(第三)
- Direction 2(叙事拓扑网络):Force-directed network(主)、Linear connection diagram(次)、Metro-style map(示意)

---

## 三、完整时间线(从零到完成)

### 阶段零:选题与设计构思(2026-03-23 ~ 2026-06-24,git仓库建立之前)

*以下基于`proposal/`和`report/session_reports/`目录下带时间戳的文件重建,细节可能不全。*

- **2026-03-23**:导师Uta Hinrichs在DPMT(Degree Project Management Tool)发布项目brief"A Visual Trace Map of Edinburgh Place Names in Literature"——核心目标是设计抽象化的静态/交互地图,追踪爱丁堡地名在文学作品中出现的顺序与共现关系,明确要求"decidedly move away from mapping location mentions to geographical maps",并以伦敦地铁图为设计灵感来源之一(`proposal/brief/TraceMapEdinburgh_project.pdf`)。该项目当时有10名学生感兴趣,容量上限3人。
- **2026-04-02**:确定选题意向(`proposal/brief/ProjectIdea.pdf/docx`)。
- **2026-04-14**:提交正式的IPP(Informatics Project Proposal,`proposal/IPP_Proposal_S2887338.pdf`)。
- **2026-06-24**:产出首份设计草图报告(`report/session_reports/24Jun.pdf`)——针对两个方向各设计4个候选方案(共8个):Direction 1(作者空间指纹)候选为Radar chart、Small multiples、Geographic density map、Bar-code fingerprint;Direction 2(叙事拓扑网络)候选为Force-directed network、Metro-map topology、Chord diagram、Adjacency matrix heatmap。每个候选都标注了目标人群(domain experts / general public / general)、优势与风险,并规划了"专家+大众"两组用户研究的雏形思路。这是最终六个设计(从八个候选中筛掉Geographic density map与Chord diagram/Adjacency matrix中的一个,经Uta反馈后用Linear connection diagram替代chord diagram)的直接前身。
- **2026-06-30 ~ 07-01**:继续设计推进(`report/session_reports/1Jul.html`,含中英双语版本),同日仓库正式建立,项目从"设计讨论"转入"工程实现"阶段。

### 阶段一:数据管道搭建(2026-07-01)
- 从`/tmp`整理出Python原型脚本,正式建仓
- 排除145MB原始SQL文件的git追踪(改用CSV/衍生数据)
- 完成PostgreSQL数据库导入、`api_sentence`/`api_locationmention`等核心表梳理

### 阶段二:六个可视化原型开发(2026-07-10 ~ 07-11)
- 完成官方14分区(Sector)分类v2,六个D3可视化接入真实数据交互
- Metro地图从"手绘八线"重建为"数据驱动的叙事拓扑"(社区发现算法)
- 搭建Scale Exploration(2/5/20/50/408作者规模测试)工具
- 论文初稿第1-7章草稿成型
- 搭建Combined Interface框架雏形(共享作者选择器 + 跨视图联动 + 统一详情面板)

**7月10日的中期状态快照**(`report/session_reports/10Jul_project_status.html`,当时距截止还有42天):六个可视化设计与交互已100%完成,规模探索6/6完成,论文章节5/7基本完成;但**用户研究进度为0%**,被明确标记为"最大风险"("招募+跑session+分析都需要不可压缩的时间,但目前排在优先级列表最后一位");Combined Interface当时还只是"第四优先级、尚未开始"的待办事项。事后看,这份快照相当准确地预判了后续一个月的工作重心——Combined Interface(8月4-5日)和用户研究(8月9日设计、8月9-19日执行)确实是压哨完成的两大块。

### 阶段三:Combined Interface打磨与首次导师评审(2026-08-04 ~ 08-05,高强度阶段)
- 修复大规模作者数下的性能瓶颈(力导向图卡顿、颜色冲突、bar-code渲染为0px高度等三个真实bug,均通过实测发现)
- 论文补齐8张缺失的插图(此前`\listoffigures`列了标题但正文零图片)
- 根据Uta Hinrichs第一轮UX反馈,对Combined Interface做整体重构
- 补充色觉无障碍检测(protanopia/deuteranopia/tritanopia模拟)
- 加入pytest测试套件,验证发布数据与论文陈述的一致性,接入CI
- 完成端到端项目时间线文档、Qualtrics问卷搭建指南

### 阶段四:用户研究工具设计与打磨(2026-08-09,高强度阶段)
- 重新设计Fingerprint任务为"study-then-identify"结构(而非冷猜),关闭两个记忆/作弊漏洞
- 加入F0理解力检查题,区分"读懂编码"与"单纯认出图形"
- 加入五选五匹配任务(M1/M2),构建完整5×5混淆矩阵
- 制作盲测单作者刺激材料,归档Qualtrics QSF备份

### 阶段五:用户研究执行(2026-08-09 ~ 08-19)
- 分发Qualtrics问卷,回收16份原始回复
- 期间持续维护README与时间估算等文档准确性

### 阶段六:数据分析与论文冲刺(2026-08-20,全天高强度)
1. **数据分析**:排除3份低质量回复(n=13),完成第5/6/7章(方法、结果、讨论)结果部分
2. **仓库整理**:清理提交材料、扩充参考文献、核查合规性,首次尝试压缩至40页限制
3. **安全修复**:发现并移除`directus.sql`中泄露的第三方管理员凭证(已暴露约7周),purge出git追踪
4. **逐条处理导师Overleaf评论**(本次对话主要内容,数十条批注):
   - 图表说明文字位置、Design章节结构、数据探索发现(Finding 1-5)措辞修正
   - 六个可视化分别配上"交互状态"截图(而非仅静态总览图),用Playwright脚本精确截取
   - Combined Interface补充5张(后精简为3张)功能截图,覆盖跨视图联动、详情面板、Metro例外机制等
   - 章节级重组:新增独立的"Data and Data Preparation"章节(原Implementation章节数据管道部分独立成章,置于Design之前);Implementation技术细节并入Design对应设计段落,消除内容重复
   - 修复多处LaTeX编译隐患:`wasysym`/`amsmath`加载顺序冲突、公式`\text{}`缺失宏包、长代码标识符/URL溢出页边距
   - 补充NetworkX、Leaflet.js、CartoDB等技术引用,新增文献条目(19条)
   - 加入"Generative AI Use"学术诚信声明
5. **压缩至40页**:通过精简冗余表述、图片尺寸调整、章节合并,将正文从45页压缩至精确40页(卡线不超)
6. **全篇复核**:基于真实Overleaf编译PDF逐页人工核查70页全文,发现并修复2处真实排版bug(长标识符/URL溢出页边距导致文字被截断)
7. **生成提交材料**:通过`git archive`打包完整代码仓库 + 手动补充被gitignore的原始SQL dump,生成70MB的`submission/....zip`及最终PDF
8. **正式提交**:23:39:18通过University of Edinburgh官方Project Submission系统提交,获得回执

---

## 四、关键技术决策

- **可视化技术选型**:D3.js(项目brief指定),因其对视觉编码的精细控制、无需安装部署、数字人文领域广泛使用
- **空间分类方案**:放弃地名个体作为坐标轴(因作者间地名重叠度极低,仅18个地名被两位以上作者共享),改用14个官方城市分区(Neighbourhood Partnership Areas + Natural Neighbourhoods,Open Government Licence v3.0数据源)作为雷达图轴
- **共现粒度选择**:句子级共现在数据结构上不可行(`api_sentence`表实际是"每条提及一行"而非"每个真实句子一行"的构造性artifact);页面级共现过密(单页最多92个共现地名);最终采用文档级共现(403对,权重≥2)
- **Metro地图重设计**:从人工绘制(22%的相邻站点由真实共现支撑)重建为基于modularity社区发现算法的数据驱动版本(88%的相邻站点由真实共现支撑),包含完整6步流程(社区发现→站点排序→换乘检测→线路命名→力导向布局→八边形走线修正)
- **章节结构**(经导师多轮反馈迭代):Introduction → Literature Review → **Data and Data Preparation**(独立成章)→ **Design**(含六设计的原理+实现细节合并呈现)→ Implementation(仅保留技术约束与Combined Interface)→ Evaluation → Discussion → Conclusion

---

## 五、用户研究结果摘要(n=13,3份低质量回复已排除)

**RQ1(空间指纹可识别性)**:部分成立。Radar chart在所有客观指标上均优于另外两个设计——五选五匹配准确率69%(20%概率基线),最相似一对作者的区分准确率85%。Bar-code与Small multiples матching准确率分别为48%和49%。

**RQ2(叙事拓扑vs地理拓扑)**:成立。最强共现地名对Leith与Princes Street(28部作品共同出现),两地地理距离约2.5公里,是"叙事邻近性不反映空间邻近性"的最清晰实证。Metro地图重设计将这一发现从单一实例扩展为系统性内部一致性验证(22%→88%)。

**一个有趣的张力**:Metro地图在"最强连接对识别"任务上准确率最低(15%,另两个设计均为69%),但在赛后排名和"最难忘设计"投票中却是绝对第一(7/13票)——说明其借用的地铁图视觉语言带来的是"导航自信感"而非"单条边的精确检索能力"。

---

## 六、遗留与未来工作(取自Conclusion章节)

- 更快的客户端近似聚类算法,让Metro地图摆脱"预计算快照"限制,实现真正的实时联动
- 六个视图统一为单一共享详情面板(目前Combined Interface的详情面板与各独立视图各自为政)
- 利用`api_posmention`的词性标注做"叙事权重分析"(对话vs叙述vs描写)
- "文学沉默地图"(Literary silences map)——分析语料库中从未被提及的爱丁堡地点
- Reader-plot时间线可视化(利用已建好但未启用的`position_pct`字段)

---

*本记录生成于提交后。阶段零及阶段一前半基于仓库内带时间戳的文件(`proposal/`、`report/session_reports/`)重建,早期设计讨论的具体过程不在可见范围内;7月10日之后的部分基于完整git提交历史(84次提交)与本次对话记录整理,用于项目复盘与后续参考。*
