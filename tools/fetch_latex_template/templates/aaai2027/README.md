# AAAI-27 Template

Official LaTeX template for AAAI-27 conference submissions, packaged with a
clean starter `main.tex` ready for actually writing a paper (rather than
the long formatting-instructions document the official author kit ships
with).

## What's in here

| File | Purpose |
|------|---------|
| `main.tex` | Starter — overwrite this with your paper |
| `references.bib` | Starter bib (carries the kit's example entries; replace) |
| `aaai2027.sty` | Official AAAI-27 style file. **Do not edit.** |
| `aaai2027.bst` | Official AAAI-27 BibTeX style. **Do not edit.** |
| `figures/` | Drop figures here |
| `official_template.tex` | The full original kit `AnonymousSubmission2027.tex` for reference — not copied into your paper project |

## Strict AAAI-27 formatting rules

The author kit lists a long set of `% DO NOT CHANGE THIS` lines in the
preamble and a long DISALLOWED PACKAGES list. The starter `main.tex` here
already respects both. Notable forbidden packages: `hyperref`, `geometry`,
`fullpage`, `multicol`, `setspace`, `indentfirst`, `authblk`, `balance`.
Submissions that touch the page geometry are desk rejected — do not
"helpfully" add these even if you are used to them from other venues.

## Submission vs camera-ready

The starter uses:

```latex
\usepackage[submission]{aaai2027}
```

The `submission` option auto-anonymises authors and removes the copyright
footer. On acceptance:

1. Remove the `submission` option: `\usepackage{aaai2027}`.
2. Replace the `\author{Anonymous Submission}` / `\affiliations{}` blocks
   with the real author/affiliation block (see `official_template.tex`
   §"Camera-Ready Guidelines" for the exact macros: `\equalcontrib`,
   `\corresponding`, multiple-affiliation superscripts).
3. Add the AAAI copyright footer as the kit instructs.

## Bibliography

Cite with `\cite{...}` / `\citep{...}` (natbib is loaded by the kit).
`aaai2027.bst` is the required bib style — do not switch it for
`plainnat` or any other.

## Compiling

```bash
pdflatex main
bibtex   main
pdflatex main
pdflatex main
```
