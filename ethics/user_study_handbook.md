# 用户调研完整执行手册 / Complete User Study Execution Handbook

**项目 / Project:** A Visual Trace Map of Edinburgh Place Names in Literature
**研究者 / Researcher:** Merritt Wang (S2887338)
**伦理审批号 / Ethics reference:** 446635（审批日期 / Approved: 13 May 2026）
**文档目的 / Purpose of this document:** 一份可以直接照做的完整调研执行方案，中英双语，供你自己查阅、也可以把问卷部分的英文原文直接搬进Qualtrics。/ A fully self-contained, ready-to-execute study plan. Chinese sections are for your own reference; the English question wording is what participants will actually see and can be copy-pasted directly into Qualtrics.

---

## 目录 / Table of Contents

0. 总览 Overview
1. 招募方案 Recruitment Plan
2. 材料清单 Materials Checklist
3. 完整问卷内容（可直接导入Qualtrics）Full Questionnaire (Qualtrics-ready)
4. 搭建与发布流程 SOP Step-by-Step
5. 数据收集与清理 Data Collection & Cleaning
6. 分析方案 Analysis Plan
7. 结果如何填回论文 Mapping Results to the Dissertation
8. 时间线建议 Suggested Timeline
9. 风险与注意事项 Risks & Reminders

---

## 0. 总览 / Overview

### 中文

本研究评估六个可视化原型（三个"作者指纹"设计 + 三个"叙事拓扑"设计）是否能让人：
- **RQ1**：先自主观察5位作者都标名字的参考图、总结出规律，再看一张去掉名字的单作者图，能不能凭学到的规律认出是哪位作者（2026年8月9日之前的版本是让参与者完全凭空瞎猜、没有任何参照，这样对不了解这几位作者的人毫无意义，已经改成"先学后测"）
- **RQ2**：从共现关系图里自发判断出"叙事关系强的两个地方"未必"地理上近"

研究采用**在线、无主持人、自助式**问卷形式（Qualtrics），参与者按自己的节奏完成，全程约35-50分钟。这个格式已经写进PIS，不能中途改成有主持人的访谈形式（会跟已批准的伦理描述不符）。

### English

This study evaluates whether the six visualisation prototypes (three "author fingerprint" designs, three "narrative topology" designs) allow participants to:
- **RQ1**: after studying a labelled reference view showing all five authors' fingerprints and forming their own impression of how the patterns differ, identify which author a single unlabelled fingerprint represents (the pre-9 August 2026 version asked participants to guess with no reference at all, which is meaningless for anyone unfamiliar with these five authors specifically; the task now tests whether the visual pattern is learnable and recognisable, not prior literary knowledge)
- **RQ2**: spontaneously recognise, from a co-occurrence visualisation, that two narratively-connected places need not be geographically close

The study is **online, unmoderated, self-paced** (Qualtrics), taking approximately 35–50 minutes per participant. This format is already specified in the approved PIS and should not be changed to a moderated interview format without a fresh ethics amendment.

---

## 1. 招募方案 / Recruitment Plan

### 中文

**两组人，各自招募标准（PIS里已经写明，招募时不用额外解释）：**

| 组别 | 定义 | 建议人数 | 招募渠道 |
|---|---|---|---|
| 专家组 Domain experts | 文学研究者、数字人文学者、对爱丁堡文学地理熟悉的人 | 5–8人 | 英文系/数字人文系师生、爱丁堡文学类读书会、LitLong项目组本身、你的导师Uta Hinrichs可能认识的相关学者 |
| 大众组 General public | 无专业背景，可以完全不了解爱丁堡文学 | 8–12人 | 朋友圈、同学网络、Informatics系内非文学背景的同学、社交媒体（注意：分组是问卷里的自我描述决定的，不是招募时候贴标签分组，见下方问卷第3题设计说明） |

**总数建议：13–20人。** 不是为了统计显著性，是为了拿到有代表性的准确率趋势+足够丰富的质性材料（自由文本回答）。

