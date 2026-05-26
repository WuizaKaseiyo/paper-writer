---
name: paper_writer
version: 1.3.0
description: "Runbook for synthesizing all prior AutoResearch stage outputs into a publication-grade paper draft. Non-negotiable section list, claim-ledger white-list, inline per-sentence traceability, multi-format output (markdown / latex / docx / pdf), and output contract."
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

## Step 2 — Build the Claim Ledger

Before you write a single sentence of the paper, build a **claim ledger** in your scratchpad. The ledger is the white-list of everything you are permitted to assert. If a statement is not backed by a ledger entry, it does not enter the paper. This step is what stops the most common failure: writing a fluent, plausible sentence that no prior stage actually supports (the "A becomes A+B" elaboration).

Go through your Step 1 notes and extract every discrete, citable claim into a table. One row per claim:

| Field | Meaning |
|---|---|
| `id` | Sequential handle, `L1`, `L2`, … You reference these inline while drafting. |
| `type` | `quant` (a number, table cell, or figure value), `def` (a formal definition, equation, or algorithm), `qual` (a qualitative finding, design choice, or hypothesis), or `cite` (a reference from Stage 2). |
| `source` | The stage it came from: `S1`–`S7`. |
| `fragment` | The **verbatim** source text, copied byte-for-byte. For `quant`, copy the exact number. For `def`, copy the notation unchanged. |

Example:

```
| id | type  | source | fragment                                                          |
|----|-------|--------|-------------------------------------------------------------------|
| L1 | quant | S7     | "Sparse-A reaches 82.3 F1 versus 80.1 for the dense baseline"     |
| L2 | def   | S4     | "loss L = L_task + lambda * ||W||_1 with lambda = 1e-3"           |
| L3 | qual  | S3     | "hypothesis: activation sparsity improves out-of-domain transfer" |
| L4 | cite  | S2     | "Vaswani et al. (2017), Attention Is All You Need"                |
```

Rules for the ledger:
- **Extract, do not interpret.** A ledger entry records what a stage *said*, not what you infer it *implies*. "Accuracy rose 2 points" is a valid entry; "the method generalises well" is not, unless a stage said exactly that.
- **No entry, no fact.** If while reading you wanted to write something but cannot find a fragment for it, it gets no ledger row, which means it cannot enter the paper.
- The ledger is scratchpad-only. It is **not** part of the output file, but you report its size in `submit_result()`.

## Step 3 — Write the Paper Body

### Draft with inline source tags

You draft in **two passes**. In the first pass you write the body with a source tag appended to **every sentence**. In Step 5 you strip the tags to produce the clean, format-ready content. Tagging while you draft is what forces each sentence to earn its place; do not skip it and "write clean directly", because that is exactly when unsupported elaboration creeps in.

Every body sentence falls into exactly one of three categories and carries the matching tag:

- **Sourced** — the sentence asserts a fact, and that fact maps to a ledger entry. Tag it with the entry id: `⟨L7⟩`. A sentence may cite several entries: `⟨L7,L9⟩`. This is the only category allowed to state findings, numbers, definitions, or claims.
- **Connective** — the sentence carries no factual content; it only links, signposts, or restates structure (e.g. "This section describes the experimental setup."). Tag it `⟨—⟩`. Keep these rare.
- **Speculation** — an interpretation that no stage states outright. Allowed **only** in Discussion, **only** with hedging ("we conjecture", "this suggests, though not directly tested, that …"), and tagged `⟨spec⟩`.

If a sentence fits none of the three, it is a hallucination by definition: either find a ledger entry for it (and make it Sourced) or delete it. There is no fourth category. A sentence that *feels* true and *reads* fluently but has no ledger id is exactly the failure this guards against.

Worked micro-example. Suppose the ledger has only `L1 = "Sparse-A reaches 82.3 F1 vs 80.1 baseline"`.

- Allowed: *"Sparse-A reaches 82.3 F1, against 80.1 for the dense baseline. ⟨L1⟩"*
- Forbidden (this is the A→A+B failure): *"Sparse-A reaches 82.3 F1, against 80.1 for the dense baseline, because sparsity suppresses noisy activations."* The clause after "because" has no ledger entry. Either it earns its own entry from a stage, or it is cut. To offer it as interpretation, move it to Discussion, hedge it, and tag `⟨spec⟩`.

The tagging requirement applies to Introduction, Related Work, Methodology, Experimental Setup, Results, Discussion, Limitations, and Conclusion. Title and References are exempt (Title derives from Stage 1; References are governed by the `citation-management` skill). Tagging happens at the level of the synthesised content and is carrier-independent: the format chosen later in Step 6 does not change which sentences are allowed.

