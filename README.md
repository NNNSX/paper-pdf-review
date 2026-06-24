# Paper PDF Review Skill

`paper-pdf-review` is a Codex skill for rigorous research-paper PDF review. It combines extracted text, rendered page images, formula/table checks, data-reuse auditing, and local writing-rule coverage to produce grounded review reports.

## What It Reviews

- Writing structure and claim scope
- Figures, tables, captions, legends, labels, and visual readability
- Formula and symbol consistency
- Experiment protocol and numeric-claim traceability
- Data reuse, baseline provenance, and protocol mismatches
- Reference metadata and external baseline comparability
- Layout, readability, and language restraint

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R paper-pdf-review ~/.codex/skills/
```

Then ask Codex to use `$paper-pdf-review` for PDF review.

## Usage

Prepare a PDF review bundle:

```bash
python3 paper-pdf-review/scripts/prepare_pdf_review.py path/to/paper.pdf --out path/to/review_bundle
```

The script creates a review bundle with extracted text, per-page text files, a page manifest, and rendered PNG pages when local PDF tools are available.

By default, generated index files avoid raw PDF metadata and absolute input paths. Use `--include-metadata` only when metadata is needed and safe to retain.

Example prompts:

```text
Use $paper-pdf-review to audit this manuscript PDF against the local writing rules.
Use $paper-pdf-review to check whether figures, captions, formulas, and numeric claims are consistent.
Use $paper-pdf-review to prepare a data-reuse and baseline-provenance audit for this PDF.
```

## Requirements

- Python 3
- `PyPDF2` for `paper-pdf-review`
- Optional but recommended: Ghostscript (`gs`) for page PNG rendering
- Optional on macOS: `qlmanage` and `sips` as fallback helpers

## Notes

These skills do not replace your full local writing rules. When a user provides or references a writing-rule document, Codex should read that file first and use the bundled references only as checklists to avoid omissions.

Generated review bundles may contain paper text and page images. Do not publish bundles unless the paper content is safe to share.

For writing and revision tasks, use the separate `paper-writing-assistant` skill repository.

## License

MIT