**招募文案怎么发**：直接发下面英文模板（参与者是英语环境，招募信息必须用英文），附上：
1. PIS文件（`ethics/PIS_Merritt_final.docx`转的PDF，即`dissertation/5Aug/pis.pdf`——注意用这个日期文件夹，`4Aug/`那份还是旧版30-40分钟时长，没同步最新问卷）
2. Qualtrics问卷链接（下面第4节教你怎么生成）

### English — Recruitment message template (send this, in English, via email/social media/etc.)

> **Subject: Participants needed — 35-50 min online study on visualising Edinburgh literature (MSc research, Informatics)**
>
> Hi [Name],
>
> I'm running a short online study as part of my MSc dissertation at the University of Edinburgh, School of Informatics, supervised by Dr Uta Hinrichs. The study looks at different ways of visualising place names in Edinburgh-related literature, and takes about 35–50 minutes.
>
> You'll look at a few visualisations and answer some simple questions about what you see — no prior knowledge of Edinburgh literature is required. The study is entirely online and self-paced; you can do it whenever suits you.
>
> Full details are in the attached Participant Information Sheet. If you're happy to take part, please read it and then use this link to start: [QUALTRICS LINK]
>
> This project has ethics approval from the Informatics Research Ethics Committee (reference 446635).
>
> Thanks so much — happy to answer any questions first if useful.
>
> Merritt

---

## 2. 材料清单 / Materials Checklist

全部已经就绪，无需重做，直接用：

| 材料 | 状态 | 路径 |
|---|---|---|
| Participant Information Sheet（35-50分钟版） | ✅ 已定稿 | `ethics/PIS_Merritt_final.docx`（PDF版：`dissertation/5Aug/pis.pdf`） |
| Consent Form | ✅ 已定稿 | `ethics/Consent_Merritt_final.docx`（PDF版：`dissertation/5Aug/consent.pdf`） |
| **完整问卷（逐屏，可直接照抄进Qualtrics）** | ✅ 已定稿 | **`ethics/user_study_questionnaire.md`** |
| Task/Survey Questions 措辞同步版 | ✅ 已定稿（论文Appendix A） | `dissertation/5Aug/dissertation.tex` 搜索 `\section{Task Questions}` / `\section{Survey Questions}` |
| 六个可视化的公开链接 | ✅ 已上线并实测 | https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ |
| 本手册（招募方案+流程SOP+分析方案） | ✅ 本文档 | `ethics/user_study_handbook.md` |

**你还需要准备的只有一件事**：注册/登录Qualtrics（爱丁堡大学学生有机构账号，登录 https://ed.qualtrics.com），把 `ethics/user_study_questionnaire.md` 里的内容录入进去。

**关于"Combined Interface"（整合界面）——它不是问卷材料，不要发给参与者：**

中文：项目里还有一个`combined_interface.html`（整合界面，https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/combined/d3/combined_interface.html ），把六个设计放进同一个页面、支持自由切换作者（含2026年8月新增的"全部408位作者"大规模探索选项）、跨图联动高亮。**这是给导师看的演示/汇报工具，不是正式问卷材料**——正式问卷里Fingerprint任务用的是两组固定链接（Step 1参考版：5位作者都标名字的标准页面；Step 2盲测版：单作者、不标名字的专用页面，见`ethics/study_stimuli/`），Topology任务用三个标准页面，全部都不带"自由切换到任意作者"这种功能，这样才能保证RQ1的实验条件不被破坏——参与者只能在我们规定的"先看哪5个人、再猜哪一个"这个范围内操作，不能自己跳出去看任何其他作者的数据。给导师发材料时可以两个链接都发（问卷链接+Combined Interface链接），但发给正式参与者的招募邮件/问卷Welcome页只应该包含Qualtrics问卷链接，不要额外附上Combined Interface链接，避免参与者提前看到其他作者的数据而影响判断。

