---
name: paper-pdf-review
description: "Review research-paper PDFs with multi-channel reading: extracted text, page/figure visual inspection, formulas, tables, data-reuse consistency, writing quality, and compliance with local thesis/paper writing rules. Use when Codex is asked to read,审查, audit, review, revise, or diagnose a PDF paper, especially when figures, formulas, tables, captions, experimental claims, or data provenance must be checked."
---

# Paper PDF Review

Use this skill for serious research-paper PDF review. Do not rely on a text-only PDF extraction when the user asks for writing quality, figures, formulas, layout, or data consistency. Always state which channels were actually inspected.

## Required Workflow

1. Locate the PDF and the applicable writing-rules file. Prefer the user-specified rules file; otherwise search the current workspace for local paper/thesis writing-rule documents and read the newest applicable version completely before reviewing. The skill checklist is only a routing index; the external rules file is authoritative.
2. Run `scripts/prepare_pdf_review.py` on the PDF to create a review bundle.
3. Read `references/v4_rule_coverage_matrix.md` to make sure the full v4 rule surface is covered, then read the generated `review_index.md`, extracted text, page-level notes, and visual inspection queue.
4. Inspect page images for the title page, all figure/table pages, formula-dense pages, dense numeric-result pages, conclusion page, and any page mentioned by the user.
5. Complete the coverage matrix. If a section cannot be checked because source data, LaTeX, logs, BibTeX, response letters, or supplementary files are missing, mark it as `not checked: missing material` rather than silently skipping it.
6. Cross-check text and PNG before making findings:
   - Text says a figure/table/formula exists -> verify it in the page PNG.
   - PNG shows labels/curves/tables/formulas -> verify the caption and正文 explain them.
   - Text-extracted numbers/formulas -> verify visually when they support a finding.
   - Visual layout issues -> do not infer from text extraction alone.
7. Produce a review with separate sections:
   - 内容写作审查
   - 图与表审查
   - 公式与符号审查
   - 实验与数据复用审计
   - 文献与外部 baseline 审查
   - AI 味与语言克制审查
   - 回复稿/补充材料同步审查
   - 版式与可读性审查
   - 优先修改清单
   - 未能核查/需要原始材料确认

If page images cannot be generated, say so and downgrade figure/layout findings to `待视觉核查`. If raw logs, CSV, source LaTeX, or plotting scripts are absent, say that data authenticity and exact source tracing remain unverified.

## Review Bundle Script

Run:

```bash
python3 paper-pdf-review/scripts/prepare_pdf_review.py path/to/paper.pdf --out path/to/output_dir
```

The script attempts to create a review bundle. It avoids writing raw PDF metadata and absolute input paths by default; use `--include-metadata` only when metadata is needed for the review and safe to retain.

- `review_index.md`: metadata, tool availability, page inventory, candidate issues.
- `full_text.txt`: extracted text with page separators.
- `pages/page_XXX.txt`: page-level text.
- `page_images/`: rendered page images when local tools support it.
- `page_manifest.json`: structured page inventory for follow-up scripts or audits.

Use the script output as an index, not as the final review. Text extraction may split formulas, captions, hyphenated words, and two-column reading order.

## Minimum Cross-Channel Audit

For each major issue in the final report, include the evidence channel:

```text
Evidence channel: text / PNG / text+PNG / source data unavailable
```

Use `text+PNG` for findings about formulas, figures, tables, page layout, and claims tied to visible plots. Use `text` only for prose-level issues. Use `source data unavailable` for authenticity or provenance findings that require logs, CSV, LaTeX, BibTeX, or plotting scripts.

## Reading Standards

Apply the local writing rules as the primary standard. When no rule file is supplied, use these default checks:

- 论证链：问题、缺口、方法、实验、边界是否闭合。
- 摘要：是否直入问题，是否只给可支撑结论，缩写是否首次定义。
- 引言：是否从场景进入，相关方法是否按逻辑分组，贡献是否具体可核查。
- 方法：每个模块是否说明动机、输入输出、公式含义、接口关系和设计理由。
- 实验：每段是否有目的、设置、结果、机制解释和边界。
- 结论：是否复述了实验范围，而非放大成普遍结论。

For full coverage, use `references/v4_rule_coverage_matrix.md` as the checklist. Do not omit sections just because no issue is obvious; report either findings or `checked, no major issue found`.

## Figure And Table Review

For every visible figure/table page, inspect the page image when available. Check:

- Caption 是否自解释，并说明比较对象、指标、条件、读者应关注的现象。
- 正文是否引用并解释该图表，而不是只写 “Fig. X shows”。
- 图内标签、legend、子图编号、caption、正文术语是否一致。
- 曲线图是否有坐标轴、单位、刻度、legend、误差或试验次数说明。
- 架构图是否清楚显示模块边界、输入输出、数据流和设备分区。
- 定性图是否说明样例来源、信道/SNR/码率、trial 选择规则，避免只挑有利样例。
- 表格是否说明指标方向、单位、平均范围、reported/reproduced/ours 区分、缺失值规则。
- PDF 视觉上是否存在表头过密、caption 贴图、图中文字过小、符号挤压、双栏错位。

Do not treat extracted figure/table text as sufficient. The page PNG is the authority for visual readability, curve visibility, legend placement, table density, and formula layout.

## Formula And Symbol Review

Check formulas against surrounding text and algorithms:

- 公式前是否说明建模目的，公式后是否解释作用。
- 所有符号是否首次定义，大小写、粗斜体、上下标是否一致。
- active/full cases 是否区分，例如 `K` vs `κ`、train vs inference。
- 公式、算法、正文和图中变量是否同步。
- 损失函数中的每个项是否定义，并给出权重或说明在哪里设置。
- 如果出现理论解释但无证明，建议用 `suggests` / `can be viewed as` 降级。

## Data-Reuse Audit

Trigger this audit whenever the paper contains experiments, tables, curves, numeric claims, or copied baseline results.

For each key number, map:

```text
number -> table/figure/page -> source type S1/S2/S3/S4 -> protocol -> claim using it
```

Check:

- 摘要、贡献、正文、图注、结论中的数值是否一致。
- `all/best/outperform/consistent/significant/robust/efficient` 是否被数据支持。
- 平均值、提升率、下降率、速度倍数、参数压缩倍数是否可复算。
- 同一表中的数据是否混用不同 seed、checkpoint、SNR、硬件、分辨率或 trial 次数。
- 外部 baseline 是否标注 reported/reproduced/ours；协议不一致时不得写公平优于。
- 图中估读值不得当作精确表格数值。

Use tags where useful:

- `[DATA-CHECK]` source missing or not traceable.
- `[DATA-CONFLICT]` text/table/figure mismatch.
- `[PROTOCOL-MISMATCH]` comparison protocols differ.
- `[CLAIM-OVERREACH]` claim stronger than evidence.
- `[DERIVED-DATA-STALE]` average/ranking/gain may be stale.
- `[METRIC-MISMATCH]` metric definition/unit/channel differs.

## Output Style

Be concrete and actionable. Cite PDF page numbers or generated page text locations where possible. Separate confirmed findings from likely issues and tool limitations. Do not invent missing data, figure values, or baseline results.
