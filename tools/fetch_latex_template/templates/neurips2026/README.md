# NeurIPS 2026 Template

Official LaTeX template for NeurIPS 2026 submissions, packaged with a clean
starter `main.tex` and the **mandatory** `checklist.tex`.

## Files

| File | Purpose |
|------|---------|
| `main.tex` | **Start here** — skeleton manuscript with Abstract / Intro / Related / Method / Experiments / Discussion / Conclusion stubs + checklist input |
| `checklist.tex` | **Official** NeurIPS Paper Checklist — REQUIRED, do not delete |
| `references.bib` | Empty bibliography starter |
| `neurips_2026.sty` | **Official** NeurIPS 2026 style file (with track options) |
| `official_template.tex` | The official "formatting instructions" `.tex` from the NeurIPS 2026 zip, kept verbatim for reference |
| `figures/` | Put your `.pdf` / `.png` figures here |

## Build

From this directory:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Or use the repo's helper:

```bash
../../scripts/build.sh
```

Or copy this whole directory to start a new paper:

```bash
../../scripts/new-paper.sh neurips2026 my-paper-name
cd ../../papers/my-paper-name
```

## NeurIPS 2026 specific knobs

### Track selection — pick exactly one

The `neurips_2026.sty` supports 7 submission modes. Default in `main.tex`:

```latex
\usepackage{neurips_2026}                    % = main (default)
```

Switch by commenting out the default and uncommenting the relevant line:

| Option | Track |
|--------|-------|
| `[main]` | Main Track (double-blind) — **default** |
| `[position]` | Position Paper Track |
| `[eandd]` | Evaluations & Datasets Track |
| `[creativeai]` | Creative AI Track |
| `[sglblindworkshop]` | Workshop (single-blind reviewing) |
| `[dblblindworkshop]` | Workshop (double-blind reviewing) |
| `[preprint]` | arXiv / preprint distribution |

For workshops, also set `\workshoptitle{Your Workshop Name}` in the preamble.

### Camera-ready

Add `final` to the track option:

```latex
\usepackage[main, final]{neurips_2026}
```

This reveals author info and removes the "Under review" footer.

### The Checklist is MANDATORY

Papers without the NeurIPS Paper Checklist are **desk-rejected**.

The `main.tex` here already includes `\input{checklist}` after the
bibliography. The checklist:

- Does NOT count toward the page limit
- Goes AFTER references, BEFORE the appendix
- Must keep the section heading "NeurIPS Paper Checklist"
- Must keep all subsection headings, questions, and guidelines
- Must use `\answerYes{}`, `\answerNo{}`, or `\answerNA{}` macros (defined by the .sty)
- Must include a 1-2 sentence justification after each answer

The instruction block at the top of `checklist.tex` (between
`%%% BEGIN INSTRUCTIONS %%%` and `%%% END INSTRUCTIONS %%%`) **must be
deleted** before final submission.

### Page limits

Check the **current year's** official Call for Papers for the exact limit
(typically 9 pages for Main Track plus unlimited references + checklist +
appendix). Limits can change year to year.

### Citation style

NeurIPS uses plainnat / natbib:

```latex
\cite{lecun2015deep}        % "LeCun et al. (2015)"
\citep{lecun2015deep}       % "(LeCun et al., 2015)"
\citet{lecun2015deep}       % "LeCun et al. (2015)"
\citeauthor{lecun2015deep}  % "LeCun et al."
```

If you need numeric citations: `\PassOptionsToPackage{numbers, compress}{natbib}`
BEFORE `\usepackage{neurips_2026}` (the .sty loads natbib internally).

### Common pitfalls

- **Forgot the checklist** → desk reject. The default `main.tex` includes it.
- **Changed margins** → desk reject. Don't modify `\textwidth` / `\textheight`.
- **Forgot to delete checklist instruction block** before camera-ready → embarrassing.
- **Wrong track option for camera-ready** → wrong footer; reviewers may flag.
- **Author info in preprint metadata** → if submitting double-blind, scrub `\author{}` block and PDF metadata before upload.

## Source

These files were extracted from the official NeurIPS 2026 formatting
instructions zip (file timestamps 2026-04-30). The `.sty` / `checklist.tex`
are byte-identical to the official distribution.

The `.sty` carries a `2026-01-29` revision stamp internally.
