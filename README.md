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
└── tools/
    ├── .mcp.json                             no MCP servers needed
    └── manifest.yaml                         no custom tools (uses BASE_TOOLS)
```

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
| `llm_model` | `MiniMax-M2.7` | Long-context, good at academic prose. Swap to any equivalent. |
| `temperature` | `0.5` | Low enough for consistent traceability, high enough for readable prose. |
| `skills` | `[paper_writer, citation-management]` | `paper_writer` is the Stage 8 routing key consumed by `pipeline_engine.py`. |

## License

Apache 2.0 (matching the OneManCompany ecosystem). Add a `LICENSE` file before publishing.
