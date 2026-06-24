# Research Paper Codex Skills

This repository contains two Codex skills for research-paper work:

- `paper-pdf-review`: rigorous PDF review with extracted text, rendered page images, formula/table checks, data-reuse auditing, and local writing-rule coverage.
- `paper-writing-assistant`: rule-based research-paper writing and revision from user intent, manuscript text, review reports, reviewer comments, venue requirements, and verified facts.

## Skill Split

Use `paper-pdf-review` when the primary task is finding issues in a PDF:

- Writing structure and claim scope
- Figures, tables, captions, legends, labels, and visual readability
- Formula and symbol consistency
- Experiment protocol and numeric-claim traceability
- Data reuse, baseline provenance, and protocol mismatches
- Reference metadata and external baseline comparability
- Layout, readability, and language restraint

Use `paper-writing-assistant` when the primary task is writing or revising text:

- Abstracts, introductions, contributions, related work, methods, experiments, captions, and conclusions
- Review-report findings converted into manuscript edits
- Reviewer responses and synchronized paper revisions
- Claim-strength calibration and AI-like wording removal
- Final self-checks for data-bearing claims, references, and response packages

## Install

Copy one or both skill folders into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R paper-pdf-review ~/.codex/skills/
cp -R paper-writing-assistant ~/.codex/skills/
```

Then ask Codex to use `$paper-pdf-review` for PDF review or `$paper-writing-assistant` for writing and revision.

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
Use $paper-writing-assistant to rewrite the experiment analysis from this review report and verified table values.
Use $paper-writing-assistant to draft a reviewer response and matching manuscript revision for these comments.
```

## Requirements

- Python 3
- `PyPDF2` for `paper-pdf-review`
- Optional but recommended: Ghostscript (`gs`) for page PNG rendering
- Optional on macOS: `qlmanage` and `sips` as fallback helpers

## Notes

These skills do not replace your full local writing rules. When a user provides or references a writing-rule document, Codex should read that file first and use the bundled references only as checklists to avoid omissions.

Generated review bundles may contain paper text and page images. Do not publish bundles unless the paper content is safe to share.

## License

MIT
