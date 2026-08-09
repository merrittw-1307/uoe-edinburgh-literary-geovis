# 用户调研问卷（完整版，可直接照抄进Qualtrics）
# User Study Questionnaire (Complete, Qualtrics-ready)

**说明 / Note:** 本文档只包含问卷本身，逐屏排列，可以直接从上到下照抄进Qualtrics。设计说明、招募方案、分析方法见 `ethics/user_study_handbook.md`。本问卷内容与论文 `dissertation/5Aug/dissertation.tex` 的 Appendix A（Task Questions / Survey Questions）完全同步——如果以后要改问卷措辞，两边都要改，保持一致。

预计用时：**50-65分钟**（几轮修改后的最新估计——PIS/Consent Form里的时间区间尚未同步，见文末提醒）。

---

## Screen 1 — Welcome

> **Welcome**
>
> Thank you for considering taking part in this study about visualising Edinburgh's literary geography. Before you begin, please read the Participant Information Sheet [attach/link the PDF here].
>
> This should take about 50–65 minutes. There are no right or wrong answers — we're interested in your honest first impressions.
>
> This project has ethics approval from the Informatics Research Ethics Committee (reference 446635).

---

## Screen 2 — Consent *(required — all four boxes must be checked to continue)*

> Please confirm the following before continuing:
> - [ ] I have read and understood the Participant Information Sheet.
> - [ ] I understand my participation is voluntary and I can withdraw at any time up to 7 days after completing this survey, without giving a reason.
> - [ ] I consent to my anonymised responses being used in academic publications and presentations.
> - [ ] I agree to take part in this study.

*(Qualtrics实现：这四条做成4道独立的Force Response必答题，不用Skip Logic——没勾选就点不了下一页，效果一样但不用配置分支逻辑。参与者如果不同意，直接关掉页面退出即可，不会走到Screen 12。详细步骤见`qualtrics_build_guide.md`第2节。)*

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
> Each of the next three visualisations shows five authors' individual "fingerprints" — how each of them distributes place names across Edinburgh in their writing. For each one, you'll go through three short steps:
>
> 1. **Look at the reference view** — all five authors' fingerprints together, each labelled with the author's name. Take a few minutes to get a feel for how each author's pattern differs from the others — there's no trick to look for, just notice whatever stands out to you.
> 2. **Identify one on its own** — we'll show you one of those five fingerprints again, with the name hidden, and ask which author you think it is.
> 3. **Match all five at once** — we'll show you all five fingerprints again, unlabelled and in a new order, and ask you to match each one to an author.
>
> You're welcome to go back and check the reference view again at any point before answering — none of this is a memory test.
>
> Please open each link in a new browser tab, and come back to this page to answer.

---

## Screens 5a / 5b / 5c — Fingerprint Task ×3
*(Qualtrics: put these three blocks in a Randomizer, "present all 3, randomised order")*

**⚠️ 每个block有三个链接，顺序不能反：**
1. **"参考版"链接**——就是六可视化正文里原本的`radar.html`/`barcode.html`/`small_multiples.html`，5位作者都在、都标真名。这是给参与者"自主学习总结规律"用的，不是废弃的旧文件。
2. **"盲测版"链接**（`_task.html`结尾）——只有1位作者、不出现姓名、关掉了详情面板，用来回答F1-F4。
3. **"匹配版"链接**（`_matching.html`结尾，★2026年8月9日新增）——5位作者全部再出现一次，全部不署名、顺序打乱，用来回答M1-M2。

如果只发盲测版、不发参考版，参与者就是在凭空猜一个从没见过任何参照的陌生人名字，对完全不懂这几位作者的人来说毫无意义——这是Merritt指出的问题，已经改成"先学参考图、再认盲测图"这个结构。而单独的盲测（1个图配5个名字，命中率20%）信息量有限，只能得到"对/错"一个bit；匹配版让参与者一次性给全部5个图配对5个名字，能拿到完整的5×5混淆矩阵——哪两位作者的图形最容易被认错，这是比单次猜对/猜错丰富得多的数据，也更直接回答"这些指纹彼此之间到底有多可区分"这个RQ1的核心问题。

