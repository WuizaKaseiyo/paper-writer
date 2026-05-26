---
name: compile_latex
description: Compile a filled-in LaTeX project to PDF with a host TeX distribution (latexmk preferred, else pdflatex/xelatex/lualatex). Judges success by a fresh non-empty PDF, returns a .log tail on failure. Requires a TeX distribution on the host PATH.
---

# compile_latex

The final step of the LaTeX output path. Call this **after**
`fetch_latex_template` has laid down the venue project and you have used
`write()` to fill in `main.tex` and `references.bib` with the synthesised
paper. It turns that project into `main.pdf`.

## When to call

Only when the task asks for a compiled PDF (`output_format=pdf`). For
`output_format=latex` the deliverable is the source project, so you stop after
writing `main.tex`; do not compile.

## Arguments

| Arg | Type | Default | Purpose |
|-----|------|---------|---------|
| `project_dir` | str | (required) | The LaTeX project directory — the `dest_dir` returned by `fetch_latex_template` (e.g. `<workspace>/stage8_paper`). |
| `main_tex` | str | `"main.tex"` | Entry `.tex` filename inside `project_dir`. |
| `engine` | str | `"auto"` | `"auto"`, `"latexmk"`, `"pdflatex"`, `"xelatex"`, or `"lualatex"`. `"auto"` uses `latexmk` if present, else the first available pdf engine. |
| `run_bibtex` | bool | `True` | Run a BibTeX pass when a `references.bib` is present (only affects the manual fallback; `latexmk` handles the bibliography itself). |
| `timeout_s` | int | `180` | Per-command timeout in seconds. |

## Returns

```json
{
  "status": "ok",
  "pdf_path": "/abs/path/to/main.pdf",
  "engine": "latexmk",
  "passes": ["latexmk"],
  "size_bytes": 184213,
  "warnings": []
}
```

On error:

```json
{
  "status": "error",
  "error": "compilation finished but no PDF was produced at ...",
  "engine": "pdflatex",
  "passes": ["pdflatex", "bibtex", "pdflatex", "pdflatex"],
  "log_tail": "...last 40 lines of main.log..."
}
```

## How it works

- With `latexmk` it runs a single `latexmk -pdf -interaction=nonstopmode -halt-on-error`, which decides how many passes and whether BibTeX/Biber is needed.
- Without `latexmk` it runs the classic sequence: engine, then `bibtex` (if `references.bib` exists and `run_bibtex` is true), then engine twice more to resolve cross-references and citations.
- LaTeX often exits non-zero on warnings yet still emits a valid PDF, so success is judged by "a fresh, non-empty PDF exists", not by the exit code. The exit code and a `.log` tail are always available for triage.

## Dependencies and safety

- Requires a TeX distribution on the host `$PATH` (MacTeX, TeX Live, or MiKTeX). If none is found, the tool returns a clear error suggesting `output_format=markdown` or `docx` instead. The talent runs in the OMC backend, so the TeX distribution must be installed on that host, not just on a developer laptop.
- Prefer a *complete* distribution (full TeX Live / MacTeX), not a minimal one (BasicTeX). The venue styles pull in common CTAN packages: the NeurIPS style needs `environ` (which itself needs `trimspaces`), `geometry`, `natbib`, and `lineno`. A missing package surfaces in `log_tail` as `File 'foo.sty' not found`; install it on the host with `tlmgr install foo`.
- Shell escape (`\write18`) is disabled on every direct engine call, so a `.tex` file cannot run arbitrary host commands during compilation.

## What this tool does NOT do

- It does not write or edit `main.tex` / `references.bib` — that is your job before calling it.
- It does not fetch packages over the network mid-build; missing LaTeX packages surface as compile errors in `log_tail`.
- It does not convert Word or Markdown to PDF; it only compiles LaTeX. For docx, use the LibreOffice path on the host instead.
