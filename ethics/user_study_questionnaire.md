# 用户调研问卷（完整版，可直接照抄进Qualtrics）
# User Study Questionnaire (Complete, Qualtrics-ready)

**说明 / Note:** 本文档只包含问卷本身，逐屏排列，可以直接从上到下照抄进Qualtrics。设计说明、招募方案、分析方法见 `ethics/user_study_handbook.md`。本问卷内容与论文 `dissertation/5Aug/dissertation.tex` 的 Appendix A（Task Questions / Survey Questions）完全同步——如果以后要改问卷措辞，两边都要改，保持一致。

预计用时：**35-50分钟**（已同步进最新版PIS）。

---

## Screen 1 — Welcome

> **Welcome**
>
> Thank you for considering taking part in this study about visualising Edinburgh's literary geography. Before you begin, please read the Participant Information Sheet [attach/link the PDF here].
>
> This should take about 35–50 minutes. There are no right or wrong answers — we're interested in your honest first impressions.
>
> This project has ethics approval from the Informatics Research Ethics Committee (reference 446635).

---

## Screen 2 — Consent *(required — all four boxes must be checked to continue)*

> Please confirm the following before continuing:
> - [ ] I have read and understood the Participant Information Sheet.
> - [ ] I understand my participation is voluntary and I can withdraw at any time up to 7 days after completing this survey, without giving a reason.
> - [ ] I consent to my anonymised responses being used in academic publications and presentations.
> - [ ] I agree to take part in this study.

*(Qualtrics logic: if any box unchecked → skip to Screen 12 "Not enrolled")*

---

## Screen 3 — Background Questionnaire