**★2026年8月9日第二次加强：F1b和P1，专门用来防止题目太简单（天花板效应）或太难（地板效应）**
- **F1b（第二猜测）**：F1只记录"对/错"一个bit，如果大部分人一次就猜中或者一次就猜错，数据会显得很单薄。加一个"如果第一个猜错了，你的第二猜测是谁"，可以看出参与者是"完全瞎猜"还是"至少缩小到了2个候选人里"——后者说明图形确实传递了某些有效信息，即使排名第一的选择不对，这是比单纯对/错更细致的数据。
- **P1（针对性两选一）**：M1的5×5矩阵测的是"整体上5个图形彼此有多好区分"，但如果5位作者的图形本来就长得很不一样，M1可能整体正确率很高，掩盖了"其实某两位作者的图形特别容易混淆"这个更细节的问题（天花板效应）。P1直接把**用真实数据算出来最相似的那一对作者**挑出来，做成一道二选一——因为这一对是所有作者两两组合里最难分辨的，能保证这道题不会因为"两个图形明显不一样"而变得太简单，同时二选一（50%基线）又不会因为选项太多而变得太难，是专门为了保证"够难又不至于太难"而设计的。三个设计选的具体是哪一对作者，以及为什么这么选，见下面的对照表。

**★2026年8月9日第三次修改：消除"靠记忆而非理解作弊"的漏洞（Merritt指出的问题）**——Merritt发现盲测版（`_task.html`）的图形颜色跟参考版**一模一样**（比如参考版里Scott是金色，盲测版里Scott也是金色）。这意味着参与者可以完全不看图形的形状，只要记住"参考图里金色的是Scott"这一个颜色标签，就能在F1里蒙对——这样测出来的根本不是"图形能不能被学会认出来"，而是"参与者的颜色记忆力"，跟RQ1想验证的东西完全不是一回事。**已修复**：三个盲测版文件（`radar_task.html`/`barcode_task.html`/`small_multiples_task.html`）的图形颜色现在统一改成中性的灰蓝色（`#5B6B8C`），跟参考版的颜色完全不一样，参与者只能靠形状本身来判断，不能靠"记颜色"这条捷径。匹配版（`_matching.html`）和P1用的图从一开始设计时就已经是中性色（当时就是为了防这个问题），不需要改。

**★2026年8月9日第四次修改：新增F0，专门用来防"靠轮廓记忆蒙混过关，但完全没理解图形在说什么"（Merritt指出的更深层问题）**——就算颜色改成中性色了，参与者理论上还是可以纯靠"记住这个锯齿状轮廓对应参考图里的Scott"这种**整体剪影记忆**来蒙对F1，完全不需要理解"这个尖峰指向Old Town方向，代表这位作者写Old Town写得最多"这层真正的语义。这样测出来的还是识别记忆力，不是"图形有没有把信息真正传达给读者"。F0是一道**只看当前这张盲测图就能回答、完全不需要记住参考图**的客观读图题——直接问"根据这张图，这位作者写得最多的是[哪个扇区/哪个地点]"，用真实数据里排名前4接近的选项做干扰项（不是随便编的假选项），逼参与者真的去看轴上的标签、读懂尖峰指向哪里，而不是只记一个抽象轮廓。这道题即使完全没看过参考图的人、单凭这张盲测图本身也应该能答对，是一个跟F1"认出是谁"完全独立的"有没有读懂这张图在说什么"的检验。三个设计各自问的对象和选项见下方对照表。

> **Step 1 — Reference view [1 of 3]**
> 👉 Open this link in a new tab, and take a few minutes to compare all five authors: **[Radar chart / Bar-code / Small Multiples — see "参考版链接" table below]**