English: The project also has a `combined_interface.html` ("Combined Interface", https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/combined/d3/combined_interface.html ) that puts all six designs on one page with free author-switching (including an "All 408 authors" large-scale-exploration preset added in August 2026) and cross-view highlighting. **This is a supervisor-facing demo/review tool, not part of the formal study instrument.** The Fingerprint tasks in the actual questionnaire use two fixed link sets instead (Step 1 reference: the standard all-five-labelled page; Step 2 blind: a single-author, no-name page built specifically for this task, in `ethics/study_stimuli/`), and the Topology tasks use the three standard pages — none of them let a participant freely switch to see any other author's data. Combined Interface's free-switching would break that boundary. It's fine to send both links to your supervisor, but the recruitment email / questionnaire Welcome screen sent to actual participants should only ever contain the Qualtrics link, not the Combined Interface link.

---

## 3. 完整问卷内容 / Full Questionnaire

**问卷已经拆分成独立文档，见 `ethics/user_study_questionnaire.md`** —— 那份文档是唯一的问卷正本，逐屏排列、可以直接照抄进Qualtrics，并且已经跟论文 `dissertation/5Aug/dissertation.tex` 的 Appendix A（Task Questions / Survey Questions）保持完全同步。本手册不再重复问卷全文，避免两处内容不一致。

**这一版问卷相比最初的Appendix A草稿，做了一次针对性加深（回应"希望被试自发发现地名共现关系"的要求）：**
- Task 2（拓扑任务）每个设计新增两题：**T3**（"除了最强的那对，还有没有哪个连接让你意外？"）和**T4**（"有没有看到3个以上地方好像是一伙的？"）——这两题不设标准答案，专门用来捕捉自发的深度观察。
- 三个拓扑设计全部看完后，新增一道**Cross-design synthesis**问题："看完这三种方式后，关于爱丁堡文学地理，有没有什么让你意外的发现？"——这是全份问卷里对RQ2最关键的一题。
- Task 1和Task 2都新增了"自解释性"量化题（如果没人跟你解释，你能不能单看图就看懂），把论文Study Design里"cold presentation测试自解释性"这个方法论直接量化出来。
- 背景问卷新增"是否住过/去过爱丁堡"一题，把"熟悉这座城市"和"熟悉这座城市的文学"拆成两个独立变量。
- 反思部分新增"六个里你印象最深的是哪个"一题。

**预计用时因此从30-40分钟调整为35-50分钟**，PIS文件（`ethics/PIS_Merritt_final.docx`及对应PDF）已经同步改过这个数字，不需要你再手动改。

**详见 `ethics/user_study_questionnaire.md`**，里面还附了六个可视化的完整链接表和题目数量统计。

---

## 4. 搭建与发布流程 / Setup & Publishing SOP

**逐block、逐题的完整操作手册（可直接照抄）见 [`ethics/qualtrics_build_guide.md`](qualtrics_build_guide.md)**——里面精确到每个block选什么Question Type、粘贴什么文字、开不开Force Response、链接放在哪。下面这节是精简版流程概览。

### 中文步骤

1. **登录Qualtrics**：https://ed.qualtrics.com ，用爱丁堡大学账号登录（机构账号，免费）。
2. **新建调查**：Create a new project → Survey → From scratch。
3. **按build guide顺序建16个Block**：Welcome、Consent（4道独立必答题）、Background、Fingerprint说明、三个指纹任务block（每个内部是"参考版链接→Page Break→盲测版链接+F1-F4"）、排名、拓扑说明、三个拓扑任务block、排名、反思、结束语。
4. **Consent不用Skip Logic**：4道题都设成Force Response必答，没勾选就点不了下一页，效果等同"没同意就不能继续"，不需要额外配置跳转逻辑。
5. **设置随机化**：进入 Survey Flow（左侧菜单）→ 把三个指纹任务block拖进一个"Randomizer"元素，勾选"Randomly present X of Y elements"设为3（即全部随机顺序展示）→ 对三个拓扑任务block重复同样操作。
6. **插入可视化链接**：**具体每个block放哪个链接、Fingerprint为什么要放两个链接（参考版+盲测版），必须照`qualtrics_build_guide.md`第5节来，这里不再重复列表，避免两处链接不一致**。Topology三个block用原版链接（network.html/linear.html/metro.html）即可，同样详见build guide。全部链接建议设置成"在新标签页打开"（Qualtrics里可以用富文本编辑器插入`<a href="..." target="_blank">`)。
7. **预览测试**：自己先完整走一遍（Qualtrics有Preview功能），确认链接能打开（Fingerprint的参考版要看到5人、盲测版要看到1人无名字）、随机化生效、Consent不勾选点不了下一页。
8. **发布**：点击"Publish"，生成的匿名链接就是发给参与者的问卷链接。
9. **收集期设置**：可以在Survey Options里设置一个自动关闭日期（比如发布后7天自动停止收集）。