### Section contract

Author the following sections in this order. The section names are mandatory; do not rename, omit, or reorder. The *carrier* (Markdown, LaTeX, or Word) is selected later in Step 6; here you produce the content.

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

The rules below apply to the synthesised content in every output format (Markdown, LaTeX, Word). They do NOT apply to your scratchpad notes or to your `submit_result()` summary. Violating any of these is an automatic Stage 9 reject.

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

## Step 4 — Draft the Abstract Last

Write the body sections first. Only after the body is complete, write the Abstract by summarising what you already wrote. This prevents the abstract from making claims the body does not support. Tag abstract sentences too: every abstract sentence must restate a body sentence that is itself `⟨L…⟩`-sourced. The abstract introduces no new ledger reference and no claim the body did not already make.

## Step 5 — Self-Audit and Strip Tags

You now have a fully tagged draft (body plus abstract). Do not emit any format yet. Run this audit, in order:

1. **Untagged-sentence sweep.** Read every sentence of the body. Any sentence with no `⟨…⟩` tag is unaccounted for: attach the correct ledger id, demote it to `⟨—⟩` if it truly carries no claim, or delete it. After this sweep, **every** body sentence has exactly one tag.
2. **Speculation check.** For each `⟨spec⟩` sentence, confirm it sits in Discussion and is hedged. If a `⟨spec⟩` sentence reads as a flat assertion, reword it as a conjecture or cut it.
3. **Connective budget.** Count `⟨—⟩` sentences. If they exceed roughly one per section, you are padding; the usual cause is the "three substantive sentences per paragraph" rule pushing you to invent filler. Prefer a shorter, fully-sourced paragraph over a padded one. **Traceability outranks the paragraph-length style rule whenever they conflict.**
4. **Abstract back-check.** Confirm each abstract sentence maps to an `⟨L…⟩`-sourced body sentence.
5. **Quant spot-check.** For each `⟨L…⟩` of type `quant`, compare the number in your prose against the ledger fragment character-by-character. No rounding, no reformatting.

Only after all five pass, **strip the tags**: remove every `⟨…⟩` token plus any stray whitespace it leaves behind. The result is the clean, tag-free synthesised content that Step 6 emits in the requested format. Whatever files Step 6 writes (Markdown, LaTeX, or Word) **must contain zero `⟨` characters**. A surviving tag is itself an automatic Stage 9 reject, so verify before submitting.

## Step 6 — Dispatch to Output Format

The synthesised content (clean and de-tagged from Step 5) stays the same regardless of format; only the *carrier* changes.

Parse the task description for an `output_format` directive. The grammar is intentionally minimal:

- `output_format=markdown` (or no directive at all) → **default behaviour** — single Markdown file
- `output_format=latex venue=iclr2026` → ICLR 2026 LaTeX project (source only, not compiled)
- `output_format=latex venue=neurips2026` → NeurIPS 2026 LaTeX project (source only, not compiled)
- `output_format=docx` → academic Word document
- `output_format=pdf venue=<venue>` → LaTeX project compiled to PDF
- `output_format=both venue=<venue>` → emit Markdown AND LaTeX (skip docx and pdf unless explicitly requested)

If `venue=` is missing for a `latex`, `pdf`, or `both` request, default to `iclr2026` and warn in your `submit_result()` summary.

### 6a. Markdown branch (default — original behaviour)

1. `write()` the synthesised content to `stage8_paper_writer.md`.
2. Proceed to Step 7.

### 6b. LaTeX branch

1. Call `fetch_latex_template(venue=<venue>, dest_dir="<workspace>/stage8_paper")`. This clones the paper-templates repo and copies the venue's `.sty`, `.bst`, `main.tex` starter, `references.bib`, and `figures/` directory.
2. Read the returned `main_tex_path` to see the skeleton structure.
3. Build the full filled-in `.tex` content in your scratchpad. The 11 mandatory sections from Step 3 map cleanly onto the LaTeX `\section{}` structure already in the starter — replace its placeholder text with your synthesised content.
4. Translate Markdown conventions to LaTeX as you write:
   - `[Author, Year]` inline cites → `\citep{author_year}` (with a corresponding `references.bib` entry)
   - `*italics*` → `\emph{italics}` (only if the body truly needs emphasis; remember: emphasis sparingly)
   - Section headers → `\section{}`, `\subsection{}`
   - Tables → LaTeX `tabular` environments
   - Display equations → `\begin{equation}...\end{equation}`
   - `[TODO: missing from Stage N]` markers → keep them verbatim; the critic will see them
