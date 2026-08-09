# Qualtrics 问卷搭建完全手册

**这份文档的用途**：跟着从上到下一步步做，照抄英文文字进Qualtrics，就能把问卷完整搭出来，不需要再回头查别的文档。题目内容跟 `ethics/user_study_questionnaire.md`（问卷正本）以及论文 `dissertation/5Aug/dissertation.tex` 的 Appendix A 完全一致——这份文档只是把那份内容翻译成"在Qualtrics里具体怎么点"的操作步骤。

**预计搭建时间**：2–3小时（Fingerprint部分现在是"参考版+盲测版"两步结构，比纯单链接多一点搭建量；第一次用Qualtrics会慢一些，跟着做不用自己想措辞）。

**链接核实状态**：2026年8月9日更新——Fingerprint任务每个block现在用两个链接：Step 1参考版（原本的`radar.html`/`barcode.html`/`small_multiples.html`，5人都标名字，用来让参与者自主总结规律）+ Step 2盲测版（`radar_task.html`/`barcode_task.html`/`small_multiples_task.html`，去掉名字用来测试识别），原因见第5节。全部链接（3个参考版 + 3个盲测版 + Topology原版3个 + PIS）当天逐一实测，全部200正常返回。

---

## 目录

0. 开始之前：创建问卷
1. Block 1 — Welcome
2. Block 2 — Consent
3. Block 3 — Background
4. Block 4 — Part 1 Instructions
5. Block 5/6/7 — Fingerprint Tasks ×3（Radar / Bar-code / Small Multiples）
6. Block 8 — Fingerprint Ranking
7. Block 9 — Part 2 Instructions
8. Block 10/11/12 — Topology Tasks ×3（Network / Linear / Metro）
9. Block 13 — Cross-design Synthesis
10. Block 14 — Topology Ranking
11. Block 15 — Reflection
12. Block 16 — Debrief
13. Survey Flow 设置（两处随机顺序）
14. 全局设置（Survey Options）
15. 发布前自查清单

---

## 0. 开始之前：创建问卷

1. 打开 `https://ed.qualtrics.com`，用爱丁堡大学EASE账号登录（跟邮箱/Learn同一套登录，不是单独的Qualtrics密码）。
2. 点右上角 **Create new project**。
3. 选 **Survey** → **Start from scratch**。
4. 问卷名称（Project name），直接复制粘贴：

   ```
   Edinburgh Literary Geography — Visualisation Study
   ```

5. 点 **Get started**，进入编辑界面。你会看到左边默认已经有一个空的 "Default Question Block"——第1步开始时把它改名/复用成 "Welcome" block即可，不用删掉重建。

---

## 1. Block 1 — Welcome

**操作**：把默认的第一个block改名为 `Welcome`（点block标题旁边的铅笔图标改名）。这个block里只放1道题。

### Q-Welcome
- **Question Type**：`Text/Graphic`（在"Change question type"菜单里选，图标通常显示"Tx"或写着"Text/Graphic"）
- **Question Text**（直接复制粘贴进题目文本框，注意方括号里的内容要按说明操作，不要直接粘贴方括号）：

  ```
  Welcome

  Thank you for considering taking part in this study about visualising Edinburgh's literary geography. Before you begin, please read the Participant Information Sheet:
  ```

