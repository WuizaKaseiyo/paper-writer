"""render_docx — Render synthesized paper sections to an academic .docx file.

Uses python-docx (must be installed in OMC venv: `pip install python-docx`).
Produces Times New Roman 11pt, two-column body, with proper handling of:

- Title (centered, 14pt bold)
- Authors block (centered, 11pt)
- Abstract (single-column, italics heading)
- Section headers (\\section{} → "1. Title", \\subsection{} → "1.1 Title")
- Body prose (justified, single-spaced)
- Inline citations (preserved as plain text — Word doesn't do auto-bib like LaTeX)
- Display equations (centered, italic, numbered)
- Tables (basic 3-line academic style)
- References section (single-column, hanging indent, 10pt)

This is a deliberate **subset** of academic styling — production-grade
venue-specific Word formatting (e.g. ACM templates) needs venue-supplied
.dotx files. For best fidelity to a target venue, use the LaTeX output
path instead.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

# python-docx import is deferred so the tool can be loaded by OMC's
# tool_registry without the dep installed; the actual call returns a clear
# error if missing.


@tool
def render_docx(
    sections: dict[str, str],
    output_path: str,
    title: str = "",
    authors: str = "",
    abstract: str = "",
    references: str = "",
    venue: str = "generic",
    figures: list[dict] | None = None,
) -> dict[str, Any]:
    """Render a structured paper into a Word .docx with academic styling.

    Args:
        sections: Ordered dict-like {section_name: section_body_markdown}.
            Keys become section headers in order (e.g.
            {"1. Introduction": "...", "2. Related Work": "...", ...}).
        output_path: Absolute path where the .docx will be written.
        title: Paper title (renders as centered 14pt bold).
        authors: Author block (one line per author, centered).
        abstract: Abstract text (single-column, italicized heading).
        references: References section body (one ref per line, hanging
            indent). Pre-formatted by the LLM; this tool does NOT reorder
            or reformat the bib entries.
        venue: Informational tag (logged into the .docx properties);
            does not change formatting today. Reserved for future
            per-venue templates.
        figures: Optional list of figure descriptors. Each entry is
            ``{"path": "<abs path to .png/.jpg>", "caption": "<caption>",
            "section": "<exact key from sections>"}``. Each figure is
            inserted at the end of its target section, centered, followed
            by an italic 10pt caption. Default render width is 3.25 in
            (fits one column of the two-column body). When the path is
            missing or the section key does not match, a warning is
            recorded and the figure is appended at the end of the body
            (before References) rather than dropped silently.

    Returns:
        {
          "status": "ok",
          "output_path": "...",
          "size_bytes": N,
          "section_count": K,
          "figure_count": F,
          "warnings": [...]
        }
    """
    warnings: list[str] = []

    try:
        from docx import Document
        from docx.enum.section import WD_SECTION
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, Inches, RGBColor
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
    except ImportError:
        return {
            "status": "error",
            "error": (
                "python-docx is not installed in the OMC venv. "
                "Run: `.venv/bin/pip install python-docx` in your Memento-Research directory. "
                "Or use output_format=markdown / latex instead."
            ),
        }

    output_path = str(Path(output_path).expanduser().resolve())

    doc = Document()

    # ── Document-wide defaults ───────────────────────────────────────────
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)

    # Page margins (~ academic conference standard)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # ── Title (centered, single-column) ──────────────────────────────────
    if title:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.bold = True
        run.font.size = Pt(14)

    # ── Authors (centered, single-column) ────────────────────────────────
    if authors:
        for author_line in authors.strip().split("\n"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(author_line)
            run.font.size = Pt(11)

    # blank line before abstract
    doc.add_paragraph()

    # ── Abstract (single-column, italic heading "Abstract.") ─────────────
    if abstract:
        p = doc.add_paragraph()
        run = p.add_run("Abstract.")
        run.bold = True
        run.italic = True
        run = p.add_run(" " + abstract.strip())
        # Justify abstract body
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # ── Normalise figures: group by target section, keep orphans aside ───
    figures = figures or []
    figs_by_section: dict[str, list[dict]] = {}
    orphan_figs: list[dict] = []
    section_keys = set(sections.keys())
    for fig in figures:
        sec = (fig.get("section") or "").strip()
        if sec and sec in section_keys:
            figs_by_section.setdefault(sec, []).append(fig)
        else:
            if sec:
                warnings.append(
                    f"figure section '{sec}' did not match any sections key; "
                    "appended at end of body"
                )
            orphan_figs.append(fig)

    # ── Section break to two-column body ─────────────────────────────────
    new_section = doc.add_section(WD_SECTION.CONTINUOUS)
    _set_column_count(new_section, 2)

    # ── Body sections ────────────────────────────────────────────────────
    section_count = 0
    figure_count = 0
    for sec_name, sec_body in sections.items():
        section_count += 1
        h = doc.add_paragraph()
        run = h.add_run(sec_name)
        run.bold = True
        run.font.size = Pt(11)

        for block in _split_blocks(sec_body):
            if block.startswith("$$") and block.endswith("$$"):
                # Display equation — centered, italic, numbered placeholder
                eq = block.strip("$").strip()
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run(eq)
                run.italic = True
            elif block.startswith("| ") and "\n| " in block:
                _add_markdown_table(doc, block, warnings)
            else:
                p = doc.add_paragraph(block)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        # Figures targeting this section follow the last body block.
        for fig in figs_by_section.get(sec_name, []):
            if _add_figure(doc, fig, warnings):
                figure_count += 1

    # Orphan figures (missing or unmatched section) land at the body's tail.
    for fig in orphan_figs:
        if _add_figure(doc, fig, warnings):
            figure_count += 1

    # ── Section break back to single-column for references ───────────────
    if references:
        refs_section = doc.add_section(WD_SECTION.CONTINUOUS)
        _set_column_count(refs_section, 1)

        h = doc.add_paragraph()
        run = h.add_run("References")
        run.bold = True
        run.font.size = Pt(11)

        for ref_line in references.strip().split("\n"):
            ref_line = ref_line.strip()
            if not ref_line:
                continue
            p = doc.add_paragraph()
            # Hanging indent: first line flush, subsequent lines indented
            pf = p.paragraph_format
            pf.left_indent = Inches(0.25)
            pf.first_line_indent = Inches(-0.25)
            run = p.add_run(ref_line)
            run.font.size = Pt(10)

    # ── Doc properties (provenance) ──────────────────────────────────────
    cp = doc.core_properties
    cp.title = title or "Paper Writer Output"
    cp.author = authors.split("\n")[0] if authors else "AutoResearch"
    cp.subject = f"Generated by AutoResearch paper-writer talent (venue={venue})"

    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
    except Exception as e:
        return {"status": "error", "error": f"failed to save .docx: {e}"}

    return {
        "status": "ok",
        "output_path": output_path,
        "size_bytes": os.path.getsize(output_path),
        "section_count": section_count,
        "figure_count": figure_count,
        "warnings": warnings,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _add_figure(doc, fig: dict, warnings: list) -> bool:
    """Insert a centered image + italic caption. Returns True on success.

    Defensively skips and warns when the image is missing or unreadable —
    a single bad figure must not abort the whole .docx render.
    """
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt

    path = fig.get("path", "")
    caption = fig.get("caption", "")

    if not path:
        warnings.append("figure missing 'path' key; skipping")
        return False

    img_path = Path(path).expanduser()
    if not img_path.exists():
        warnings.append(f"figure not found at {path}; skipping")
        return False

    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    try:
        run = para.add_run()
        run.add_picture(str(img_path), width=Inches(3.25))
    except Exception as e:
        warnings.append(f"failed to embed image at {path}: {e}; skipping")
        return False

    if caption:
        cap_p = doc.add_paragraph()
        cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_run = cap_p.add_run(caption)
        cap_run.italic = True
        cap_run.font.size = Pt(10)

    return True


def _set_column_count(section, n: int) -> None:
    """Set the column count of a docx section — python-docx has no API."""
    from docx.oxml.ns import qn

    sectPr = section._sectPr
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        from docx.oxml import OxmlElement

        cols = OxmlElement("w:cols")
        sectPr.append(cols)
    cols.set(qn("w:num"), str(n))


def _split_blocks(text: str) -> list[str]:
    """Split body text into paragraph blocks separated by blank lines.

    Tables (markdown pipe syntax) and display equations ($$...$$) are
    preserved as single blocks. All other paragraphs are collapsed to
    single-line whitespace.
    """
    out: list[str] = []
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    for b in blocks:
        if b.startswith("$$"):
            out.append(b)
        elif b.startswith("| ") and "\n| " in b:
            out.append(b)
        else:
            out.append(" ".join(b.split()))
    return out


def _add_markdown_table(doc, table_md: str, warnings: list) -> None:
    """Render a simple markdown pipe-table to a docx table.

    Recognises:
        | h1 | h2 | h3 |
        |----|----|----|
        | a  | b  | c  |
    """
    from docx.shared import Pt

    lines = [l.strip() for l in table_md.strip().split("\n") if l.strip()]
    if len(lines) < 2:
        warnings.append("table block too short to render; skipping")
        return

    # Drop the separator row (|---|---|)
    rows = [l for l in lines if not all(c in "|-: " for c in l)]
    if not rows:
        return

    parsed = []
    for row in rows:
        # Strip leading/trailing pipes then split
        cells = [c.strip() for c in row.strip("|").split("|")]
        parsed.append(cells)

    n_cols = max(len(r) for r in parsed)
    table = doc.add_table(rows=len(parsed), cols=n_cols)
    table.style = "Light Grid Accent 1"

    for i, row_cells in enumerate(parsed):
        for j in range(n_cols):
            cell_text = row_cells[j] if j < len(row_cells) else ""
            cell = table.cell(i, j)
            cell.text = cell_text
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
                    if i == 0:
                        run.bold = True
