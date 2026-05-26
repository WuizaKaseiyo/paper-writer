# Paper Writer

A research-paper synthesis agent for the [AutoResearch](https://github.com/1mancompany/OneManCompany) pipeline (Stage 8).
Reads every prior pipeline stage output (Stages 1 to 7) and produces a single, peer-review-ready Markdown paper draft.

> Built to the [Talent Market template](https://github.com/1mancompany/talent-template) spec.

## What it does

Paper Writer is *not* a research agent. It performs no new experiments and runs no new analyses. Its only job is faithful synthesis: it reads `stage1_topic_refiner.md` through `stage7_result_analyst.md` from the project workspace and produces `stage8_paper_writer.md` containing the following mandatory sections in order:

1. Title
2. Abstract
3. Introduction
4. Related Work
5. Methodology
6. Experimental Setup
7. Results
8. Discussion
9. Limitations
10. Conclusion
11. References

Every numerical claim, table, and figure must trace back to a specific prior stage. Untraceable content is rejected by the downstream Stage 9 critic.

## Strict output style

The runbook bakes in non-negotiable style rules for the produced paper:

- **British English** throughout (e.g. *optimise*, *behaviour*, *modelling*).
- **No bold.** Use *italics* for emphasis, sparingly.
- **No bullet points or numbered lists** inside body sections. Enumerations become prose.
- **No em-dashes or en-dashes.** Use commas, semicolons, parentheses, or full stops instead.
- **No stub paragraphs.** Every body paragraph contains at least three substantive sentences.

Full details live in [`skills/paper_writer/SKILL.md`](skills/paper_writer/SKILL.md).

## Repo structure

```
paper-writer/
├── profile.yaml                              talent identity + config
├── DESCRIPTION.md                            public-facing description
├── skills/
│   ├── paper_writer/SKILL.md                 main runbook (Stage 8 routing key)
│   └── citation-management/SKILL.md          inline-citation and reference rules
├── tools/
│   ├── .mcp.json                             no MCP servers needed
│   ├── manifest.yaml                         tool manifest (template/notes)
│   ├── fetch_latex_template/                 copy bundled ICLR/NeurIPS template (offline)
│   │   └── templates/                        vendored iclr2026 + neurips2026 (+ NOTICE)
│   ├── render_docx/                          synthesise sections → academic .docx
│   └── compile_latex/                        compile main.tex → PDF (host TeX)
└── tests/                                    offline-mocked tool tests
```

## Output formats

The default output is a single Markdown file. The task may request another carrier via an `output_format` directive parsed in the runbook's dispatch step:

| `output_format` | Deliverable | Backed by |
|---|---|---|
| `markdown` (default) | `stage8_paper_writer.md` | built-in `write()` |
| `latex venue=iclr2026` / `neurips2026` | LaTeX project (source only) | `fetch_latex_template` (bundled, offline) |
| `docx` | two-column academic `.docx` | `render_docx` (needs `python-docx`) |
| `pdf venue=<venue>` | compiled PDF (plus LaTeX source) | `fetch_latex_template` + `compile_latex` (needs host TeX) |
| `both venue=<venue>` | Markdown + LaTeX | the above |

Only `iclr2026` and `neurips2026` venues are supported; a missing `venue=` defaults to `iclr2026` with a warning. The two venue templates are vendored under `tools/fetch_latex_template/templates/`, so the LaTeX/PDF source setup runs offline (no `git`, no network); conference style files keep their original authors' terms (see `templates/NOTICE`). The `docx` and `pdf` paths still depend on host software (`python-docx`, a TeX distribution) and degrade gracefully when it is absent.

## How to use

### Inside OneManCompany / AutoResearch

1. **Remote mode.** With `talent_market.mode: remote` in `config.yaml`, register this repo URL in your Talent Market profile. HR will surface Paper Writer as a hire candidate.
2. **Local mode.** With `talent_market.mode: local`, clone this repo into `src/onemancompany/talent_market/talents/paper-writer/` of your OneManCompany checkout. HR will list it automatically on next reload.

Once hired, the AutoResearch `pipeline_engine` will dispatch Stage 8 to this employee via skill routing on the string `paper_writer`.

### Standalone

The runbook is self-contained Markdown. You can lift `skills/paper_writer/SKILL.md` into any other agent framework that supports system-prompt-style instructions, but you will need to provide the seven Stage 1-7 input files yourself.

## Configuration

The defaults in [`profile.yaml`](profile.yaml) are tuned for AutoResearch:

| Field | Value | Why |
|---|---|---|
| `hosting` | `omctalent` | Runs as a platform-internal LangChain ReAct agent. No external process. |
| `llm_model` | `openai/gpt-5.5-pro` (via OpenRouter) | Strong at long-form structured academic prose. Swap to any equivalent. |
| `temperature` | `0.5` | Low enough for consistent traceability, high enough for readable prose. |
| `skills` | `[paper_writer, citation-management]` | `paper_writer` is the Stage 8 routing key consumed by `pipeline_engine.py`. |

## License

[Talent Market Attribution License (TMAL) v1.0](LICENSE) — matching the upstream `1mancompany/talent-template` so this talent can be published to Talent Market under compatible terms.
