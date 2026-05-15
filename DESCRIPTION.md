# Paper Writer

> A research-paper synthesis agent. Reads everything your AutoResearch pipeline produced and turns it into a peer-review-ready draft.

## Overview

Paper Writer is the **Stage 8** specialist in the AutoResearch pipeline. It does **not** perform any new research — its job is single-minded synthesis: take the seven prior stages' deliverables and weave them into a coherent paper that an academic reviewer could read top-to-bottom without confusion.

Every claim it writes traces back to a specific prior stage. If a fact isn't in Stages 1–7, it never enters the paper.

## What it produces

A single Markdown file (`stage8_paper_writer.md`) with these mandatory sections:

1. **Title** — from the refined research question (Stage 1)
2. **Abstract** — 150–250 words, structured: problem → method → key result → claim
3. **Introduction** — motivation, gap, contributions
4. **Related Work** — taxonomy from the literature survey, positioning of this work
5. **Methodology** — formal definitions from methodology design
6. **Experimental Setup** — datasets, baselines, metrics from experiment design
7. **Results** — tables and figures verbatim from result analysis
8. **Discussion** — interpretation, evidence vs. speculation clearly separated
9. **Limitations** — scope, dataset bias, baseline coverage, reproducibility caveats
10. **Conclusion** — what was shown, what comes next
11. **References** — sorted, deduplicated, sourced exclusively from the literature survey

## Use Cases

- **Research lab end-of-iteration draft** — At the end of a pipeline run, produce a draft suitable for internal review or external submission.
- **Reproducibility report** — Because every claim is forced to trace back to a stage output, the draft doubles as an evidence-chain summary.
- **Adversarial-review input** — The output feeds directly into Stage 9 (`adversarial-critic`). Drafts with hallucinations or missing sections will be rejected and rerun.

## What it does NOT do

- Generate new experimental results
- Run analyses the result-analyst did not run
- Cite papers not appearing in the literature survey
- Decide what experiments should have been run (that's earlier stages)
- Polish prose at the expense of traceability — if a number is missing, it writes `[TODO: missing from Stage N]` rather than guessing

## How it works

1. Dispatched by `pipeline_engine.py` when Stage 7 (Result Analysis) passes critic review.
2. Loads its runbook via `load_skill("paper_writer")`.
3. Reads `stage1_topic_refiner.md` through `stage7_result_analyst.md` from the project workspace.
4. Drafts the body first, then writes the abstract last.
5. Writes the final paper to `stage8_paper_writer.md` and calls `submit_result()`.

## Demo

<!-- Add screenshots of generated drafts here -->

## Success Stories

<!-- Real-world results -->

---

> **Content Policy**: This description is publicly visible on the Talent Market platform.
> Do not include illegal content, political propaganda, child exploitation material,
> pornography, or graphic violence. Violations will result in talent removal and
> repeated offenses will lead to permanent account suspension.
> All external links must point to legitimate, safe resources.
