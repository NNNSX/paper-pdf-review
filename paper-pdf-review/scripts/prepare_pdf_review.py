#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


SECTION_RE = re.compile(r"^(Abstract|Index Terms|[IVX]+\.\s|[A-Z]\.\s|REFERENCES|ACKNOWLEDG|CONCLUSION|Conclusion)\b")
FIGTAB_RE = re.compile(r"\b(Fig\.|Figure|TABLE|Table)\s*[IVX0-9]+", re.IGNORECASE)
FORMULA_RE = re.compile(r"(\([0-9]{1,3}\)|\\sum|\\min|\\max|=|∑|≤|≥|∈|κ|σ|ϕ|θ|ψ)")
STRONG_CLAIM_RE = re.compile(
    r"\b(significant|significantly|superior|best|outperform|outperforms|outperformed|"
    r"state-of-the-art|SOTA|all|every|always|prove|proved|proves|"
    r"consistently|robust|remarkably|comprehensive)\b",
    re.IGNORECASE,
)
WEAK_CLAIM_RE = re.compile(
    r"\b(demonstrate|demonstrates|demonstrated|efficient|average|up to|only|"
    r"substantially|clearly|notably|stable|stability)\b",
    re.IGNORECASE,
)
NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?\s*(?:dB|ms|MB|M|%|percent|fps|frames per second|×|x)?")


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def extract_with_pypdf2(pdf: Path, out_dir: Path):
    try:
        from PyPDF2 import PdfReader
    except Exception as exc:
        return None, f"PyPDF2 unavailable: {exc}"

    try:
        reader = PdfReader(str(pdf))
        pages = []
        page_dir = out_dir / "pages"
        page_dir.mkdir(parents=True, exist_ok=True)
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(text)
            (page_dir / f"page_{i:03d}.txt").write_text(text, encoding="utf-8")
        full_text = "\n\n".join(f"===== PAGE {i} =====\n{text}" for i, text in enumerate(pages, start=1))
        (out_dir / "full_text.txt").write_text(full_text, encoding="utf-8")
        return {"page_count": len(pages), "pages": pages, "metadata": dict(reader.metadata or {})}, None
    except Exception as exc:
        return None, f"PyPDF2 extraction failed: {exc}"


def render_pages_best_effort(pdf: Path, out_dir: Path, page_count: int):
    image_dir = out_dir / "page_images"
    image_dir.mkdir(parents=True, exist_ok=True)
    notes = []

    if have("gs"):
        pattern = image_dir / "page_%03d.png"
        result = run(
            [
                "gs",
                "-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=png16m",
                "-r180",
                f"-sOutputFile={pattern}",
                str(pdf),
            ]
        )
        produced = sorted(image_dir.glob("page_*.png"))
        notes.append(f"ghostscript exit={result.returncode}; rendered pages={len(produced)}")
        if result.returncode == 0 and produced:
            return notes
        if result.stderr.strip():
            notes.append("ghostscript stderr: " + result.stderr.strip().splitlines()[-1])

    if have("qlmanage"):
        ql_out = out_dir / "quicklook"
        ql_out.mkdir(exist_ok=True)
        result = run(["qlmanage", "-t", "-s", "1800", "-o", str(ql_out), str(pdf)])
        notes.append(f"qlmanage exit={result.returncode}")
        produced = list(ql_out.glob("*.png"))
        if produced:
            target = image_dir / "quicklook_thumbnail.png"
            shutil.copyfile(produced[0], target)
            notes.append(f"quicklook thumbnail: {target}")
        if result.stderr.strip():
            notes.append("qlmanage stderr: " + result.stderr.strip().splitlines()[-1])

    if have("sips"):
        # sips cannot reliably rasterize all PDF pages, but it is useful to record availability.
        notes.append("sips available; use it manually for image conversion when a page image exists.")

    if not any(image_dir.iterdir()):
        notes.append("No page images generated. Use external rasterization tools such as pdftoppm, mutool, or Acrobat export.")

    return notes


def inventory_pages(pages):
    rows = []
    for i, text in enumerate(pages, start=1):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        sections = [ln for ln in lines if SECTION_RE.search(ln)]
        figtabs = [ln for ln in lines if FIGTAB_RE.search(ln)]
        formula_hits = [ln for ln in lines if FORMULA_RE.search(ln)]
        strong_claim_hits = [ln for ln in lines if STRONG_CLAIM_RE.search(ln)]
        weak_claim_hits = [ln for ln in lines if WEAK_CLAIM_RE.search(ln)]
        numbers = NUMBER_RE.findall(text)
        rows.append(
            {
                "page": i,
                "chars": len(text),
                "sections": sections[:8],
                "figtabs": figtabs[:10],
                "formula_count": len(formula_hits),
                "strong_claim_count": len(strong_claim_hits),
                "weak_claim_count": len(weak_claim_hits),
                "number_count": len(numbers),
            }
        )
    return rows


def visual_queue(inventory, page_count):
    pages = {1, page_count} if page_count else set()
    for row in inventory:
        if row["figtabs"] or row["formula_count"] >= 8 or row["number_count"] >= 50 or row["strong_claim_count"] >= 4:
            pages.add(row["page"])
    return sorted(p for p in pages if p)


