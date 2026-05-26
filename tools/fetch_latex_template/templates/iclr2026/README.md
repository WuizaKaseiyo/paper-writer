# ICLR 2026 Template

Official LaTeX template for ICLR 2026 conference submissions, packaged with
a clean starter `main.tex` ready for actually writing a paper (rather than
the formatting-instructions document the official zip ships with).

## Files

| File | Purpose |
|------|---------|
| `main.tex` | **Start here** — skeleton manuscript with Abstract / Intro / Related / Method / Experiments / Discussion / Conclusion stubs |
| `references.bib` | Empty bibliography starter |
| `iclr2026_conference.sty` | **Official** ICLR 2026 style file |
| `iclr2026_conference.bst` | **Official** BibTeX style |
| `fancyhdr.sty` | Page header/footer (required by `.sty`) |
| `natbib.sty` | Citation handling (required by `.sty`) |
| `math_commands.tex` | Common math macros from [goodfeli/dlbook_notation](https://github.com/goodfeli/dlbook_notation) — loaded by `main.tex` |
| `official_template.tex` | The official "formatting instructions" `.tex` from the ICLR 2026 zip, kept verbatim for reference |
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
../../scripts/new-paper.sh iclr2026 my-paper-name
cd ../../papers/my-paper-name
```

## ICLR 2026 specific knobs

### Anonymization (REQUIRED for submission)

The submitted version **must be anonymized**. Keep `\iclrfinalcopy` commented
out in `main.tex` — it should look like:

```latex
% \iclrfinalcopy
```

Only uncomment AFTER acceptance, when preparing the camera-ready.
Non-anonymous submissions are desk-rejected.

### Author placeholder

`main.tex` ships with `Anonymous Authors` / `Anonymous Affiliation`.
Replace those with real authors only after acceptance.

### Page limits

- **Main text**: 10 pages (excluding references and appendix)
- **References**: unlimited pages
- **Appendix**: unlimited (but reviewers are not required to read it)

Always verify the **current year's** limit on the official ICLR 2026 call
for papers — limits can change.

### Citation style

ICLR uses author-year style via `natbib`:

```latex
\cite{lecun2015deep}        % "LeCun et al. (2015)"
\citep{lecun2015deep}       % "(LeCun et al., 2015)"
\citet{lecun2015deep}       % "LeCun et al. (2015)"
\citeauthor{lecun2015deep}  % "LeCun et al."
\citeyear{lecun2015deep}    % "2015"
```

### Math macros

`math_commands.tex` provides a large set of pre-defined math macros (vectors
`\vx`, matrices `\mX`, sets `\sX`, distributions, etc.). See the
[dlbook_notation source](https://github.com/goodfeli/dlbook_notation) for
the full list. Remove the `\input{math_commands.tex}` line in `main.tex`
if you don't need them.

### Common pitfalls

- **Hyperref + cleveref ordering**: load `hyperref` before any `cleveref` package
- **Wrong margins**: don't change `\textwidth` / `\textheight` — the `.sty`
  sets ICLR margins; modifying them causes desk rejection
- **Author info in PDF metadata**: even with `\iclrfinalcopy` commented out,
  `\author{}` content can leak into PDF metadata. Many submission systems
  strip metadata automatically; verify with `pdfinfo main.pdf` before upload

## Source

These files were extracted from the official ICLR 2026 conference template
zip (file timestamps 2025-06-25 / 2025-08-21). The `.sty` / `.bst` /
`math_commands.tex` / `fancyhdr.sty` / `natbib.sty` are byte-identical to
the official distribution.

If a newer revision is released, replace these files in place — `main.tex`
is independent and won't need to change unless the `.sty` API breaks
backward compatibility.