### English quick-reference

1. Log in at ed.qualtrics.com with your University of Edinburgh account.
2. Create Survey → From scratch.
3. Build all 16 blocks per the build guide (each Fingerprint block internally has "reference link → page break → blind link + F1-F4").
4. Consent needs no Skip Logic: make all four checkboxes Force Response, which alone prevents proceeding without agreeing.
5. Use Survey Flow → Randomizer around the three fingerprint task blocks (present all 3, randomised), and again around the three topology task blocks.
6. **Follow `qualtrics_build_guide.md` Section 5 for exactly which link(s) go in each block** — Fingerprint blocks need both a reference (labelled, all five authors) and a blind (single author, no name) link; this file no longer duplicates that table, to avoid the two documents drifting out of sync with each other.
7. Preview and test the full flow yourself before publishing.
8. Publish → distribute the anonymous link.
9. Set an auto-close date under Survey Options if you want a hard cutoff.

---

## 5. 数据收集与清理 / Data Collection & Cleaning

### 中文

- **收集窗口建议**：开放7天左右，招募信息发出后前3天通常是响应高峰。
- **撤回期**：PIS里写的是"7天内可撤回"，所以问卷关闭后再等7天，才把数据当作"定稿"用于分析——这期间如果有人发邮件要求撤回，把对应的Response ID从数据集里删除（Qualtrics按Response ID区分每份提交，不含姓名，符合匿名化承诺）。
- **数据导出**：Qualtrics → Data & Analysis → Export & Import → Export Data → 选CSV格式。
- **清理**：删除测试期间你自己预览产生的记录（Qualtrics导出里通常标记为"Preview"或者可以通过完成时间异常短的记录识别）；检查是否有完全没做任务只跳到最后的记录（可以清除）。

### English

- Keep the survey open ~7 days.
- Wait a further 7 days after closing (matching the PIS withdrawal window) before treating the dataset as final.
- Export via Data & Analysis → Export & Import → CSV.
- Remove your own preview/test responses and any incomplete straight-throughs before analysis.

---

## 6. 分析方案 / Analysis Plan

### 中文：每个数字具体怎么算

**RQ1 — 指纹识别准确率**
- 对每个设计（radar/barcode/small multiples），准确率 = 答对人数 ÷ 该设计总作答人数
- 平均置信度 = 该设计所有置信度评分的平均值（1-5分）
- ➕新增的"自解释性"题：算出每个设计"Yes, easily"的比例
- 用Excel/Google Sheets做透视表（按设计分组）就够了，不需要统计软件
- **2026年8月9日后的重要提醒**：现在Fingerprint任务是"先看5人都标名字的参考版、自主总结规律，再看盲测版尝试识别"，不再是完全凭空瞎猜——所以整体准确率大概率会比"纯冷启动"设计高不少（这是预期之内、也是我们想要的，因为现在测的是"图形能不能被学会认出来"，不是"图形本身够不够有名"）。写进论文的时候不要拿这个准确率跟一个假设的"随机瞎猜20%基线"简单对比，而要强调：如果准确率明显高于20%，说明参与者确实从参考版里学到了可迁移的视觉特征；如果某个设计的准确率明显低于其他两个，说明这个设计的"可学习性"不如另外两个——这才是三个设计之间真正可比的地方。