- 在这段文字下面，插入一个超链接，文字显示为 `Participant Information Sheet`，链接指向：

  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/dissertation/5Aug/pis.pdf
  ```

  **怎么插入超链接**：选中你要做成链接的文字 → 富文本工具栏点🔗链接图标 → 粘贴上面的URL → 一定要检查"在新标签页打开"（Open in new tab / target=_blank）有没有勾上，没有的话点工具栏的 `</>` (Source code) 按钮，确认对应的 `<a>` 标签里有 `target="_blank"`，没有就手动加上。**这个"新标签页打开"的检查在后面每一个插入链接的地方都要做，后文不再重复强调。**

- 链接下面继续粘贴：

  ```
  This should take about 35–50 minutes. There are no right or wrong answers — we're interested in your honest first impressions.

  This project has ethics approval from the Informatics Research Ethics Committee (reference 446635).
  ```

- 这道题不需要设置 Force Response（纯说明文字，没有交互）。

---

## 2. Block 2 — Consent

**操作**：新建一个block，命名为 `Consent`。

**重要设计说明**：不要按老思路做"一道题4个复选框+跳转逻辑"。更简单可靠的做法是**做成4道独立的题，每道题只有1个复选框选项，并且都设置成必答（Force Response）**。这样Qualtrics会在参与者没有勾选某一项时直接不让他点"下一页"（Next），效果跟"没勾选就不能继续"完全一样，而且不需要你去配置容易出错的Skip Logic。如果有人不同意，他自己关掉浏览器页面退出就行——这也是Qualtrics问卷里最常见、最标准的处理同意书的方式。

### Q-Consent1
- **Question Type**：`Multiple Choice`
- 建好题目后，点右侧的 **Change question type** 旁边小齿轮/或题目下方的 "Selector" 设置，把 Selector 改成 **Multiple Answer**（复选框样式，即使只有一个选项也要选这个，不要选Single Answer，否则显示的是圆形单选框而不是方框复选框）
- **Question Text**：

  ```
  Please confirm the following before continuing:
  ```

  （这句话只需要在Consent1这一题里写一次；Consent2/3/4三道题的题目文本框可以留空或者只写一个空格，因为它们看起来是同一个问题的延续——四道题连续放在同一个block里，视觉上就是一份完整的确认列表。）

- **Answer Choices**（只有1个选项，直接粘贴）：

  ```
  I have read and understood the Participant Information Sheet.
  ```

- **设置**：右侧 Validation → Force Response → 打开（**On**）

### Q-Consent2
同Q-Consent1的设置（Multiple Choice / Multiple Answer / Force Response On），题目文本框留空，选项：

```
I understand my participation is voluntary and I can withdraw at any time up to 7 days after completing this survey, without giving a reason.
```

### Q-Consent3
同上，选项：

```
I consent to my anonymised responses being used in academic publications and presentations.
```

### Q-Consent4
同上，选项：

```
I agree to take part in this study.
```

**（可选但推荐）**：在Consent1题目文本框那句话前面，可以再加一句并附上PIS链接，方便参与者不用翻回上一页确认：

```
As a reminder, you can review the Participant Information Sheet here: [链接同Welcome页那个PIS链接]

Please confirm the following before continuing:
```

---

## 3. Block 3 — Background

**操作**：新建block，命名为 `Background`。共5道题。

### Q-B1
- **Question Type**：`Multiple Choice`，Selector：**Single Answer**（标准单选圆点）
- **Question Text**：

  ```
  How familiar are you with Edinburgh's literary history (e.g. Sir Walter Scott, Robert Louis Stevenson, contemporary Edinburgh fiction)?
  ```

- **Answer Choices**（5个，一行一个直接粘贴——Qualtrics会自动把每一行拆成一个选项）：

  ```
  Not at all familiar
  Slightly familiar
  Moderately familiar
  Very familiar
  Extremely familiar
  ```

- **设置**：Force Response On；**不要**打开"Randomize Answer Order"（选项顺序必须保持从"不熟悉"到"非常熟悉"的固定顺序）

### Q-B2
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Have you read any works by these authors: Alexander McCall Smith, Irvine Welsh, John Gibson Lockhart, Walter Scott, or Robert Louis Stevenson?
  ```

- **Answer Choices**：

  ```
  Yes, several
  Yes, one or two
  No
  ```

- Force Response On

### Q-B3
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  How would you best describe your background?
  ```

- **Answer Choices**：

  ```
  Literary studies / English literature
  Digital humanities
  Information visualisation / HCI / Computer Science
  Other academic background
  General public, no specialist background in the above
  Other (please specify)
  ```

- **特殊设置**：最后一项"Other (please specify)"需要加一个文本输入框。点这个选项右边的三个小点（更多选项）→ **Add Text Entry**，这样参与者选中它之后会自动出现一个填空框。
- Force Response On

### Q-B4
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  How familiar are you with reading data visualisations or charts in general (e.g. bar charts, network diagrams, maps)?
  ```

- **Answer Choices**（跟B1完全一样的5点量表，直接复制）：

  ```
  Not at all familiar
  Slightly familiar
  Moderately familiar
  Very familiar
  Extremely familiar
  ```

- Force Response On

