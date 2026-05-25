---
name: fetch_latex_template
description: Clone the paper-templates repo and copy an ICLR/NeurIPS venue template into a destination directory so the LLM can fill in main.tex. Returns the path to main.tex plus the list of supporting files. Network required (uses git clone).
---

# fetch_latex_template

When you need to produce LaTeX output (because the task specifies
`output_format=latex`), call this first. It does three things:

1. `git clone --depth=1` the paper-templates repo (cached in /tmp after first call)
2. Copies the chosen venue subdir (`iclr2026/` or `neurips2026/`) into your destination
3. Returns the path to `main.tex` so you can `write()` your synthesized paper into it

## Arguments

| Arg | Type | Default | Purpose |
|-----|------|---------|---------|
| `venue` | str | (required) | `"iclr2026"` or `"neurips2026"` |
| `dest_dir` | str | (required) | Where to materialize the project — typically `<project_workspace>/stage8_paper` |
| `use_latest` | bool | `True` | If True, `git pull` on the cached clone every call |
| `repo_url` | str | `https://github.com/WuizaKaseiyo/paper-templates.git` | Override for forks/mirrors |

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

- The cached clone lives in `/tmp/paper_templates_clone_<random>` and persists for the lifetime of the OMC backend process. Subsequent calls in the same session reuse it.
- `official_template.tex` and per-template `README.md` are excluded from the copy — they're docs, not paper content.
- The `figures/` subdirectory is copied (empty by default with a `.gitkeep`). Drop your PDF/PNG figures there.
- Requires `git` on `$PATH`. Will return a clear error if `git` is missing or the network is down.