> **About You**
> *(This helps us understand who took part — it isn't used to identify you individually.)*
>
> **B1.** How familiar are you with Edinburgh's literary history (e.g. Sir Walter Scott, Robert Louis Stevenson, contemporary Edinburgh fiction)?
> ○ Not at all familiar ○ Slightly familiar ○ Moderately familiar ○ Very familiar ○ Extremely familiar
>
> **B2.** Have you read any works by these authors: Alexander McCall Smith, Irvine Welsh, John Gibson Lockhart, Walter Scott, or Robert Louis Stevenson?
> ○ Yes, several ○ Yes, one or two ○ No
>
> **B3.** How would you best describe your background?
> ○ Literary studies / English literature
> ○ Digital humanities
> ○ Information visualisation / HCI / Computer Science
> ○ Other academic background
> ○ General public, no specialist background in the above
> ○ Other (please specify): ______
>
> **B4.** How familiar are you with reading data visualisations or charts in general (e.g. bar charts, network diagrams, maps)?
> ○ Not at all familiar ○ Slightly familiar ○ Moderately familiar ○ Very familiar ○ Extremely familiar
>
> **B5.** Have you lived in or spent significant time in Edinburgh?
> ○ Yes, I live/have lived there ○ I've visited several times ○ I've visited once or twice ○ Never

---

## Screen 4 — Part 1 Instructions

> **Part 1: Author Fingerprints**
>
> You're about to see three different visualisations, one at a time. Each one shows how a single author distributes place names across Edinburgh in their writing — but we won't tell you which author it is, or how to read the chart. Just look at it, form your own impression, and answer the questions that follow.
>
> Please open each visualisation in a new browser tab using the link provided, look at it for as long as you like, then come back to this page to answer.

---

## Screens 5a / 5b / 5c — Fingerprint Task ×3
*(Qualtrics: put these three blocks in a Randomizer, "present all 3, randomised order")*

**⚠️ 用下面"盲测版链接"表里的`_task.html`链接，不要用六可视化正文里的`radar.html`/`barcode.html`/`small_multiples.html`——那三个原版一次性显示全部5位作者、图例上直接写着真名，参与者根本没法"猜"，点开详情面板还能看到书名/例句，等于变相剧透。`_task.html`版本才是专门为这道盲测题做的：每个只显示1位作者、完全不出现姓名、关掉了详情面板。**

> **Visualisation [1 of 3]**
> 👉 Open this link in a new tab: **[Radar chart / Bar-code / Small Multiples — see "盲测版链接" table below]**
>
> **F1.** Which of the following five authors do you think this visualisation represents?
> ○ Alexander McCall Smith ○ Irvine Welsh ○ John Gibson Lockhart ○ Walter Scott ○ Robert Louis Stevenson ○ I don't know
>
> **F2.** How confident are you in this answer?
> ○ Not at all confident ○ Slightly confident ○ Moderately confident ○ Confident ○ Very confident
>
> **F3.** In one or two sentences, what about the visualisation led you to that answer?
> [free text]
>
> **F4.** If no one had told you anything about this visualisation, would you have understood how to read it just by looking?
> ○ Yes, easily ○ Yes, with a little effort ○ No, I was confused about how to read it

---

## Screen 6 — Fingerprint Ranking

> Having now seen all three (radar chart, bar-code, small multiples), which did you find the most intuitive to read *without* any explanation?
> ○ Radar chart ○ Bar-code ○ Small multiples (maps)
>
> Why? *(optional, free text)*

---

## Screen 7 — Part 2 Instructions

> **Part 2: Place Connections**
>
> Now you'll see three different visualisations showing how places mentioned in Edinburgh literature relate to each other. Before answering, take a moment to explore each one freely — hover over places, click on them, zoom or scroll if the design allows. There's no need for any special knowledge of Edinburgh.

---

## Screens 8a / 8b / 8c — Topology Task ×3
*(Qualtrics: Randomizer, "present all 3, randomised order")*

> **Visualisation [1 of 3]**
> 👉 Open this link in a new tab: **[Network / Linear / Metro — see URL table below]**
>
> Take a minute to explore freely before answering.
>
> **T1.** Which two places appear to be the *most strongly connected*?
> Place A: ______   Place B: ______
>
> **T2.** Based on your own knowledge of Edinburgh (or your best guess if you're not familiar with the city), are these two places geographically close together or far apart?
> ○ Very close ○ Somewhat close ○ Not sure ○ Somewhat far ○ Very far
>
> **T3.** Beyond that pair, is there any *other* connection in this visualisation that surprises you — for example, two places that seem strongly linked even though you'd expect them to be unrelated, or two places you'd expect to be linked that don't appear connected at all? Name the places and briefly explain what surprised you.
> [free text — optional but encouraged]
>
> **T4.** Do you notice any group of **three or more** places that seem to form a cluster of connections with each other? If so, list them and, if you have a guess, why you think they might be grouped together.
> [free text — optional]
>
> **T5.** If no one had told you anything about this visualisation, would you have understood how to read it just by looking?
> ○ Yes, easily ○ Yes, with a little effort ○ No, I was confused about how to read it

---

## Screen 9 — Cross-design Synthesis *(new — this is the key "deep insight" question)*

> Having now seen all three ways of showing connections between places, is there anything about Edinburgh's literary geography that surprised you, or that you hadn't thought about before — for example, places that seem to "belong together" in these authors' writing that you wouldn't have expected?
> [free text — optional but encouraged]

---

## Screen 10 — Topology Ranking

> Having now seen all three (force-directed network, linear connection diagram, metro map), which did you find the most intuitive to read *without* any explanation?
> ○ Force-directed network ○ Linear connection diagram ○ Metro-style map
>
> Why? *(optional, free text)*

---

## Screen 11 — Reflection

> **Final thoughts**
>
> **R1.** Before this study, had you thought about literary place names as anything other than locations on a map?
> [free text]
>
> **R2.** Did any of the six visualisations change how you think about the relationship between a literary work and the real city it's set in? If so, which one, and how?
> [free text]
>
> **R3.** Is there anything about any of the six visualisations that confused you, or that you would change?
> [free text]
>
> **R4.** Any other comments?
> [free text]
>
> **R5.** Overall, which single visualisation (of all six) did you find the most memorable or interesting, and why?
> [free text]

---

## Screen 12 — Debrief / Thank You

> **Thank you!**
>
> That's everything — thank you very much for your time and thoughtful answers. Your responses will help improve how literary geography is visualised for future audiences.
>
> If you have any questions about this study, contact the lead researcher, Uta Hinrichs (uhinrich@ed.ac.uk).
>
> *(Optional)* If you'd like a short summary of the results once the study is complete, leave your email below. This will be stored separately from your survey answers and will not be linked to them.
> Email (optional): ______

*(This is also the screen shown to anyone who didn't complete consent on Screen 2, minus the optional email field.)*

---

## 六个可视化链接 / Visualisation URLs

**Fingerprint任务（F1-F4）用"盲测版"链接，Topology任务（T1-T5）用原版链接**——这两组链接的用途不一样，千万别用混：

### 盲测版链接（Fingerprint Task专用，Screens 5a/5b/5c）

| 设计 Design | 盲测对象 | 网址 URL |
|---|---|---|
| Radar chart | Walter Scott | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/radar/d3/radar_task.html` |
| Bar-code | John Gibson Lockhart | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/barcode/d3/barcode_task.html` |
| Small multiples | Robert Louis Stevenson | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/small_multiples/d3/small_multiples_task.html` |

**这三个链接是2026年8月9日新加的，专门为F1这道"猜作者"题做的**：原本的`radar.html`/`barcode.html`/`small_multiples.html`是一次性展示全部5位作者、图例上直接写真名的探索工具，参与者点开根本不用猜，直接读图例上的名字就行——这是Merritt发现的一个真实设计漏洞。`_task.html`这三个新文件每个只画1位作者、图例整个拿掉、点击查看书名/例句的详情面板也关掉了（书名本身就能暴露作者，比如看到《Trainspotting》就知道是Welsh），只留下形状和悬停读数这两样，跟F1-F4题目的设计初衷完全对上。三个设计故意用了三个不同的作者（而不是同一个人在三种图里反复出现），这样参与者猜完第一个设计之后不会带着"记忆效应"去猜后面两个。

### 原版链接（Topology Task专用，Screens 8a/8b/8c）

| 设计 Design | 网址 URL |
|---|---|
| Force-directed network | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/network/d3/network.html` |
| Linear connection diagram | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/linear/d3/linear.html` |
| Metro-style map | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/metro/d3/metro.html` |

这三个继续用原版就好——Topology任务问的是"哪两个地方连接最强"，本来就是把5位作者的数据合并在一起看，不存在"猜是谁"的盲测需求，原版没有问题。

（全部已实测确认可正常打开，最近一次核实：2026年8月9日 / all verified live, last checked 9 August 2026）

**注意 / Note：** 项目里还有一个`combined_interface.html`（整合界面，可自由切换全部408位作者），那是**给导师看的演示工具，不要发给参与者，也不要放进这份问卷**，否则会破坏F1/T1等题目"仅凭图形本身识别"的测试前提。/ The project also has a separate `combined_interface.html` ("Combined Interface") with free switching across all 408 authors; that is a **supervisor-facing demo tool and must not be sent to participants or linked from this questionnaire**, as doing so would undermine the "identify from the image alone" premise behind questions like F1 and T1.

---

## 题目清单一览（给你自己核对用，不给参与者看）/ Question Count Summary (for your own reference)

| 部分 | 题数 |
|---|---|
| Consent | 4 项确认 |
| Background | 5题 |
| Fingerprint tasks（3设计 × 4题） | 12题 |
| Fingerprint ranking | 2题 |
| Topology tasks（3设计 × 5题） | 15题 |
| Cross-design synthesis | 1题（★新增，专门用来捕捉自发的深度发现） |
| Topology ranking | 2题 |
| Reflection | 5题 |
| **合计** | **46题**（含多项选择+自由文本，预计35-50分钟） |

**关于深度**：T3、T4、Screen 9这三处是专门为了让被试自发说出"某些地名之间有意外的关系""某几个地名好像是一伙的"这类观察而设计的——不设标准答案，鼓励自由发挥，分析时重点编码这三处的自由文本。T4尤其关键：如果参与者能不看任何提示、自己说出"这几个站好像是一条线上的"，就是对社群检测方法本身最有力的独立验证。
