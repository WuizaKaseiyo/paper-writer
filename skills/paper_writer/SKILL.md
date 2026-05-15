---
name: paper_writer
version: 1.0.0
description: "Runbook for synthesizing all prior AutoResearch stage outputs into a publication-grade paper draft. Non-negotiable section list, traceability rules, and output contract."
author: AutoResearch
---

# Paper Writer Runbook

You are dispatched for **AutoResearch Stage 8: Paper Generation**. Stages 1–7 have already produced their deliverables in the project workspace. Your sole job is to fuse them into one coherent paper draft.

## Step 0 — Confirm Inputs Exist

Before reading anything, call `ls()` on the project workspace. You must see all seven files below. If any are missing, **stop**, call `submit_result()` with status `FAILED` and report which stage(s) did not produce output. **Do not invent content for missing stages.**

| File | Source stage | What you extract |
|---|---|---|
| `stage1_topic_refiner.md` | Topic Refinement | Research question, scope, evaluation plan |
| `stage2_literature_surveyor.md` | Literature Survey | Related work, taxonomy, gap statement, **all citations** |
| `stage3_idea_generator.md` | Idea Generation | Hypothesis, architecture sketch, differentiation |
| `stage4_methodology_designer.md` | Methodology Design | Algorithms, loss functions, training procedure |
| `stage5_experiment_designer.md` | Experiment Design | Datasets, baselines, metrics, ablation plan |
| `stage6_experimentalist.md` | Experiment Execution | Raw results, logs, reproducibility notes |
| `stage7_result_analyst.md` | Result Analysis | Statistical analysis, tables, figures, interpretation |

## Step 1 — Read Every Input

`read()` each file sequentially. Take notes in your scratchpad on:
- The exact research question (Stage 1)
- The 5–10 most-cited related works (Stage 2)
- The core hypothesis (Stage 3)
- Any LaTeX-style notation in the methodology (Stage 4) — preserve it verbatim
- Every numerical table and figure caption (Stages 6, 7)
- Limitations explicitly noted by any earlier stage

## Step 2 — Write the Paper

Output **one** file `stage8_paper_writer.md` via `write()` with these sections in this order. The section names are mandatory; do not rename, omit, or reorder.

### Required Sections

1. **Title** — derived from Stage 1's research question. One line, capitalize content words.
2. **Abstract** — 150–250 words. Structure:
   - 1 sentence: problem statement (from Stage 1)
   - 2 sentences: method overview (from Stages 3 + 4)
   - 1–2 sentences: key quantitative result (from Stage 7 — copy the headline number verbatim)
   - 1 sentence: contribution claim
3. **1. Introduction** — three flowing prose paragraphs in this order:
   1. Motivation (drawn from Stage 1).
   2. Gap statement (drawn from Stage 2).
   3. Contributions paragraph naming 3 to 5 contributions in continuous prose, e.g. *"In this paper we make three contributions. First, … Second, … Third, …"*. This must NOT be a bullet list.
4. **2. Related Work**
   - Taxonomy from Stage 2
   - Explicit positioning paragraph: "Unlike [Author, Year], we …"
5. **3. Methodology**
   - Formal definitions from Stage 4 (preserve LaTeX/math notation verbatim)
   - Algorithm pseudocode if Stage 4 provided it
6. **4. Experimental Setup**
   - Datasets, baselines, metrics — **verbatim from Stage 5**
   - Hardware / hyperparameter notes from Stage 6
7. **5. Results**
   - Tables and figures from Stage 7 — **do not modify any numbers**
   - One paragraph per table/figure describing what it shows (no interpretation yet)
8. **6. Discussion**
   - Interpretation from Stage 7
   - Separate evidence from speculation. Flag speculation with phrases like "we conjecture", "this suggests, though not directly tested, that …"
9. **7. Limitations**
   - Explicit threats to validity. At minimum cover:
     - Scope (which settings were tested)
     - Dataset bias
     - Baseline coverage
     - Reproducibility caveats from Stage 6
10. **8. Conclusion**
    - What was shown (echo Stage 7 headline)
    - What comes next (open questions from Stages 2 and 7)
11. **References** — see `citation-management` skill

### Traceability Rules (non-negotiable)

- **No new claims.** Every sentence in Methodology, Results, and Discussion must trace to a prior stage file. If you can't point to a source line, do not write it.
- **No silent fabrication.** If Stage 7 reported a number, copy it. If you need a number you can't find, write `[TODO: missing from Stage N]` and continue. **Never** invent a value.
- **Quote sparingly.** Rephrase for flow, but preserve exact numerical claims and technical definitions byte-for-byte.
- **Speculation must be flagged.** Use hedging phrasing — never present speculation as result.

### Style — Strict Output Constraints

The rules below apply to your output file `stage8_paper_writer.md`. They do NOT apply to your scratchpad notes or to your `submit_result()` summary. Violating any of these is an automatic Stage 9 reject.