### Q-B5
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Have you lived in or spent significant time in Edinburgh?
  ```

- **Answer Choices**：

  ```
  Yes, I live/have lived there
  I've visited several times
  I've visited once or twice
  Never
  ```

- Force Response On

---

## 4. Block 4 — Part 1 Instructions

**操作**：新建block，命名为 `Part 1 Instructions`。只有1道纯说明题。

### Q-Part1Intro
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Part 1: Author Fingerprints

  Each of the next three visualisations shows five authors' individual "fingerprints" — how each of them distributes place names across Edinburgh in their writing. For each one, you'll first see all five authors' fingerprints together, each labelled with the author's name. Take a few minutes to look at them and get a feel for how each author's pattern differs from the others — there's no trick to look for, just notice whatever stands out to you.

  Then we'll show you one of those five fingerprints again on its own, with the name hidden, and ask which author you think it is, based on the pattern you just looked at. You're welcome to go back and check the labelled view again before answering — this isn't a memory test.

  Please open each link in a new browser tab, and come back to this page to answer.
  ```

- 不需要Force Response

---

## 5. Block 5/6/7 — Fingerprint Tasks ×3

**这里要建三个独立的block**，因为每个设计要放不同的链接。三个block内部的结构完全一样，只有链接不同。

**⚠️ 每个block内部分两步，中间要插一个Page Break：**
1. **Step 1（参考版）**：先给原版链接（`radar.html`/`barcode.html`/`small_multiples.html`，5位作者都标真名），让参与者自己观察、总结每个作者的图形有什么不一样——这一步不设问题，纯展示。
2. **（插入Page Break）**
3. **Step 2（盲测版）**：再给`_task.html`结尾的单作者盲测链接，回答F1-F4。

**为什么要分两步**：如果只给盲测版，参与者是在对一个从没见过任何参照的陌生人名字凭空瞎猜，对不了解这几位作者的人来说这个任务没有意义——这是2026年8月9日发现并修正的问题。现在先让参与者看5人都标名字的参考版、自己总结规律，再看去掉名字的盲测版尝试识别，测的是"图形本身能不能承载可学习、可辨认的特征"，不再要求参与者本来就认识这几位作者。

### Block 5 — 命名为 `Fingerprint - Radar`

#### Q-FP-Radar-Reference
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Step 1: Take a few minutes to compare all five authors' fingerprints below.
  ```

  插入超链接，显示文字 `Open reference view →`，链接地址（**这个是原版，5人都标名字**）：

  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/radar/d3/radar.html
  ```

- 不需要Force Response

**➡️ 在这道题后面插入一个Page Break**（题目编辑界面右上角有"Add Page Break"选项，或者在Survey Flow里对应位置插入）。Page Break前后仍然算同一个block，只是分成两屏，参与者必须先经过Step 1这一屏才能翻到Step 2。

#### Q-FP-Radar-Blind
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Step 2: Now look at one of those five fingerprints again on its own, with the name hidden. The reference view from Step 1 is still open in your other tab if you want to check it again.
  ```

  插入超链接，显示文字 `Open this one →`，链接地址（**这个是盲测版，只有1个作者、不显示名字**）：

  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/radar_task.html
  ```

#### Q-FP-Radar-F1
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Which of the following five authors do you think this represents?
  ```

- **Answer Choices**：

  ```
  Alexander McCall Smith
  Irvine Welsh
  John Gibson Lockhart
  Walter Scott
  Robert Louis Stevenson
  I don't know
  ```

- Force Response On；不要随机化选项顺序

#### Q-FP-Radar-F2
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  How confident are you in this answer?
  ```

- **Answer Choices**：

  ```
  Not at all confident
  Slightly confident
  Moderately confident
  Confident
  Very confident
  ```

- Force Response On

#### Q-FP-Radar-F3
- **Question Type**：`Text Entry`，格式选 **Essay**（多行文本框，右侧"Content Type"或题目下拉里选）
- **Question Text**：

  ```
  What specific feature of the shape led you to that answer? (for example, an unusually large spike in one area, or a shape that's spread evenly across many areas)
  ```

- Force Response On

#### Q-FP-Radar-F4
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  If no one had told you anything about this visualisation, would you have understood how to read it just by looking?
  ```

- **Answer Choices**：

  ```
  Yes, easily
  Yes, with a little effort
  No, I was confused about how to read it
  ```

- Force Response On

---

### Block 6 — 命名为 `Fingerprint - Barcode`

跟Block 5完全相同的结构（Reference → Page Break → Blind + F1-F4，文字一字不改），**唯一区别是两个链接**：

- Step 1参考版：
  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/barcode/d3/barcode.html
  ```