**RQ1 — 质性编码**
- 把每个设计的F3自由文本（"具体是什么形状特征让你这样判断"）导出，通读一遍，标记重复出现的主题（比如"提到了某个方向的尖峰""提到了分布均匀/集中""说自己是瞎猜的"），数一下每个主题出现的次数——这里尤其要留意有没有人明确提到"我记得参考图里这个作者是这样的"这类说法，这直接证明了参考版确实被使用、确实起到了作用

**RQ2 — 最核心的数字（T1/T2题）**
- 对每个拓扑设计，把参与者填的"两个地方"与该数据集里真实权重最高的一对（比如network/linear是Leith & Princes Street，metro看具体是哪条线的哪一对）比对，算"识别正确率"
- **在识别正确的人里**，看有多少人同时选了"远/较远"——这个百分比就是RQ2最直接的证据
- 按第3步分组（专家 vs 大众）交叉对比上面所有数字

**RQ2 — 深度发现（T3/T4/Cross-design synthesis，这是这次加深的重点，分析方法如下）**
- **T3（意外的连接）**：把每个设计下所有参与者写的"地名对+意外原因"列成一张表，人工判断这个连接是否跟数据里真实的高权重共现边吻合（可以对照`data/processed/dir_2/network/data/network_enriched.json`里的edges列表核实权重）——如果多个参与者独立提到同一对地名，这是很强的证据，可以直接引用"3位参与者独立注意到X和Y的连接出乎意料"这样的句子
- **T4（自发发现群组/cluster）**：这是验证社群检测方法本身是否work的关键题。把参与者说的"这几个地方好像是一伙的"跟`metro.html`实际的线路分组（或network的力导向布局里视觉上聚在一起的节点）对比——**如果参与者在完全不知道"community detection"这个概念的情况下，独立说出了跟算法分组高度重合的一组地名，这是对整个方法论最有力的独立验证**，比任何准确率数字都有分量，务必在Discussion里重点讨论
- **Cross-design synthesis**：这题的自由文本通读一遍，看有没有反复出现的"顿悟时刻"（比如好几个人都提到"没想到A和B有关系"），这是最适合直接摘录进Conclusion或Discussion开头的材料，比统计数字更能体现RQ2"叙事关系≠地理关系"这个论点是否真的被参与者感知到了
- 按第3步分组（专家 vs 大众）交叉对比：专家组是否比大众组更容易在T4里说出"正确"的分组？这本身就是一个值得讨论的发现

**排名投票**：直接数票数，做成一个简单的柱状图或表格

**质性材料汇总**：反思问卷的4+1题，通读后挑3-5条最有代表性的引用，直接摘录进Discussion章节（记得匿名化，用"P3""P7"这样的编号代替任何身份信息）

### English summary

- Accuracy = correct / total responses, per design (Excel pivot table is sufficient, no stats software needed)
- Mean confidence per design
- Self-explanatoriness: % "Yes, easily" per design
- RQ2 core metric: among participants who correctly identified the strongest pair, % who judged it geographically far
- RQ2 deep-insight items (T3/T4/synthesis): manually cross-check reported "surprising connections" and "clusters" against the real edge weights and metro line groupings — independent agreement between a participant's unprompted cluster and the algorithm's community-detection output is the strongest possible validation of the method, stronger than any accuracy number, and should be a headline point in the Discussion chapter if it occurs
- Cross-tabulate all of the above by expert vs. general-public (from background Q3)
- Thematic coding: read all free-text responses once, tag recurring themes, count frequency
- Pull 3-5 representative anonymised quotes (labelled P1, P2, ...) for the Discussion chapter

---

## 7. 结果如何填回论文 / Mapping Results to the Dissertation

