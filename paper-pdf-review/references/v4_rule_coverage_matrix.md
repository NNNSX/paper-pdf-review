# V4 Rule Coverage Matrix

This is a compact routing checklist derived from a local extended paper-writing and data-reuse audit rule set. It does not replace the full rules file. Always read the full user-specified/local rules file first when available.

For each row, mark one of:

```text
checked: issue found
checked: no major issue found
not checked: missing material
not applicable
```

## 1. 论证链与语言克制

- 主线是否完整：现实问题 -> 现有缺口 -> 核心挑战 -> 方法设计 -> 实验验证 -> 机制解释 -> 边界意义。
- 每段是否说明解决什么问题、如何衔接、支撑哪项贡献。
- 是否存在 `prove / fully solve / completely eliminate / clearly verify / superior / remarkably / comprehensive / significantly` 等强词且无证据。
- 是否使用 `suggests / indicates / is consistent with` 等边界表达处理推断。

## 2. 摘要、引言与贡献

- 摘要是否包含背景/问题、具体缺口、方法一句话、关键机制、主要实验结论、意义。
- 摘要是否出现未经正文支撑的数值或强结论。
- 缩写是否首次给出全称。
- 引言是否从场景和问题进入，而不是直接堆技术。
- 现有方法是否按逻辑分组，并说明各自解决什么和留下什么缺口。
- 贡献项是否具体、可核查，并对应方法/公式/图/实验。
- 贡献是否存在重叠、泛化、首创性过度宣传。

## 3. 相关工作

- 是否按方向/技术脉络分组，而不是逐篇罗列。
- 每组文献后是否有判断和边界。
- 是否公平评价已有工作，不贬低。
- 是否清楚说明本文与最相关工作的区别。
- 是否避免和引言重复。

## 4. 方法与公式

- 每个模块是否有动机、输入、输出、与前后模块接口、设计理由。
- 是否避免写成代码说明书。
- 公式前是否说明建模目的，公式后是否解释算法作用。
- 符号是否首次定义，字体/上下标/维度是否一致。
- 损失项、指标、表格列名是否在方法或实验设置中定义。
- 算法、公式、图中符号是否一致。
- 理论解释是否有证明；没有证明时是否降级为解释或直觉。

## 5. 实验叙事

- 每个实验是否按目的 -> 设置/指标 -> 结果 -> 机制解释 -> 贡献关系展开。
- 安全性/效率/消融/诊断实验是否明确攻击假设、硬件、输入规模、统计方式、目的和边界。
- 是否把诊断实验写成主实验结论。
- 是否把单数据集、单 seed、单图样例写成普遍规律。
- 是否说明负向结果、局部反转、trade-off。

## 6. 数据来源与数据复用审计

- 每个关键数值是否能回答：从哪里来、按什么协议得到、是否正确转写、是否支撑当前结论。
- 数值来源是否标为 S1/S2/S3/S4 或等价说明。
- 主实验是否优先使用本文实验原始输出或整理表。
- 外部 baseline 是否区分 reported/reproduced/ours。
- 表格是否检查旧数据残留、旧分析残留、行列错位、方法名错配、指标方向错配、单位错配。
- Average/Mean/Std/Gain/Reduction/Speedup/BDBR/BD-rate/Rank 是否可复算。
- 加粗、下划线、best/second-best 是否与当前表格一致。
- 摘要、贡献、正文、图注、结论、回复稿/补充材料中的同一数值是否同步。

## 7. 内联数字与强断言

- 每个正文内联数值是否能定位到表格、图、公式、日志或参考论文位置。
- `outperforms / improves / reduces / achieves the best` 是否有比较对象和对应数值。
- `average` 是否说明平均范围。
- `highest / lowest / best` 是否检查全表全图。
- `all / each / every / consistently` 是否检查所有设置。
- `significant` 是否有统计检验、多 seed 或明确量级；否则降级。
- `up to` 是否确认最大提升来源。
- `comparable / close / slight` 是否有差距或阈值。

## 8. 图表

- 每个图表是否承担明确论证功能。
- Caption 是否自解释：比较对象、关键指标、子图含义、关注现象。
- 正文是否解释图表验证什么，而非只说 `Table X shows`。
- 图中标签、legend、caption、正文术语是否一致。
- 表头单位、指标方向、加粗规则是否一致。
- 曲线图横纵轴、单位、legend、平滑/log/归一化/误差棒是否说明。
- 图中趋势是否与表格和正文一致。
- 定性样例是否说明数据集、设置、trial 选择规则；是否避免只挑有利样例。
- 页面视觉是否有表格过密、图中文字过小、caption 太近、异常空白、符号异常。

## 9. 术语、缩写、引用与 LaTeX

- 核心缩写是否首次出现写全称。
- 同一概念全文术语是否一致。
- 图、表、公式、章节、文献是否使用可维护交叉引用，避免硬编码编号。
- 指标单位是否统一，例如 dB、ms、MB、bpp、bits/token。
- 特殊符号是否在 LaTeX 中稳定表达。
- Clean/Tracked 版是否分别满足修订标记要求（如适用）。

## 10. AI 味与写作风格

- 是否存在空泛句、模板连接词、过长句、机械 `not only...but also`。
- 是否存在可放入任何论文的泛化段落。
- 是否用具体数据、机制或图表替代抽象评价。
- 是否保留真实研究边界和取舍。

## 11. 参考文献与外部数据

- 文献是否真实、相关、格式统一。
- 新增文献是否核查题名、作者、会议/期刊、年份、页码/DOI/arXiv。
- 定量引用是否来自原始论文具体 Table/Figure/Appendix，而不是二次转引。
- arXiv、会议版、期刊扩展版、README 是否版本一致。
- 指标定义、数据集、预处理、评价脚本、模型规模、硬件是否与本文可比。
- 若协议不同，是否标注 contextual/reported，不写公平比较。

## 12. 回复稿、补充材料与最终提交

- 若存在回复稿：每条回复是否闭环，包含问题理解、修改、结果、论文位置、摘录。
- 回复稿中的图号、表号、章节号、数值是否与论文最终版一致。
- 主文、补充材料、appendix、PPT/答辩材料中的关键数值是否一致。
- 最终 PDF 是否视觉检查通过。

## Required Output Addendum

End the review with:

```text
Coverage summary:
- Full rules file read: yes/no, path:
- Text layer checked: yes/no
- PNG pages checked: yes/no, pages:
- Formula-symbol consistency checked: yes/no
- Figure/table visual consistency checked: yes/no
- Data reuse audit completed: yes/no/partial
- Reference metadata checked: yes/no/partial
- Missing materials limiting review:
```