- Step 2盲测版：
  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/barcode_task.html
  ```

---

### Block 7 — 命名为 `Fingerprint - Small Multiples`

同样的结构，**唯一区别是两个链接**：

- Step 1参考版：
  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_1/small_multiples/d3/small_multiples.html
  ```
- Step 2盲测版：
  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/ethics/study_stimuli/small_multiples_task.html
  ```

**省时间小技巧**：与其把Block 5的两个链接问题、Page Break、F1-F4重新搭一遍，不如在Block列表里对Block 5点右键（或三个点菜单）选 **Copy Block**，复制出Block 6和Block 7（Page Break会一起被复制），再进去只改两个链接和block名字，其余全部不用动。

---

## 6. Block 8 — Fingerprint Ranking

**操作**：新建block，命名为 `Fingerprint Ranking`。这个block在Survey Flow里要放在三个Fingerprint block**之后**（不在Randomizer里面，是固定顺序，见第13节）。

### Q-FPRank
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Having now seen all three, which did you find the most intuitive to read without any explanation?
  ```

- **Answer Choices**：

  ```
  Radar chart
  Bar-code
  Small multiples (maps)
  ```

- Force Response On

### Q-FPRank-Why
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Why? (optional)
  ```

- Force Response **Off**（可选题）

---

## 7. Block 9 — Part 2 Instructions

**操作**：新建block，命名为 `Part 2 Instructions`。

### Q-Part2Intro
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Part 2: Place Connections

  Now you'll see three different visualisations showing how places mentioned in Edinburgh literature relate to each other. Before answering, take a moment to explore each one freely — hover over places, click on them, zoom or scroll if the design allows. There's no need for any special knowledge of Edinburgh.
  ```

- 不需要Force Response

---

## 8. Block 10/11/12 — Topology Tasks ×3

同样是三个独立block，结构完全一样，只有链接不同。

### Block 10 — 命名为 `Topology - Network`

#### Q-TP-Network-Link
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Please open the visualisation below in a new tab. Take a minute to explore freely before answering.
  ```

  插入超链接，显示文字 `Open visualisation →`，地址：

  ```
  https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/network/d3/network.html
  ```

#### Q-TP-Network-T1
- **Question Type**：`Text Entry`，格式选 **Form**（这个格式可以在一道题里放两个带标签的填空框）
- **Question Text**：

  ```
  Which two places appear to be the most strongly connected?
  ```

- 在Form的两行标签里分别填：
  - 第一行标签：`Place A`
  - 第二行标签：`Place B`
- Force Response On

#### Q-TP-Network-T2
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Based on your own knowledge of Edinburgh (or your best guess if you're not familiar with the city), are these two places geographically close together or far apart?
  ```

- **Answer Choices**（注意"Not sure"放在中间，顺序不要打乱）：

  ```
  Very close
  Somewhat close
  Not sure
  Somewhat far
  Very far
  ```

- Force Response On