> **Step 2 — Now try this one on its own**
> 👉 Open this link in a new tab (the reference view from Step 1 is still there if you want to check it again): **[see "盲测版链接" table below]**
>
> **F0.** *(★新增 — 题干和选项按设计各不相同，见下方对照表)* Based on the chart shown above (not your memory of the earlier reference view), which [sector/place] does this author's writing concentrate on the most?
> ○ [Option A] ○ [Option B] ○ [Option C] ○ [Option D]
>
> **F1.** Which of the following five authors do you think this represents?
> ○ Alexander McCall Smith ○ Irvine Welsh ○ John Gibson Lockhart ○ Walter Scott ○ Robert Louis Stevenson ○ I don't know
>
> **F1b.** *(★新增)* If your first guess turned out to be wrong, which of the five would be your second guess?
> ○ Alexander McCall Smith ○ Irvine Welsh ○ John Gibson Lockhart ○ Walter Scott ○ Robert Louis Stevenson
>
> **F2.** How confident are you in this answer?
> ○ Not at all confident ○ Slightly confident ○ Moderately confident ○ Confident ○ Very confident
>
> **F3.** What specific feature of the shape led you to that answer? (for example, an unusually large spike in one area, or a shape that's spread evenly across many areas)
> [free text]
>
> **F4.** If no one had told you anything about this visualisation, would you have understood how to read it just by looking?
> ○ Yes, easily ○ Yes, with a little effort ○ No, I was confused about how to read it

> **Step 3 — Matching all five**
> 👉 Open this link in a new tab: **[see "匹配版链接" table below]**
>
> This shows all five patterns again, without any names, in a new random order. Try to match each one to an author, using what you learned from the reference view.
>
> **M1.** Match each of the following to an author *(Matrix Table question — one row per shape/row/map, same 5 authors as answer options in every row; repeats are allowed)*
>
> | | Alexander McCall Smith | Irvine Welsh | John Gibson Lockhart | Walter Scott | Robert Louis Stevenson |
> |---|---|---|---|---|---|
> | Shape/Row/Map A | ○ | ○ | ○ | ○ | ○ |
> | Shape/Row/Map B | ○ | ○ | ○ | ○ | ○ |
> | Shape/Row/Map C | ○ | ○ | ○ | ○ | ○ |
> | Shape/Row/Map D | ○ | ○ | ○ | ○ | ○ |
> | Shape/Row/Map E | ○ | ○ | ○ | ○ | ○ |
>
> *(In Qualtrics the row label reads "Shape A" for the Radar block, "Row A" for the Bar-code block, "Map A" for the Small Multiples block — match the wording actually shown on the linked page.)*
>
> **M2.** Overall, having compared all five side by side, how easy or difficult do you think it would be to mix up any two of these five patterns?
> ○ Very easy to confuse ○ Somewhat easy to confuse ○ Neutral ○ Somewhat easy to tell apart ○ Very easy to tell apart
>
> **P1.** *(★新增 — 针对性两选一，题干和选项按设计各不相同，见下方对照表)* Look again at [Shape/Row/Map X] and [Shape/Row/Map Y] above. One of them is [Author A] and the other is [Author B]. Which is which?
> ○ [X] = [Author A], [Y] = [Author B]　○ [X] = [Author B], [Y] = [Author A]

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

**★2026年8月9日第二次加强：T-Strength和T-ClusterVerify，跟Fingerprint部分的F1b/P1是同一个思路，为了让数据更丰富、难度更合理**
- **T-Strength（评分题）**：T1只让参与者自己找"最强的一对"，如果这一对在视觉上过于突出（比如线特别粗、离得特别近），T1可能会有天花板效应——几乎所有人都答对，看不出设计之间的差异。T-Strength反过来，直接给参与者三对**真实权重分别是强/中/弱**的地名（用`network_enriched.json`里真实的共现次数选出来的，不是随便挑的），让参与者对每一对打分。这样即使T1本身饱和，T-Strength依然能看出参与者对"连接强度"这个概念的感知有多准——把三个设计的评分跟真实权重做相关性分析，能看出哪个设计的"强弱对比"传达得最清楚。
- **T-ClusterVerify（识别型选择题）**：T4是完全开放的"你有没有自己发现聚在一起的地名"，这题不设限但也有个问题——很多参与者可能什么都想不出来直接跳过（地板效应，拿不到数据）。T-ClusterVerify给一个有正确答案的识别版本：三个选项里只有一个是真的紧密关联的一组地名（来自metro线路分组，或者对network/linear重新跑过的社群检测结果），另外两个是故意从不同群组里混搭出来的干扰项。这样保底能拿到一个有no-floor-effect风险的量化正确率，跟T4的开放式回答互相印证——如果一个参与者在T4里自己说出的分组跟T-ClusterVerify选对的那组高度吻合，这是很强的双重证据。

**★2026年8月9日第三次修改：T1b、以及T-Strength/T-ClusterVerify改成三个设计各不相同的内容——都是为了堵住"跨设计抄答案"这个漏洞（Merritt指出的问题）**——Network、Linear、Metro三个设计背后其实是**同一份共现权重数据**，这意味着"哪两个地方连接最强"（T1）、以及原本设计的T-Strength三对地名、T-ClusterVerify的真实群组，在三个block里的**正确答案是完全一样的**！参与者只要在第一个拓扑设计里答对一次（哪怕只是蒙对，或者本来就知道"Leith和Princes Street"这类爱丁堡地标常识），后面两个设计直接照抄同一个答案就行，根本不需要看懂第二、第三个设计具体是怎么画的——这样测出来的不是"这个设计有没有把连接强弱讲清楚"，而是"参与者记不记得自己刚才的答案"，完全违背了这几道题的本意。**已修复，两处改动**：
1. **新增T1b**：紧跟在T1后面，让参与者写一句"是这张图里的什么具体特征让你这样判断的"（比如线的粗细、两点画得多近、是不是在同一条彩色线上）。就算参与者的"两个地名"答案是照抄上一个设计的，只要T1b写的解释明显不符合当前这个设计的画法（比如在metro图里却写"因为线特别粗"，但metro根本没有用线粗细表示强度），就能在质性编码时识别出这是没有真正看图、只是抄答案。
2. **T-Strength和T-ClusterVerify的具体地名/分组，三个设计现在各不相同**（虽然背后是同一份数据，但选的是数据里**不同**的强/中/弱地名对、不同的真实社群），参与者没法直接把上一个设计的评分或选择原样搬过来，必须在当前这张图里重新找到题目问的这几个具体地名才能作答。三个设计各自的具体内容见下方对照表。

> **Visualisation [1 of 3]**
> 👉 Open this link in a new tab: **[Network / Linear / Metro — see URL table below]**
>
> Take a minute to explore freely before answering.
>
> **T1.** Which two places appear to be the *most strongly connected*?
> Place A: ______   Place B: ______
>
> **T1b.** *(★新增)* What about this diagram made you think these two places are the most connected? (for example: the thickest line between them, how close together they're drawn, being on the same coloured line)
> [free text]
>
> **T2.** Based on your own knowledge of Edinburgh (or your best guess if you're not familiar with the city), are these two places geographically close together or far apart?
> ○ Very close ○ Somewhat close ○ Not sure ○ Somewhat far ○ Very far
>
> **T-Strength.** *(★新增 — 评分题，题目/量表一样，具体三对地名按设计各不相同，见下方对照表)* For each of the following pairs of places, how strongly connected do they appear to be in this visualisation? *(rating-grid/Matrix Table question, one row per pair, 5-point scale each: Not connected at all -- Extremely strongly connected)*
> | | Not connected at all | | | | Extremely strongly connected |
> |---|---|---|---|---|---|
> | [Pair 1 — strong] | ○ | ○ | ○ | ○ | ○ |
> | [Pair 2 — medium] | ○ | ○ | ○ | ○ | ○ |
> | [Pair 3 — weak] | ○ | ○ | ○ | ○ | ○ |
>
> **T3.** Beyond that pair, is there any *other* connection in this visualisation that surprises you — for example, two places that seem strongly linked even though you'd expect them to be unrelated, or two places you'd expect to be linked that don't appear connected at all? Name the places and briefly explain what surprised you.
> [free text — optional but encouraged]
>
> **T4.** Do you notice any group of **three or more** places that seem to form a cluster of connections with each other? If so, list them and, if you have a guess, why you think they might be grouped together.
> [free text — optional]
>
> **T-ClusterVerify.** *(★新增 — 识别型选择题，用来跟T4的开放式回答互相印证；三个选项文字按设计各不相同，见下方对照表；三个选项在Qualtrics里要开启随机排序)* Which of the following groups of places looks like it forms the *tightest* cluster of interconnections in this visualisation?
> ○ [Option A] ○ [Option B] ○ [Option C]
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

---

## 六个可视化链接 / Visualisation URLs

**Fingerprint任务每个设计要用三个链接（参考版 → 盲测版[F1-F4] → 匹配版[M1-M2]），Topology任务（T1-T5）只用原版链接**——几组链接用途都不一样，千万别用混：

### 参考版链接（Step 1，Fingerprint Task专用，Screens 5a/5b/5c）

就是六可视化正文里原本的`radar.html`/`barcode.html`/`small_multiples.html`——5位作者都在、都标真名，一个字节都没改过。这一步是让参与者"自主观察、自己总结每个作者的图形有什么不一样"，不设标准答案。

| 设计 Design | 网址 URL |
|---|---|
| Radar chart | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/radar/d3/radar.html` |
| Bar-code | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/barcode/d3/barcode.html` |
| Small multiples | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/small_multiples/d3/small_multiples.html` |

### 盲测版链接（Step 2，Fingerprint Task专用，Screens 5a/5b/5c）

参与者看完上面的参考版、自己总结出规律之后，再看这个去掉了姓名和详情面板的单作者版本，回答F1-F4。

| 设计 Design | 盲测对象 | 网址 URL |
|---|---|---|
| Radar chart | Walter Scott | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/radar_task.html` |
| Bar-code | John Gibson Lockhart | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/barcode_task.html` |
| Small multiples | Robert Louis Stevenson | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/small_multiples_task.html` |

**为什么要分两步 / 2026年8月9日修改的原因**：一开始只给盲测版链接，等于让完全不了解这几位作者的参与者凭空对应一个从没见过任何参照的陌生人名字——对没有文学背景的大众组参与者来说这个任务没有意义，也测不出"图形本身能不能承载可学习、可辨认的个人特征"这个我们真正想知道的问题（Merritt指出的问题）。现在改成"先看参考版自主总结规律，再看盲测版尝试识别"，测的是图形的**可学习性和可辨识度**，不再依赖参与者本来就认识这几位作者。三个设计故意用了三个不同的盲测作者（而不是同一个人反复出现），避免参与者带着"记忆效应"把第一个设计的猜测原样套到后两个。

**F0题干对照表（★2026年8月9日第四次新增，用来防"记轮廓不理解语义"）**——三个设计问的对象不同（Radar是扇区，Bar-code/Small Multiples是具体地点），选项是该盲测作者真实数据里排名前4的扇区/地点，不是随便编的：

| 设计 | 问的是 | 正确答案（真实数据里排名第1） | 干扰项（真实数据里排名2-4） |
|---|---|---|---|
| Radar chart | 扇区 sector | Old Town（32.0%） | Canongate（15.9%）、Leith（9.6%）、Liberton/Gilmerton（9.3%） |
| Bar-code | 具体地点 place | Canongate（21.1%） | Castle Street（19.1%）、Leith（9.4%）、Holyrood（6.6%） |
| Small multiples | 具体地点 place | Leith（56次提及） | Princes Street（46次）、Cramond（36次）、Swanston（32次） |

选项在Qualtrics里要开启"Randomize choice order"，正确答案不能每次都排在第一个。

### 匹配版链接（Step 3，Fingerprint Task专用，Screens 5a/5b/5c，★2026年8月9日新增）

参与者做完单独识别（F1-F4）之后，再看这个把全部5位作者的图**同时**、**全部不署名**、**顺序打乱**放在一起的版本，回答M1（配对）和M2（主观区分度评分）。

| 设计 Design | 网址 URL |
|---|---|
| Radar chart | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/radar_matching.html` |
| Bar-code | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/barcode_matching.html` |
| Small multiples | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/small_multiples_matching.html` |

**⚠️ 打乱顺序是固定的、写死在文件里的，不是每个参与者随机生成的**——因为这个页面是在Qualtrics之外独立打开的一个静态网页，如果用JS给每个参与者随机洗牌，Qualtrics完全无法知道当时洗出来的是哪一种对应关系，你分析问卷答案时就没法判断"参与者说Shape A是Welsh"到底对不对。所以每个设计各自固定了一种打乱顺序（三个设计之间顺序也彼此不同，避免参与者用"上一题A是谁"去套下一题），**评分时按下表的固定答案核对**：

| Radar (`radar_matching.html`) | Bar-code (`barcode_matching.html`) | Small Multiples (`small_multiples_matching.html`) |
|---|---|---|
| Shape A = Irvine Welsh | Row A = Walter Scott | Map A = John Gibson Lockhart |
| Shape B = Robert Louis Stevenson | Row B = Alexander McCall Smith | Map B = Irvine Welsh |
| Shape C = Alexander McCall Smith | Row C = Robert Louis Stevenson | Map C = Walter Scott |
| Shape D = John Gibson Lockhart | Row D = Irvine Welsh | Map D = Robert Louis Stevenson |
| Shape E = Walter Scott | Row E = John Gibson Lockhart | Map E = Alexander McCall Smith |

三个设计的打乱顺序、以及和F1-F4盲测版用的单一作者，都刻意选得互不相同，防止参与者靠"这个字母上次是谁"这种捷径蒙对，而不是真的靠图形本身分辨。

**P1题干对照表（★2026年8月9日新增，跟M1用同一个匹配版页面，不需要额外打开新链接）**——这一对是用真实数据算出来的、每个设计里最相似（最难分辨）的一对作者（余弦相似度：Radar 0.844、Small Multiples 0.744、Bar-code为避免和Radar重复选了第二相似的0.474），选它们做2选1就是为了保证这道题不会因为"两个图形一眼看上去就很不一样"而变得太简单：

| 设计 Design | 题干里的两个字母 | 对应的两位作者 |
|---|---|---|
| Radar chart | Shape D vs Shape E | John Gibson Lockhart vs Walter Scott |
| Bar-code | Row A vs Row D | Walter Scott vs Irvine Welsh |
| Small multiples | Map A vs Map D | John Gibson Lockhart vs Robert Louis Stevenson |

### 原版链接（Topology Task专用，Screens 8a/8b/8c）

| 设计 Design | 网址 URL |
|---|---|
| Force-directed network | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/network/d3/network.html` |
| Linear connection diagram | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/linear/d3/linear.html` |
| Metro-style map | `https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/metro/d3/metro.html` |

这三个继续用原版就好——Topology任务问的是"哪两个地方连接最强"，本来就是把5位作者的数据合并在一起看，不存在"猜是谁"的盲测需求，原版没有问题。

**T-Strength的三对地名（★2026年8月9日新增，第二次修改后三个Topology设计改成各不相同，防止参与者直接照抄上一个设计的评分）**——虽然network/linear/metro背后是同一份共现权重数据，但三个设计选的是数据里**不同**的强/中/弱地名对，参与者必须在当前这张图里重新找到题目问的具体地名才能作答：

| 设计 | 强 | 中 | 弱 |
|---|---|---|---|
| Force-directed network | New Town & Princes Street（权重18） | Lochend & Waverley Station（权重4） | Leith & Silvermills（权重2） |
| Linear connection diagram | Dundas Street & Princes Street（权重17） | Old Town & Princes Street（权重6） | Arthur's Seat & Haddington（权重2） |
| Metro-style map | Bruntsfield & Dundas Street（权重16） | Howe Street & Stockbridge（权重6） | Dalkeith & Linlithgow（权重2） |

（数据来源：`data/processed/dir_2/network/data/network_enriched.json`的edges列表，三个设计权重数据完全一致，只是各自选了不同的具体地名对；最强的一对Leith-Princes Street权重28，是T1题目本来就该被参与者自己找出来的答案，三个设计都故意没有选它，避免和T1完全重复。）

**T-ClusterVerify的三个选项（★2026年8月9日新增，第二次修改后Force-directed network和Linear connection diagram也改成了不同的真实群组，不再共用一组）**——每组里只有一个是真实的紧密关联群组（选项顺序在Qualtrics里要设置成随机）：

| 设计 | 真实群组（正确答案） | 干扰项1 | 干扰项2 |
|---|---|---|---|
| Force-directed network | New Town, Princes Street, Dundas Street, Stockbridge（对network边数据跑Louvain社群检测得到的社群1） | New Town, Leith Walk, Holyrood, Waverley Station（故意跨社群混搭） | Grassmarket, Bruntsfield, Tollcross, Cramond（故意跨社群混搭） |
| Linear connection diagram | Leith Walk, Lochend, Pilrig, Waverley Station（同一份社群检测里**不同**的社群2，跟Network的社群1是两个真实但不同的群组） | Leith Walk, New Town, Grassmarket, Dalkeith（故意跨社群混搭） | Lochend, Stockbridge, Canongate, Musselburgh（故意跨社群混搭） |
| Metro-style map | University of Edinburgh, Royal Society of Edinburgh, Castle Street, St Giles（"Lockhart's Edinburgh"线路的真实站点） | Castle Street, St Giles, Pilrig, Tollcross（混了"Lockhart's Edinburgh"和"Welsh's Edinburgh"两条线） | Moray Place, Grassmarket, Dalkeith, Hanover Street（混了"Smith's Edinburgh"和"Scott's Edinburgh"两条线） |

**⚠️ 正确答案不要总是放在"选项A"**：Qualtrics的Multiple Choice题型有"Randomize choice order"选项，务必打开，否则三个设计的正确答案如果总是排在同一个位置，会被眼尖的参与者看出规律。

（全部已实测确认可正常打开，最近一次核实：2026年8月9日 / all verified live, last checked 9 August 2026）

**注意 / Note：** 项目里还有一个`combined_interface.html`（整合界面，可自由切换全部408位作者），那是**给导师看的演示工具，不要发给参与者，也不要放进这份问卷**，否则会破坏F1/T1等题目"仅凭图形本身识别"的测试前提。/ The project also has a separate `combined_interface.html` ("Combined Interface") with free switching across all 408 authors; that is a **supervisor-facing demo tool and must not be sent to participants or linked from this questionnaire**, as doing so would undermine the "identify from the image alone" premise behind questions like F1 and T1.

---

## 题目清单一览（给你自己核对用，不给参与者看）/ Question Count Summary (for your own reference)

| 部分 | 题数 |
|---|---|
| Consent | 4 项确认 |
| Background | 5题 |
| Fingerprint tasks（3设计 ×（F0、F1、F1b、F2、F3、F4、M1、M2、P1 共9题）） | 27题（★F0/F1b/M1/M2/P1均为2026年8月9日新增） |
| Fingerprint ranking | 2题 |
| Topology tasks（3设计 ×（T1、T1b、T2、T-Strength、T3、T4、T-ClusterVerify、T5 共8题）） | 24题（★T1b/T-Strength/T-ClusterVerify均为2026年8月9日新增） |
| Cross-design synthesis | 1题（★新增，专门用来捕捉自发的深度发现） |
| Topology ranking | 2题 |
| Reflection | 5题 |
| **合计** | **70题**（含多项选择+矩阵表+评分网格+自由文本，预计50-65分钟——F0是快速单选题，对总时长影响很小，暂不调整分钟数区间；PIS里如果写的是35-50/40-55/45-60分钟，需要同步改成50-65分钟，见下方提醒） |

**关于深度**：T3、T4、Screen 9这三处是专门为了让被试自发说出"某些地名之间有意外的关系""某几个地名好像是一伙的"这类观察而设计的——不设标准答案，鼓励自由发挥，分析时重点编码这三处的自由文本。T4尤其关键：如果参与者能不看任何提示、自己说出"这几个站好像是一条线上的"，就是对社群检测方法本身最有力的独立验证。

**关于难度校准（★2026年8月9日第二次新增的F1b/P1/T-Strength/T-ClusterVerify，都是为了同一个目的）**：单纯的F1（1选5）和T1（自己找最强的一对）都有可能出现天花板效应（图形/连接太明显，所有人都答对，看不出设计之间的差异）或地板效应（完全没有参照，大家都是瞎猜或者直接跳过不填）。这四道新题都是用**真实数据算出来的**难度适中的具体案例（最相似的作者对、真实强/中/弱的连接、真实的社群分组+干扰项），不是随便设计的，目的是保证不管F1/T1本身表现如何，这几道题都能提供有区分度、可分析的数据。

**关于防止"靠记忆而非理解作弊"（★2026年8月9日第三、四次修改，Merritt指出的问题，共三处修复）**：
1. **F1盲测版图形颜色改成中性色**——之前盲测版跟参考版用的是完全一样的颜色，参与者可以只记颜色标签、完全不看形状就蒙对F1，这样测出来的是记忆力不是"图形能不能被学会认出来"。现已把三个盲测版文件的颜色统一改成中性灰蓝色，跟参考版的颜色不再一样。
2. **T1b + T-Strength/T-ClusterVerify改成三个设计各不相同**——Network/Linear/Metro背后是同一份共现权重数据，导致T1、以及原本设计的T-Strength/T-ClusterVerify在三个设计里的正确答案完全一样，参与者只要在第一个拓扑设计里蒙对/答对一次，后面两个直接照抄同一个答案就行，不需要真的看懂后面两张图。现已加入T1b（要求参与者写出"具体是这张图的什么特征让你这样判断"，答案抄袭但解释对不上当前设计画法的情况能在质性编码时被识别出来），并把T-Strength/T-ClusterVerify的具体地名/群组改成三个设计各不相同（虽然背后数据一样，但参与者必须在当前图上重新找到题目问的具体内容才能作答，不能直接照抄评分）。
3. **新增F0（★第四次修改，比颜色修复更进一步）**——就算颜色改成中性色，参与者理论上还是可以纯靠"记住这个轮廓对应参考图里的Scott"这种整体剪影记忆蒙对F1，完全不需要理解图形具体在传达什么信息（比如"这个尖峰代表这位作者写Old Town最多"）。F0是一道只看当前这张盲测图就能回答、完全不需要记住参考图的客观读图题，直接检验参与者有没有真正解码出图形的语义内容，而不是在匹配一个记住的抽象轮廓。

**⚠️ PIS/同意书时间预估需要同步更新**：几轮修改后总题数从46题涨到70题，预计用时上限从50分钟涨到65分钟左右。请检查Participant Information Sheet和Consent Form里写的时间区间，如果还是"35-50分钟"/"40-55分钟"/"45-60分钟"，需要同步改成"50-65分钟"，避免和实际用时不符。