**Voice and tense.** Third person present tense for the work itself (e.g. *"We propose a method that …"*); past tense for experiments performed (e.g. *"Models were trained on the dataset described in Section 4."*).

**Language: British English throughout the entire paper.** Use BrE spellings and conventions consistently. Apply this rule to every section you author. The most common forms to use are:

* *-ise* not *-ize*: organise, analyse, optimise, characterise, recognise, summarise, generalise, regularise, parameterise.
* *-our* not *-or*: behaviour, colour, favour, neighbour, labour, rigour.
* *-re* not *-er*: centre, fibre, metre (length), litre, theatre.
* Double consonant before suffix: modelling, modelled, labelled, travelled, cancelled.
* Other: programme (not *program*, except when referring to software code), licence (noun) / license (verb), practice (noun) / practise (verb), towards (not *toward*), amongst (acceptable), whilst (acceptable). Use *learnt* and *spelt* rather than *learned* and *spelled* when used as adjectives.
* Punctuation: single quotation marks for direct speech, double quotes nested inside; full stops and commas go OUTSIDE the closing quote when the quoted fragment is not a full sentence (BrE convention).
* Date format: *15 May 2026*, not *May 15, 2026*.

Exceptions: keep table and figure captions from Stage 7 unchanged even if the original used American spellings, and quote any direct citation verbatim without silent re-spelling.

**Formatting prohibitions for the paper body.** The following are all automatic-reject offences:

* *No bold.* Never use `**text**`. If a term genuinely needs emphasis, use *italics* with single asterisks `*text*`, and use emphasis sparingly. A whole paper should contain only a handful of italicised emphases; if you find yourself italicising several phrases per page, you are overusing it.
* *No bullet points and no numbered lists inside body sections.* Convert every enumeration into running prose. Use connective phrases such as *"First, … Second, … Third, …"* or *"The method comprises three components: first …, then …, and finally …"*. Section and subsection headings are allowed and expected; lists within a section are not. The only exception is the References section, which is one entry per line by convention.
* *No em-dashes (—) and no en-dashes (–).* Restructure sentences using commas, semicolons, colons, parentheses, or full stops. The plain hyphen `-` remains allowed for compound modifiers (e.g. *fine-tuning*, *state-of-the-art*) and for inclusive numeric ranges inside tables (e.g. *2017-2024*).
* *No stub paragraphs.* Every paragraph in the body must contain at least three substantive sentences and must develop a single idea to completion. A "substantive sentence" is one that advances the argument, not a transitional fragment. If you cannot expand a thought to three substantive sentences, merge it into an adjacent paragraph rather than leaving it on its own.

**Citations.** `[Author, Year]` inline, sourced exclusively from Stage 2. Full rules live in the `citation-management` skill.

**Vocabulary prohibitions.** Do not use *novel*, *revolutionary*, *groundbreaking*, or *state-of-the-art* unless Stage 7 provides an explicit quantitative comparison that supports the claim. Avoid hedge-stacking such as *"we somewhat suggest the possibility that …"*; state a hedged claim once, cleanly, with a single hedge.

## Step 3 — Draft the Abstract Last

Write the body sections first. Only after the body is complete, write the Abstract by summarizing what you already wrote. This prevents the abstract from making claims the body doesn't support.

## Step 4 — Submit

1. Final `write()` of `stage8_paper_writer.md`.
2. Call `submit_result()` with a one-paragraph summary containing:
   - Total word count
   - List of sections produced
   - Any `[TODO: missing from Stage N]` markers and why
   - Any references you had to drop (with reason)

## What Happens Next

Your output flows directly into **Stage 9 (`adversarial-critic` with skill `peer_reviewer`)**. Drafts with hallucinated claims, missing sections, untraced numbers, or unflagged speculation will be REJECTED and rerun. Optimize for **traceability and completeness over novelty**.

## Common Failure Modes (avoid these)

| Failure | Why it gets rejected |
|---|---|
| Citing a paper not in Stage 2 | Untraceable; critic flags as hallucination |
| Rounding a number from Stage 7 | Quantitative drift; critic flags as misreporting |
| Skipping the Limitations section | Mandatory section is missing; automatic reject |
| Writing the abstract first | Often inconsistent with body; critic flags discrepancy |
| Marketing language (*novel*, *groundbreaking*) without numerical support | Unsupported claim; automatic reject |
| Inventing a baseline result Stage 5, 6, or 7 did not include | Untraceable; automatic reject |
| Using `**bold**` anywhere in the paper | Style violation; automatic reject |
| Using bullet points or numbered lists in any body section | Style violation; automatic reject |
| Using em-dashes (—) or en-dashes (–) anywhere | Style violation; automatic reject |
| One- or two-sentence paragraph in any body section | Stub paragraph; automatic reject |
| American spellings (*color*, *optimize*, *behavior*, *toward*) | Language violation; automatic reject |