#### Q-TP-Network-T3
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Beyond that pair, is there any other connection in this visualisation that surprises you — for example, two places that seem strongly linked even though you'd expect them to be unrelated, or two places you'd expect to be linked that don't appear connected at all? Name the places and briefly explain what surprised you.
  ```

- Force Response **Off**（可选，但题目文字里"encouraged"的鼓励语气可以直接体现在题目文本里，见下方备注）
- **备注**：如果想更贴近问卷正本的语气，可以在题目文字末尾加一句：`(optional, but we'd love to hear your thoughts)`

#### Q-TP-Network-T4
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Do you notice any group of three or more places that seem to form a cluster of connections with each other? If so, list them and, if you have a guess, why you think they might be grouped together.
  ```

- Force Response Off

#### Q-TP-Network-T5
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  If no one had told you anything about this visualisation, would you have understood how to read it just by looking?
  ```

- **Answer Choices**：

  ```
  Yes, easily
  Yes, with a little effort
  No, I was confused about how to read it
  ```

- Force Response On

---

### Block 11 — 命名为 `Topology - Linear`

跟Block 10完全一样的5道题（T1-T5文字直接复制），**唯一区别是链接**：

```
https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/linear/d3/linear.html
```

### Block 12 — 命名为 `Topology - Metro`

同样5道题，**唯一区别是链接**：

```
https://merrittw-1307.github.io/uoe-edinburgh-literary-geovis/data/processed/dir_2/metro/d3/metro.html
```

**同样建议用 Copy Block 复制Block 10两次，只改链接和block名字。**

---

## 9. Block 13 — Cross-design Synthesis

**操作**：新建block，命名为 `Cross-design Synthesis`。这是整份问卷里专门用来捕捉自发深度发现的关键一题，放在三个Topology block**之后**（固定顺序，不在Randomizer里）。

### Q-CrossSynthesis
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Having now seen all three ways of showing connections between places, is there anything about Edinburgh's literary geography that surprised you, or that you hadn't thought about before — for example, places that seem to "belong together" in these authors' writing that you wouldn't have expected?
  ```

- Force Response Off（鼓励但不强制）

---

## 10. Block 14 — Topology Ranking

**操作**：新建block，命名为 `Topology Ranking`。

### Q-TopoRank
- **Question Type**：`Multiple Choice`，Single Answer
- **Question Text**：

  ```
  Having now seen all three, which did you find the most intuitive to read without any explanation?
  ```

- **Answer Choices**：

  ```
  Force-directed network
  Linear connection diagram
  Metro-style map
  ```

- Force Response On

### Q-TopoRank-Why
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Why? (optional)
  ```

- Force Response Off

---

## 11. Block 15 — Reflection

**操作**：新建block，命名为 `Reflection`。共5道题。

### Q-R1
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Before this study, had you thought about literary place names as anything other than locations on a map?
  ```

- Force Response On

### Q-R2
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Did any of the six visualisations change how you think about the relationship between a literary work and the real city it's set in? If so, which one, and how?
  ```

- Force Response On

### Q-R3
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Is there anything about any of the six visualisations that confused you, or that you would change?
  ```

- Force Response On

### Q-R4
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Any other comments?
  ```

- Force Response Off（这道纯粹是开放收尾，不强制）

### Q-R5
- **Question Type**：`Text Entry`，Essay
- **Question Text**：

  ```
  Overall, which single visualisation (of all six) did you find the most memorable or interesting, and why?
  ```

- Force Response On

---

## 12. Block 16 — Debrief

**操作**：新建block，命名为 `Debrief`。这是最后一个block。

### Q-Debrief
- **Question Type**：`Text/Graphic`
- **Question Text**：

  ```
  Thank you!

  That's everything — thank you very much for your time and thoughtful answers. Your responses will help improve how literary geography is visualised for future audiences.

  If you have any questions about this study, contact the lead researcher, Uta Hinrichs (uhinrich@ed.ac.uk).
  ```

### Q-Email
- **Question Type**：`Text Entry`，格式选 **Single Line**
- **Question Text**：

  ```
  (Optional) If you'd like a short summary of the results once the study is complete, leave your email below. This will be stored separately from your survey answers and will not be linked to them.
  ```

- Force Response Off
- **建议**：右侧 Validation 里可以选 "Content Type: Email"，让Qualtrics自动检查格式是否像邮箱（不是必须，但更保险）

---

## 13. Survey Flow 设置（两处随机顺序）

**这一步在左侧菜单点 "Survey Flow"（不是Blocks视图）进入。**

Qualtrics默认会把你建好的16个block按建立顺序自上而下排列，这本身就是对的顺序——你**不需要**手动重新排列，只需要在两个地方插入"Randomizer"元素，把对应的3个block框进去：

### 第一处随机化：Fingerprint Tasks

1. 找到 `Fingerprint - Radar` / `Fingerprint - Barcode` / `Fingerprint - Small Multiples` 这三个block在Survey Flow里的位置（应该是连续的三个，紧跟在 `Part 1 Instructions` 后面）。
2. 在这三个block最上面那个的**前面**，点 "Add a New Element Here" → 选 **Randomizer**。
3. 会生成一个空的Randomizer容器框。把刚才那三个block**拖拽进这个框里**（鼠标按住block左边的移动手柄图标拖动）。
4. 点Randomizer框上的设置，确认 "Randomly present X of the following Elements" 里的 X 填的是 **3**（表示三个全部展示，只是顺序打乱，不是抽样展示其中几个）。

### 第二处随机化：Topology Tasks

对 `Topology - Network` / `Topology - Linear` / `Topology - Metro` 这三个block重复完全一样的操作：加一个Randomizer，把三个block拖进去，X设为3。

### 检查最终顺序

设置完之后，Survey Flow从上到下应该长这样：

```
Welcome
Consent
Background
Part 1 Instructions
[Randomizer: 3 of 3 — Fingerprint-Radar / Fingerprint-Barcode / Fingerprint-SmallMultiples]
Fingerprint Ranking
Part 2 Instructions
[Randomizer: 3 of 3 — Topology-Network / Topology-Linear / Topology-Metro]
Cross-design Synthesis
Topology Ranking
Reflection
Debrief
```

其余部分**不需要任何跳转逻辑（Skip Logic）或分支（Branch）**——因为Consent那四道必答题已经从根本上保证了不同意的人无法继续往下走。

---

## 14. 全局设置（Survey Options）

点右上角 **Survey Options**（齿轮图标），检查/设置以下几项：

- **Survey Termination**：把默认的"结束语"改成尽量简短，或者留空——因为咱们自己的 `Debrief` block已经包含完整的感谢语，不需要Qualtrics再弹一个重复的默认感谢页。
- **Security → Anonymize Responses**：打开。这跟PIS和伦理申请里"数据最小化"的承诺一致——不记录IP地址等可识别信息。
- **General → Back Button**：建议打开，让参与者可以往回改之前的答案（更友好，不强制）。
- **General → Progress Bar**：建议开启，选 "Text"（显示"还剩几题"或百分比），让46题的问卷显得没那么令人却步。

---

## 15. 发布前自查清单

正式点 **Publish** 之前，务必自己完整走一遍 **Preview**（预览模式），逐项确认：

- [ ] 16个block全部按顺序出现，两处Randomizer确实在打乱顺序（多刷新预览几次看看顺序有没有变）
- [ ] 六个可视化链接点开都是正确的页面，且都在新标签页打开（不是跳转覆盖掉问卷页面）
- [ ] **重点检查**：三个Fingerprint block（5/6/7）里，Step 1参考版链接打开后应该看到**5种颜色/5行/5张地图，图例上5个真名都在**；Step 2盲测版链接（`_task.html`结尾）打开后应该看到**只有1个图形/1行/1张地图，完全没有图例、没有作者名字**——这两个反过来就麻烦了（参考版如果只显示1个作者，参与者就没法自主总结规律；盲测版如果显示5个名字，F1这题就直接被剧透了）。三个Topology链接（`network.html`/`linear.html`/`metro.html`）打开后应该是**5位作者合并的完整数据**，这个不用区分参考/盲测，本来就只有一种版本
- [ ] Fingerprint每个block里，Step 1和Step 2之间的Page Break生效了——预览时确认看完参考版点Next会翻到新的一屏才看到盲测版链接，不是所有内容挤在同一屏
- [ ] Consent页四个复选框不勾选、直接点Next，确认页面**不会**往下走（会提示"请完成必答题"）
- [ ] T1那道"Place A / Place B"的双填空框显示正常
- [ ] B3的"Other (please specify)"选中后确实弹出了填空框
- [ ] 从头到尾自己填一遍，看总用时是否落在35-50分钟区间（如果太快，说明填得太随意，正常参与者会更慢；这一步主要是确认题目数量和长度感觉对不对）
- [ ] 预览完成后回到 Data & Analysis，**删除你自己这条预览/测试产生的记录**，避免混进正式数据

全部确认无误后，点 **Publish**，然后去 **Distributions** 标签页 → **Anonymous Link**，复制生成的链接——这就是要发给参与者、以及明天要发给Uta的那个问卷链接。

---

## 遇到问题怎么办

如果某个具体按钮的位置跟这份文档描述的不完全一样（Qualtrics偶尔会小改界面），去Qualtrics右下角的 **Help & Feedback** 或者直接搜"Qualtrics + 你卡住的那个功能名字"（比如"Qualtrics randomizer block order"、"Qualtrics add text entry to choice"），官方支持文档写得很详细，这份手册里用的功能名字（Randomizer、Force Response、Text/Graphic、Multiple Answer、Add Text Entry、Form）都是Qualtrics官方术语，搜索这些词能直接找到对应的官方教程。