def write_index(pdf: Path, out_dir: Path, extraction, extraction_error, render_notes, include_metadata=False):
    pages = extraction["pages"] if extraction else []
    inventory = inventory_pages(pages) if pages else []
    page_count = extraction["page_count"] if extraction else 0
    queue = visual_queue(inventory, page_count)
    manifest = {
        "pdf_file": pdf.name,
        "page_count": page_count,
        "render_notes": render_notes,
        "visual_inspection_queue": queue,
        "pages": inventory,
    }
    if include_metadata and extraction:
        manifest["metadata"] = extraction.get("metadata", {})
    (out_dir / "page_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = []
    lines.append(f"# PDF Review Bundle: {pdf.name}")
    lines.append("")
    lines.append("## Tool Availability")
    for cmd in ["pdfinfo", "pdftotext", "pdftoppm", "mutool", "gs", "qlmanage", "sips"]:
        lines.append(f"- {cmd}: {'yes' if have(cmd) else 'no'}")
    lines.append(f"- PyPDF2 extraction: {'yes' if extraction else 'no'}")
    if extraction_error:
        lines.append(f"- extraction error: {extraction_error}")
    lines.append("")
    lines.append("## Metadata")
    if extraction:
        lines.append(f"- pages: {extraction['page_count']}")
        if include_metadata:
            for k, v in extraction.get("metadata", {}).items():
                lines.append(f"- {k}: {v}")
        else:
            lines.append("- PDF metadata: redacted by default; rerun with `--include-metadata` if needed.")
    else:
        lines.append("- unavailable")
    lines.append("")
    lines.append("## Render Notes")
    for note in render_notes:
        lines.append(f"- {note}")
    lines.append("")
    lines.append("## Visual Inspection Queue")
    lines.append("")
    if queue:
        lines.append("Inspect these PNG pages before writing findings about figures, formulas, tables, numeric claims, layout, or conclusion scope:")
        lines.append("")
        for p in queue:
            image = Path("page_images") / f"page_{p:03d}.png"
            reason = []
            row = next((r for r in inventory if r["page"] == p), None)
            if p == 1:
                reason.append("title/abstract")
            if p == page_count:
                reason.append("last page/references")
            if row:
                if row["figtabs"]:
                    reason.append("figure/table candidates")
                if row["formula_count"] >= 8:
                    reason.append("formula-dense")
                if row["number_count"] >= 50:
                    reason.append("numeric-dense")
                if row["strong_claim_count"] >= 4:
                    reason.append("strong-claim-dense")
            lines.append(f"- Page {p}: `{image}` ({', '.join(reason)})")
    else:
        lines.append("- No queue generated because text extraction failed; inspect rendered pages manually.")
    lines.append("")
    lines.append("## Text-PNG Cross-Check Rules")
    lines.append("")
    lines.append("- Use text to locate claims, captions, formulas, and numbers.")
    lines.append("- Use PNG pages to verify visual layout, actual plots/tables/formulas, labels, legends, and readability.")
    lines.append("- Mark findings as text / PNG / text+PNG / source data unavailable.")
    lines.append("- Do not make figure, table, formula, or layout findings from text extraction alone.")
    lines.append("")
    lines.append("## Page Inventory")
    lines.append("")
    lines.append("| Page | Chars | Figures/Tables | Formula hits | Strong claims | Weak hints | Numbers | Sections |")
    lines.append("|---:|---:|---|---:|---:|---:|---:|---|")
    for row in inventory:
        figtabs = "<br>".join(row["figtabs"]).replace("|", "\\|")
        sections = "<br>".join(row["sections"]).replace("|", "\\|")
        lines.append(
            f"| {row['page']} | {row['chars']} | {figtabs} | {row['formula_count']} | "
            f"{row['strong_claim_count']} | {row['weak_claim_count']} | {row['number_count']} | {sections} |"
        )
    lines.append("")
    lines.append("## Strong Claim Lines")
    lines.append("")
    for i, text in enumerate(pages, start=1):
        for ln in text.splitlines():
            if STRONG_CLAIM_RE.search(ln):
                lines.append(f"- Page {i}: {ln.strip()}")
    lines.append("")
    lines.append("## Weak Claim Hint Lines")
    lines.append("")
    for i, text in enumerate(pages, start=1):
        for ln in text.splitlines():
            if WEAK_CLAIM_RE.search(ln):
                lines.append(f"- Page {i}: {ln.strip()}")
    lines.append("")
    lines.append("## Figure/Table Candidate Lines")
    lines.append("")
    for i, text in enumerate(pages, start=1):
        for ln in text.splitlines():
            if FIGTAB_RE.search(ln):
                lines.append(f"- Page {i}: {ln.strip()}")
    lines.append("")
    lines.append("## Required Manual Checks")
    lines.append("")
    lines.append("- Inspect page images for all figure/table pages. If only a Quick Look thumbnail exists, generate full page images externally.")
    lines.append("- Compare extracted text against PDF visual layout before citing exact wording.")
    lines.append("- Use original LaTeX/log/CSV/plot scripts for data authenticity and exact formula/table source tracing.")
    (out_dir / "review_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Prepare a multi-channel review bundle for a research-paper PDF.")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--include-metadata",
        action="store_true",
        help="Include raw PDF metadata in the generated manifest and index. Default omits it for privacy.",
    )
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")
    out_dir = args.out or (Path.cwd() / f"{pdf.stem}_pdf_review")
    out_dir.mkdir(parents=True, exist_ok=True)

    extraction, extraction_error = extract_with_pypdf2(pdf, out_dir)
    page_count = extraction["page_count"] if extraction else 0
    render_notes = render_pages_best_effort(pdf, out_dir, page_count)
    write_index(pdf, out_dir, extraction, extraction_error, render_notes, include_metadata=args.include_metadata)
    print(out_dir)


if __name__ == "__main__":
    main()
