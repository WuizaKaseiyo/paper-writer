---
name: fetch_latex_template
description: Copy a vendored ICLR/NeurIPS venue template into a destination directory so the LLM can fill in main.tex. Returns the path to main.tex plus the list of supporting files. Runs fully offline — templates are bundled in this tool's templates/ dir.
---

# fetch_latex_template

When you need to produce LaTeX output (because the task specifies
`output_format=latex`), call this first. It does two things:

1. Copies the chosen venue subdir (`iclr2026/` or `neurips2026/`) from the
   templates vendored inside this tool into your destination
2. Returns the path to `main.tex` so you can `write()` your synthesized paper into it

The templates ship in the repo (`tools/fetch_latex_template/templates/`), so
this needs no network and no `git`.

## Arguments

| Arg | Type | Default | Purpose |
|-----|------|---------|---------|
| `venue` | str | (required) | `"iclr2026"` or `"neurips2026"` |
| `dest_dir` | str | (required) | Where to materialize the project — typically `<project_workspace>/stage8_paper` |

## Returns

```json
{
  "status": "ok",
  "venue": "iclr2026",
  "dest_dir": "/abs/path/to/dest",
  "main_tex_path": "/abs/path/to/dest/main.tex",
  "files_copied": ["main.tex", "references.bib", "iclr2026_conference.sty", ...],
  "instruction": "Template ready at ... Use write() to overwrite main.tex ..."
}
```

## What you should do next

1. `read(main_tex_path)` — see the placeholder structure
2. Build the synthesized paper sections in your scratchpad
3. `write(main_tex_path, "...full filled-in .tex content...")` — overwrite the starter
4. `write(<dest_dir>/references.bib, "...bibtex entries...")` — populate citations from Stage 2

## Notes

- Templates are vendored at `tools/fetch_latex_template/templates/<venue>/`; the tool copies from there, so it works offline with no `git` and no network.
- `official_template.tex` and per-template `README.md` are excluded from the copy — they're docs, not paper content.
- The `figures/` subdirectory is copied (empty by default with a `.gitkeep`). Drop your PDF/PNG figures there.
- The bundled conference style files (`.sty`/`.bst`) are redistributed under their original authors' terms; see `templates/NOTICE`. They are pinned to whatever is committed, so they will not pick up upstream fixes automatically — refresh them by re-copying from https://github.com/WuizaKaseiyo/paper-templates when a venue updates its package.