| 分析产出 | 填入论文哪里 |
|---|---|
| 各设计准确率、置信度、自解释性比例表 | Ch5 §Results |
| 参与者人数、分组、背景描述统计 | Ch5 §Participants |
| Qualtrics流程本身的描述（本手册第4节的精简版） | Ch5 §Study Procedure |
| RQ1/RQ2数字的解读、专家vs大众对比 | Ch5 §Discussion of Results |
| "有什么confusing/想改"的质性材料 | Ch6 §Design Improvements after User Study |
| RQ1准确率headline数字 + Yes/Partial/No结论 | Ch7 Conclusion的RQ1段落（照抄RQ2那段的句式） |
| 一句话summary | Abstract结尾那句待补的话 |

---

## 8. 时间线建议 / Suggested Timeline

| 阶段 | 建议天数 |
|---|---|
| 搭建Qualtrics问卷 | 半天-1天 |
| 招募+发放 | 1-2天集中发送 |
| 收集期 | 7天 |
| 撤回等待期 | 7天（可以跟分析初稿并行，只是不要"定稿"数字） |
| 数据分析 | 2-3天 |
| 写入论文7处空白 | 2-3天 |
| **总计** | **约3周** |

如果时间紧张，收集期和撤回等待期是唯一不能被压缩太多的部分（涉及真实人类响应时间和伦理承诺），其余步骤都可以并行准备。

### 完整流程（从现在到论文彻底交完）

1. **搭建问卷**（你）——照`qualtrics_build_guide.md`建好、自查、发布，拿到匿名链接。
2. **招募**（你）——两组共13-20人，建议先找1-2人预跑一遍问卷再正式大批量发送。
3. **数据收集**（等待）——7天收集期 + 7天撤回期，期间不定稿数字，但可以并行准备分析框架。
4. **数据分析**（你导出数据后，一起）——按第6节方法跑RQ1/RQ2的数字，质性编码T3/T4/synthesis，专家vs大众交叉对比，挑3-5条匿名引用。
5. **论文填空**（先起草，你审核定稿）——Ch5 Participants/Study Procedure/Results/Discussion of Results、Ch6 Design Improvements after User Study、Ch7 RQ1结论、Abstract最后一句。
6. **全文校对+去AI味第二轮**（你主要负责）——新写的Results/Discussion部分要重新过一遍"减少AI写作痕迹"的检查；Discussion部分建议你自己加入真实的个人反思语气，这一步别人代劳不了。Acknowledgements你自己写。
7. **最终编译与格式检查**（你编译，配合看报错）——完整PDF排版检查、页数是否符合学院要求、Appendix完整性复查。
8. **提交论文**（你）——走学校/学院提交流程。
9. **项目彻底结束后的仓库收尾**（论文交完之后才做）——仓库大文件清理（任务#35）、三个日期快照文件夹要不要合并（任务#37）、GitHub social preview图片如果还没传、可选的简历/作品集项目简介精简版。

唯一不能压缩的是第3步的14天；其余步骤基本都能并行准备。

---

## 9. 风险与注意事项 / Risks & Reminders

### 中文
- **不要跳过Consent的强制勾选逻辑**——这是伦理批件里承诺的程序，跳过等于违反已批准的方案。
- **回复数量不够怎么办**：如果一周后不到10人，先别急着改研究设计，先追加发送渠道（比如问导师能不能帮忙转发给系里邮件列表），样本量不够可以在Limitations里坦诚讨论，不是致命问题。
- **数据存储**：Qualtrics导出的CSV建议存在这个repo之外的地方（比如OneDrive/大学网盘），不要把包含参与者回答的原始数据提交进git仓库——即使是匿名化的，也应该遵循数据最小化原则，仓库里只放分析后的汇总结果。
- **万一有人要求撤回**：按PIS承诺删除即可，不需要过度紧张。

### English
- Do not skip the mandatory consent checkboxes — this is what the ethics approval commits to.
- If response numbers are low after a week, expand distribution channels before changing the study design; a smaller-than-planned sample is a defensible, discussable limitation, not a fatal flaw.
- Store the raw exported CSV outside this git repository (e.g. university OneDrive) — only commit aggregated/anonymised analysis outputs, consistent with data minimisation.
- If someone requests withdrawal, honour it per the PIS; this is routine, not a crisis.