5. `write()` the complete filled-in `.tex` content to `<dest_dir>/main.tex` (overwriting the starter).
6. `write()` populated `<dest_dir>/references.bib` — one BibTeX entry per citation, sourced exclusively from Stage 2.
7. Note in your `submit_result()` summary that the deliverable is the project at `<dest_dir>` (not a single file).

### 6c. Docx branch

1. Build the section content as a Python dict `{header: body}` in your scratchpad — keys numbered like `"1. Introduction"`, `"2. Related Work"`, etc.
2. Call `render_docx(title=..., authors=..., abstract=..., sections={...}, references=..., output_path="<workspace>/stage8_paper_writer.docx", venue=<venue or "generic">)`.
3. The tool produces a two-column academic Word document. If `python-docx` is not installed in the OMC venv, it returns a clear error — in that case, fall back to writing Markdown and warn in `submit_result()` that docx output was unavailable.

### 6d. Both branch

1. Run **6a** to produce `stage8_paper_writer.md`.
2. Then run **6b** to produce the LaTeX project at `<workspace>/stage8_paper/`.

### 6e. PDF branch

1. Run **6b** in full to materialise and fill in the LaTeX project at `<dest_dir> = <workspace>/stage8_paper`. The PDF path reuses the LaTeX path; do not author content twice.
2. Call `compile_latex(project_dir="<dest_dir>")`. It compiles `main.tex` with the host TeX distribution (latexmk if present, otherwise pdflatex with a BibTeX pass) and returns `pdf_path` on success.
3. If `compile_latex` returns `status="error"`, do not discard the work: the filled-in LaTeX project is still a valid deliverable. Report the failure and the returned `log_tail` in `submit_result()`, and note that the PDF could not be produced (for example, no TeX distribution on the host, or a LaTeX error in `log_tail`). The deliverable then degrades to the LaTeX project, exactly as `output_format=latex`.
4. On success, the deliverables are both the compiled `pdf_path` and the LaTeX project alongside it.

### Format-agnostic rules (apply to all branches)

- All five style constraints (British English, no bold, no bullet points, no em-dashes, no stub paragraphs) apply to **all** output formats including LaTeX and Word. Translate the *form* (markdown vs `\textit{}` vs Word italic), not the *rule*.
- Traceability rules apply identically: every claim still traces to a Stage 1-7 file, regardless of carrier. The claim-ledger discipline from Step 2 and the inline-tag audit from Step 5 are carrier-independent; tags are stripped before any format is emitted, so no carrier may reintroduce an untraced claim.
- The 11 mandatory sections must all be present in every format.

## Step 7 — Submit

1. Confirm the deliverable exists at the expected path (single file for markdown/docx, directory for latex/both) and that no `⟨…⟩` tag survived into it.
2. Call `submit_result()` with a one-paragraph summary containing:
   - Output format used and path(s)
   - Total word count of the body (across all body sections)
   - List of sections produced
   - Claim-ledger size (number of entries, broken down by type)
   - Sentence accounting: how many `⟨L…⟩` sourced, `⟨—⟩` connective, `⟨spec⟩` speculation
   - Confirmation that the deliverable is tag-free
   - Any `[TODO: missing from Stage N]` markers and why
   - Any references you had to drop (with reason)
   - For LaTeX: number of BibTeX entries written; whether any cites lack matching `.bib` entries
   - For docx: whether `python-docx` was available; warnings returned by `render_docx`
   - For PDF: the engine `compile_latex` used and the `pdf_path`, or, if compilation failed, the `log_tail` and the fact that the deliverable degraded to the LaTeX source project

## What Happens Next

Your output flows directly into **Stage 9 (`adversarial-critic` with skill `peer_reviewer`)**. Drafts with hallucinated claims, missing sections, untraced numbers, or unflagged speculation will be REJECTED and rerun. Optimize for **traceability and completeness over novelty**.

## Common Failure Modes (avoid these)

| Failure | Why it gets rejected |
|---|---|
| Writing a fluent, plausible sentence with no ledger entry | The A→A+B elaboration; untraceable, automatic reject |
| Leaving a `⟨…⟩` tag in any emitted deliverable | Strip step skipped or incomplete; automatic reject |
| Stating an interpretation without `⟨spec⟩` plus hedging | Speculation presented as result; automatic reject |
| Padding paragraphs with connective filler to reach three sentences | Inflated `⟨—⟩` budget; prefer shorter sourced prose |
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
