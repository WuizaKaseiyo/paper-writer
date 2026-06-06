---
name: paper_writer
version: 2.0.0
description: "Runbook for synthesising all prior AutoResearch stage outputs into a top-conference-grade paper draft. Combines argument-design (contribution / mechanism-gap / insight / closest-works / RQs / 80% citation coverage) with claim-ledger and inline per-sentence traceability. Supports markdown / latex / docx / pdf / both. Includes Writing Craft Pass and Reviewer Quick-Path Audit."
author: AutoResearch
---

# Paper Writer Runbook

You are dispatched for **AutoResearch Stage 8: Paper Generation**. Stages 1–7 have already produced their deliverables in the project workspace. Your sole job is to fuse them into one coherent paper draft that meets the bar of a top venue (NeurIPS / ICLR / ICML / ACL / CVPR).

**Two readers see your output:**

1. **Stage 9 peer reviewer** — checks traceability, completeness, statistical honesty
2. **A busy top-conference reviewer (modelled)** — has 5 minutes and is mentally weighing accept / reject against dozens of other papers

The reviewer's "fast path" is **title → abstract → Figure 1 → contribution list → main result table → conclusion**. Each of these six anchors must independently convey your contribution AND be mutually consistent. If a tired reviewer reads only those six and cannot correctly state what you contributed, the paper is dead on arrival.

**Top-conference bar:** A memorable idea, proved rigorously and honestly, written so that a busy reviewer wants to defend you within five minutes. Volume of work passes the bar to submit; narrative, rigour, and honesty decide the top 5 %.

This runbook enforces two disciplines that pull in tension and must coexist:

- **Argument design** (Step 2) — produce a real top-conference argument structure, not a paraphrase of the stage files.
- **Claim-ledger traceability** (Step 3 + Step 4 + Step 6) — every sentence in the body is tagged to a verbatim source fragment and audited before tags are stripped.

Neither alone is sufficient. Argument design without the ledger produces fluent fiction; the ledger without argument design produces traceable mediocrity. Both run, in order, every time.

---

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

---

## Step 1 — Read Every Input

`read()` each file sequentially. Take notes in your scratchpad on:

- The exact research question (Stage 1)
- **The full list of papers surveyed in Stage 2** — count them, list every arxiv ID. Each one is a citation candidate; Stage 2 has already filtered for relevance, so do not re-filter at this stage. (The default disposition is *include*; see §2.7 and the `citation-management` skill.)
- The core hypothesis (Stage 3) AND the *insight* behind it (the non-obvious observation that motivates the method)
- All formal definitions and design decisions in Stage 4, including the *why-this-not-that* rationale for each choice
- All datasets, baselines, metrics, and the rationale for each (Stage 5)
- Every numerical result, ablation, and analysis dimension in Stages 6 and 7 — copy headline numbers byte-for-byte into your notes
- Limitations and threats to validity explicitly noted by any earlier stage

## Step 1.5 — Discover Figures Produced by Prior Stages

Run `ls()` on the project workspace and identify embedded figures saved by prior stages. The canonical case is **Stage 4 (Methodology Design)**, which is expected to produce `stage4_framework_figure.png` — the headline framework diagram. For each figure found, also locate the corresponding caption in the source stage's `.md` file (look for a line of the form `![Figure N: …](stage4_framework_figure.png)`) and record:

| Field | Source |
|---|---|
| `path` | absolute or workspace-relative path to the PNG |
| `caption` | the exact caption text from the prior stage's `.md` |
| `target_section` | the paper section the figure belongs in (`3. Methodology` for `stage4_framework_figure.png`; `5. Results` for any `stage7_*.png`) |

Keep this list in your scratchpad. **Do NOT re-generate or modify the image** — paper-writer is a synthesiser, not a renderer. If no figure files are present, simply skip the rest of Step 1.5; the paper still renders, just without embedded figures.

---

## Step 2 — Argument Design (scratchpad-only, no body yet)

**DO NOT WRITE PAPER BODY UNTIL THIS STEP IS COMPLETE.** A paper that goes straight from "read inputs" to "write Introduction" is the single most common reason this skill produces mediocre output. The body must be the *consequence* of an argument design, not a transcription of stage files.

In your scratchpad, produce all seven items below before writing a single body paragraph.

### 2.1 One-Sentence Contribution

Write a single non-trivial sentence stating what this work contributes to the field. Apply this filter:

**Banned words** (delete and rewrite if present): `novel`, `significant`, `robust`, `efficient`, `comprehensive`, `powerful`, `state-of-the-art`, `extensive`, `new framework`, `proposes a new`. These words signal nothing because every paper claims them.

**Required ingredients**: concrete mechanism + measurable claim grounded in Stage 6 or Stage 7 numbers.

| Pass | Fail |
|---|---|
| "A bi-level orchestrator/worker architecture that decouples strategy learning from execution, lifting task success rate on ARC-AGI-3 from 23 % to 41 %." | "We propose a novel framework for intrinsic exploration." |
| "A hybrid graph-VLM intrinsic reward that wins on 7 of 9 hard ARC-AGI-3 tiers and explains the win via a measured shift in coverage-curve curvature." | "We achieve state-of-the-art results with comprehensive experiments." |

### 2.2 Mechanism-Level Gap

Write the gap statement at the *mechanism* level. The default failure mode is to write "existing methods do not work well", which conveys nothing. Instead, say *which* method, under *which* condition, exhibits *which* phenomenon, *because of* which mechanism. The more specific the gap, the more inevitable your insight looks.

**Sources**: Stage 2 (what existing methods do and where they fail), Stage 3 (your insight into why).

| Pass | Fail |
|---|---|
| "Existing single-agent web retrieval methods saturate context after about six retrieval hops because retrieval and synthesis share one trajectory, so synthesis errors cascade into subsequent queries." | "Existing methods are not effective enough." |
| "Curiosity-driven exploration with prediction-error reward (ICM, RND) degrades in high-dimensional RGB observation settings because the prediction target itself becomes high-entropy, drowning the novelty signal." | "Prior work has limitations on hard tasks." |

### 2.3 Core Insight (why, before what)

State the non-obvious observation that motivates your method, in **one** sentence. This is the `why`. The method follows in §2.4 as the `what`. Spotlight papers always present insight before method; mediocre papers describe the method first and call the insight a "motivation".

**Source**: Stage 3's hypothesis rationale, or Stage 4's first-principles design decision.

### 2.4 Closest Prior Works (2–3)

From Stage 2's corpus, identify the **two to three** works most similar to yours along the dimension your contribution operates. For each:

- Inline citation marker `[Author, Year]`
- One sentence: what they do
- One sentence: the difference vs your work

This is the positioning lever. The single biggest reviewer red flag is missing the closest related work — Stage 2 already did this for you; just use it. You will surface this as the *positioning paragraph* in Section 4 (Related Work).

### 2.5 Contributions (3–4, bulleted in scratchpad only)

Each contribution must be:

- **Concrete** — names a mechanism or a measurable quantity, not a process
- **Verifiable** from the paper alone (no external context required)
- **Separable** from the others — no two contributions describe the same thing

Mix categories freely: conceptual, methodological, empirical. Do not mix process items with results.

**Banned contribution shapes:**

- "We perform extensive experiments…" — that is a process, not a result
- "We propose a novel framework…" — vacuous; the framework's actual mechanism is the contribution, not its existence
- "We achieve state-of-the-art results…" — a claim, not a contribution; rewrite as the *mechanism* that delivers the result

### 2.6 Research Questions (2–3)

Stages 4 and 5 already framed hypotheses. Restate them here as research questions (RQs) that your experiments will answer. Each RQ must map 1:1 to an experiment subsection in Section 5 (Results). Reviewers cannot accuse you of "why did you run this experiment?" if the RQ-to-experiment mapping is explicit.

### 2.7 Citation Plan (≥ 80 % Stage 2 Coverage)

For each paper in the Stage 2 corpus, write:

- The inline citation marker `[Author, Year]`
- Which paper section it will appear in (typically Related Work or Methodology)
- A one-clause purpose statement

**Coverage target**: at least 80 % of the Stage 2 corpus appears inline in the final paper. **The default disposition of every Stage 2 paper is *include*.** If you must drop a paper, list it explicitly in the `submit_result()` summary under `references dropped`, with a one-sentence reason (e.g. "Withdrawn from arXiv; not safe to cite"). A 4-reference paper after a 28-paper survey is a runbook failure, not a stylistic choice.

### CHECKPOINT

If §§ 2.1 – 2.7 are not all complete in your scratchpad, **return to Step 1** and re-read whichever stage is unclear. Do not proceed to Step 3.

---

## Step 3 — Build the Claim Ledger

After Step 2 finalises *what you intend to argue*, Step 3 establishes *what you are permitted to assert*. The ledger is the white-list of every factual statement you may put in the body. If a statement is not backed by a ledger entry, it does not enter the paper. This step is what stops the most common failure mode: writing a fluent, plausible sentence that no prior stage actually supports (the "A becomes A+B" elaboration, where you write a correct fact A and then quietly append an unsupported elaboration B).

Go through your Step 1 notes (and the §2.7 citation plan) and extract every discrete, citable claim into a table. One row per claim:

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
- **One `cite` row per Stage 2 paper.** Every paper in the Stage 2 corpus gets its own `cite` row. The set of `cite` rows is your citation plan from §2.7, made concrete.
- The ledger is scratchpad-only. It is **not** part of the output file, but you report its size in `submit_result()`.

---

## Step 4 — Write the Paper Body (with inline source tags)

You now have both an argument design (Step 2) and a claim ledger (Step 3). Write the body using **two passes**:

- **First pass**: write every body sentence with a source tag appended. The tag is what forces each sentence to earn its place.
- **Second pass** (Step 6): audit the tagged draft, then strip the tags to produce clean format-ready content.

Tagging while you draft is non-optional. Do not skip it and "write clean directly", because that is exactly when unsupported elaboration creeps in.

### 4.1 Tagging Grammar

Every body sentence falls into exactly one of three categories and carries the matching tag:

- **Sourced** — the sentence asserts a fact, and that fact maps to one or more ledger entries. Tag it with the entry ids: `⟨L7⟩` or `⟨L7,L9⟩`. This is the only category allowed to state findings, numbers, definitions, or claims.
- **Connective** — the sentence carries no factual content; it only links, signposts, or restates structure (e.g. "This section describes the experimental setup."). Tag it `⟨—⟩`. Keep these rare.
- **Speculation** — an interpretation that no stage states outright. Allowed **only** in Discussion, **only** with hedging ("we conjecture", "this suggests, though not directly tested, that …"), and tagged `⟨spec⟩`.

If a sentence fits none of the three, it is a hallucination by definition: either find a ledger entry for it (and make it Sourced) or delete it. There is no fourth category. A sentence that *feels* true and *reads* fluently but has no ledger id is exactly the failure this guards against.

Worked micro-example. Suppose the ledger has only `L1 = "Sparse-A reaches 82.3 F1 vs 80.1 baseline"`.

- Allowed: *"Sparse-A reaches 82.3 F1, against 80.1 for the dense baseline. ⟨L1⟩"*
- Forbidden (the A→A+B failure): *"Sparse-A reaches 82.3 F1, against 80.1 for the dense baseline, because sparsity suppresses noisy activations."* The clause after "because" has no ledger entry. Either it earns its own entry from a stage, or it is cut. To offer it as interpretation, move it to Discussion, hedge it, and tag `⟨spec⟩`.

Tagging applies to Introduction, Related Work, Methodology, Experimental Setup, Results, Discussion, Limitations, and Conclusion. Title and References are exempt (Title derives from §2.1 and Stage 1; References are governed by the `citation-management` skill). Tags are carrier-independent; they are stripped in Step 6, so no later format may reintroduce an untraced claim.

### 4.2 Required Sections (eleven, in this order)

Author the following sections in this order. The section names are mandatory; do not rename, omit, or reorder. Write the body sections first; **write the Abstract last** so it can summarise material already written.

### Section 1 — Title

Describe the **contribution**, not the field.

| Pass | Fail |
|---|---|
| `A Hierarchical Parallel Agent Framework for Web Information Seeking` | `Research on Web Agents` |
| `Decoupling Strategy and Execution in LLM Agents via Bi-Level Stackelberg Orchestration` | `A Novel LLM Agent Framework` |

Rules:

- Name your method if the method is the core contribution (e.g. `OASIS:`, `LATS:`); a memorable name lifts citation count, but names must serve the content, not the other way round
- Avoid empty words: `novel`, `efficient`, `robust`, `comprehensive` convey nothing — every paper claims them
- Capitalise content words; one line; no punctuation other than a colon between method-name and descriptor

### Section 2 — Abstract (150–250 words, self-contained, written **last**)

Five-part structure, each part one or two sentences:

1. **Context** — what the field is doing
2. **Gap / tension** — the specific unsolved problem (drawn from §2.2; *not* a generic "still not good enough")
3. **What we do** — we propose X, the core mechanism is Y
4. **Key results with numbers** — on benchmark Z we reach N % (relative improvement M %) plus one secondary finding
5. **Significance** — one sentence on impact

**Discipline**: every numeric claim in the abstract must appear, byte-identical, in the main result table. Reviewers explicitly cross-check abstract against tables to catch overclaim — if the abstract says "+12 %" but the table shows "+9 %", you are caught. Every abstract sentence must restate a body sentence that is itself `⟨L…⟩`-sourced. The abstract introduces no new ledger reference and no claim the body did not already make.

### Section 3 — Introduction (McKeown 5-paragraph)

Goal: a reviewer finishing the Introduction (or, ideally, the first page) can (a) state your contribution and (b) is convinced this is worth reading.

The five paragraphs, in order:

1. **The problem and why it matters.** One or two sentences pulling the reader into the field, then a quick narrow to the specific problem you address. Do **not** spend a paragraph on "LLMs are popular" — reviewers have no patience for this.
2. **The state of the art and its gap.** What existing methods accomplish, where they fail — **at the mechanism level** (see §2.2). The more specific the gap, the more inevitable your insight looks.
3. **Core insight + method overview.** State the **insight** first (§2.3), then describe the **method** as the near-inevitable consequence. The construction "Our key observation is that …; based on this, we propose …" is canonical.
4. **Contributions list.** Three to four contributions in continuous prose (no bullet points anywhere in the body), each lifted verbatim from §2.5. Open with a clear marker such as "In this paper we make three contributions. First, … Second, … Third, …". Mix conceptual / methodological / empirical; do not write "extensive experiments" as a contribution.
5. **Result preview.** One or two sentences with your strongest numerical evidence, primed so the reviewer reads on with expectation.

Embed **Figure 1** at the end of the Introduction (or at the start of Section 3 if methodology-heavy). Use the `stage4_framework_figure.png` discovered in Step 1.5. The figure caption must be self-contained — readable on its own as a one-paragraph summary of the paper.

**Avoid** "we are the first to…" unless you can defend it against the entire Stage 2 corpus. Use "to the best of our knowledge" or, better, describe the contribution itself without making a primacy claim.

### Section 4 — Related Work (positioning, not a bibliography)

Function: convince the reviewer you know where you stand and how you differ from the **closest** prior work.

**Structure** (mandatory):

- Two to four **thematic sub-sections**, each named for a methodological lineage (e.g. *Curiosity-Driven Exploration*, *Graph-Based Methods*). Do not organise by year or list papers one per line. Sub-section *order* is your editorial choice; do not bake numbers like `4.1` into the heading text — see §9a / §9b for why.
- Within each sub-section, three moves in order:
  1. What this line of work does
  2. Its common limitation
  3. **How your work differs**
- A final **positioning paragraph** (§2.4) that cites the 2–3 closest works inline and states the differential in one sentence per work: "Unlike `[Author, Year]`, who …, we …".

**Citation coverage (hard rule)**: at least 80 % of the Stage 2 corpus must appear inline in this section (or in Section 5 for foundational works directly cited there). Any drop must be justified in `submit_result()`. *Coverage is measured against the §2.7 citation plan.*

**Length discipline**: Related Work is not "longer is better". It serves contribution clarity. Each cited paper must earn its line.

### Section 5 — Methodology (reproducible + understandable)

Sub-structure (in order):

1. **Preliminaries / Problem Formulation.** Formalise the problem, introduce notation. Every symbol used later traces to its definition here. Symbols are stable across the paper — no mid-paper letter swaps.
2. **Method overview.** A short paragraph that paints the forest before the trees, paired with the framework figure from Step 1.5. Build a mental model first; details come after.
3. **Component-by-component.** For each design decision, answer two questions: **what** is it, and **why this and not that obvious alternative?** Spotlight papers read as if every step were forced; mediocre papers read as a pile of tricks.
4. **Intuition next to formality.** Every equation gets one sentence of intuition adjacent to it ("intuitively, this term encourages …"). Reviewers scan; raw equation blocks are skipped.
5. **Algorithm box / pseudocode / complexity.** Write the core procedure as a numbered algorithm with inputs and outputs declared. Add a one-line complexity note where applicable.

**Reproducibility floor**: a competent doctoral student should be able to rebuild your system from the Methodology plus appendix. If they cannot, you have not written enough.

If `stage4_framework_figure.png` was discovered in Step 1.5, embed it once in this section as Figure 1 (or, if you already placed it in Section 3, reference it via `Figure 1`). The exact markup depends on the output format — see Step 8 per-branch rules.

### Section 6 — Experimental Setup (RQ-framed)

Open by listing the RQs from §2.6 verbatim: "Our experiments answer the following questions: RQ1 …; RQ2 …; RQ3 …". Then commit to the mapping: each subsection of Section 7 answers exactly one RQ.

Then state in full:

- **Datasets** — name, scale, split protocol
- **Baselines** — strong and **fair**: same compute, same backbone, same prompt budget. A weak baseline that lets you "win" is a reviewer red flag, not a strength.
- **Metrics** — name, direction (↑ or ↓), source
- **Implementation details** — model, hyper-parameters, hardware, seed count

All of these are *verbatim from Stage 5*, with hardware / seed counts from Stage 6 layered on top.

### Section 7 — Results (claim → evidence → analysis)

Subsections map 1:1 to the RQs from §2.6. Each subsection has the same three-move structure:

1. **Headline.** A one-sentence claim ("RQ1 is answered affirmatively: the hybrid beats the best singleton by 8.3 pp on TSR, *p* < 0.01."). Tag this sentence to the corresponding `⟨L…⟩` quant.
2. **Evidence.** The supporting table or figure, with caption containing the takeaway. Bold the best value per row; underline the second-best; align decimals; label `↑` / `↓` direction; report mean ± std or 95 % CI.
3. **Analysis.** *Why* the result holds and *when* it fails. This is the spotlight differentiator. Run failure-case analysis, scaling behaviour, backbone-independence, sensitivity to hyper-parameter, qualitative samples. Pre-empt the reviewer's "but what if …" by answering it here.

**Ablation subsection (mandatory if ablation data exists)**: prove that each component of your method earns its keep. Drop component A, report the delta; drop B, report the delta. If a component does not move the metric, either delete it from the method or explain why it is still required.

**Anti-overclaim discipline**: for each sentence you write, ask "does the table actually support this?" If your method wins in 1 of 5 settings, write "we observe a gain in setting X; results are comparable in Y and Z". Never write "our method is better" when "our method is better in X" is the honest statement.

### Section 8 — Discussion

Interpretation grounded in Stage 7. Separate **evidence** from **speculation**; flag speculation with phrases such as "we conjecture", "this suggests, though not directly tested, that …", and tag with `⟨spec⟩`. Speculation passed off as result is the single most common automatic-reject trigger for the Stage 9 critic.

### Section 9 — Limitations

Be proactive. Cover:

- Scope — which settings were tested, which were not
- Dataset bias
- Baseline coverage
- Computational cost
- Reproducibility caveats from Stage 6

Stating a limitation yourself reduces the attack surface; refusing to state one and being caught doubles the damage. Confident but honest beats triumphalist every time.

### Section 10 — Conclusion (short)

Restate the core contribution in **different words** from the Introduction (no copy-paste). One or two sentences of substantive future work (a direction, not a TODO list). Do not introduce new content, data, or claims.

### Section 11 — References

See the `citation-management` skill. Sorted, deduplicated, ≥ 80 % Stage 2 coverage, every entry inline-cited at least once in Sections 3–10.

---

## Step 5 — Draft the Abstract Last

Write the body sections first. Only after the body is complete, write the Abstract by summarising what you already wrote. This prevents the abstract from making claims the body does not support. Tag abstract sentences too: every abstract sentence must restate a body sentence that is itself `⟨L…⟩`-sourced. The abstract introduces no new ledger reference and no claim the body did not already make.

---

## Step 6 — Self-Audit and Strip Tags

You now have a fully tagged draft (body plus abstract). Do not emit any format yet. Run this audit, in order:

1. **Untagged-sentence sweep.** Read every sentence of the body. Any sentence with no `⟨…⟩` tag is unaccounted for: attach the correct ledger id, demote it to `⟨—⟩` if it truly carries no claim, or delete it. After this sweep, **every** body sentence has exactly one tag.
2. **Speculation check.** For each `⟨spec⟩` sentence, confirm it sits in Discussion and is hedged. If a `⟨spec⟩` sentence reads as a flat assertion, reword it as a conjecture or cut it.
3. **Connective budget.** Count `⟨—⟩` sentences. If they exceed roughly one per section, you are padding; the usual cause is the "three substantive sentences per paragraph" rule pushing you to invent filler. Prefer a shorter, fully-sourced paragraph over a padded one. **Traceability outranks the paragraph-length style rule whenever they conflict.**
4. **Abstract back-check.** Confirm each abstract sentence maps to an `⟨L…⟩`-sourced body sentence.
5. **Quant spot-check.** For each `⟨L…⟩` of type `quant`, compare the number in your prose against the ledger fragment character-by-character. No rounding, no reformatting.
6. **Citation coverage check.** Count distinct Stage 2 papers cited inline in the body. Compute `|inline cited Stage 2 papers| / |Stage 2 corpus|`. If the ratio is below 80 %, return to Section 4 (Related Work) and add the missing papers (per the §2.7 plan), then re-run the audit.

Only after all six pass, **strip the tags**: remove every `⟨…⟩` token plus any stray whitespace it leaves behind. The result is the clean, tag-free synthesised content that Step 8 emits in the requested format. Whatever files Step 8 writes (Markdown, LaTeX, Word, or PDF) **must contain zero `⟨` characters**. A surviving tag is itself an automatic Stage 9 reject, so verify before submitting.

---

## Step 7 — Writing Craft Pass

After tags are stripped, audit the body once more for craft. Repair each violation in place.

- **Topic sentence per paragraph.** The first sentence of every body paragraph must convey the paragraph's main point on its own — a reader skimming only first sentences should understand the section.
- **Tell-tell-tell signposting.** Long sections open with "In this section we…" and (if warranted) close with a one-sentence summary. Subsections do the same in miniature.
- **Define before use.** Every abbreviation, symbol, and term is defined on first use and used identically thereafter. Drift (renaming the same thing across sections) exhausts reviewers and is a leading cause of low-confidence scores.
- **Banned adjectives**, full body sweep. Replace or delete every instance:
  - `novel`, `new`, `significant`, `extensive`, `comprehensive`, `powerful`, `robust`, `efficient`, `state-of-the-art` (as an adjective), `cutting-edge`, `groundbreaking`, `revolutionary`
  - These convey no information because every paper claims them. Let mechanism and numbers speak.
  - Exception: `state-of-the-art` is allowed *as a hyphenated compound modifier* describing a known concept (e.g. "state-of-the-art models such as GPT-4"); it is banned as a stand-alone descriptor of your own work.
- **Active voice preferred.** "We optimise" beats "Optimisation is performed". Reserve passive for cases where the agent is unimportant.
- **Forward references resolve.** If you write "as shown in Section 4", Section 4 must contain that content.
- **Mention equals cite.** Every paper, method, framework, or system name that appears in the body must be followed immediately by an inline `[Author, Year]` marker on first mention. Naming "SENSEI" without `[Sancaktar et al., 2025]` is a citation violation, not a stylistic choice.
- **Voice and tense.** Third person present tense for the work itself ("We propose a method that …"); past tense for experiments performed ("Models were trained on the dataset described in Section 4.").
- **British English** throughout: `-ise`, `-our`, `-re` spellings; `behaviour`, `colour`, `optimise`, `analyse`, `modelling`, `towards`. Never `color`, `optimize`, `behavior`, `modeling`. Keep table and figure captions from Stage 7 unchanged even if the original used American spellings; quote any direct citation verbatim without silent re-spelling.
- **No bold** in body. No `**text**`. Use single-asterisk *italics* sparingly for true emphasis; a whole paper should contain only a handful of italicised emphases.
- **No bullet points or numbered lists in body sections.** Convert every enumeration into running prose ("First, … Second, … Third, …"). Section and subsection *headings* are allowed and expected; *lists* within a section are not. The References section is the sole exception.
- **No em-dashes (—) or en-dashes (–).** Use commas, semicolons, colons, parentheses, or full stops to restructure. The plain hyphen is allowed only for compound modifiers (`state-of-the-art`, `fine-tuning`) and numeric ranges inside tables (`2017-2024`).
- **No stub paragraphs.** Every body paragraph contains at least three substantive sentences and develops a single idea. Merge thin paragraphs. *However*, traceability outranks paragraph length: a two-sentence paragraph of fully-sourced prose is better than a three-sentence paragraph padded with a `⟨—⟩` filler line (the connective budget already enforced this in Step 6).
- **Punctuation (BrE).** Single quotation marks for direct speech, double quotes nested inside; full stops and commas go OUTSIDE the closing quote when the quoted fragment is not a full sentence.
- **Date format.** *15 May 2026*, not *May 15, 2026*.

Apply these rules to **all** output formats — LaTeX, Word, Markdown, PDF. Translate the *form* (markdown `*italic*` vs LaTeX `\textit{}` vs Word italic) but never the *rule*.

---

## Step 8 — Reviewer Quick-Path Audit

Top-conference reviewers are time-constrained, fatigued, and default-sceptical. They read in this order, often stopping after any anchor fails to land:

1. **Title**
2. **Abstract**
3. **Figure 1 + its caption**
4. **Contribution list (in Introduction)**
5. **Main result table (in Section 7)**
6. **Conclusion**

Read these six anchors in isolation, ignoring all other text. They must (a) **independently** convey the contribution and (b) be **mutually consistent**. The dominant failure mode is the abstract claiming one headline number while the main table shows another, or the conclusion summarising a different contribution from the Introduction. Fix any inconsistency before proceeding to Step 9.

A practical test: if a busy reviewer reads only these six, can they correctly state — in one sentence — what you contributed? If no, the quick path has not landed; revise.

---

## Step 9 — Dispatch to Output Format

The synthesised content (clean, tag-free from Step 6, audited in Steps 7 and 8) stays the same regardless of format; only the *carrier* changes.

Parse the task description for an `output_format` directive. The grammar is intentionally minimal:

- `output_format=markdown` (or no directive at all) → **default behaviour** — single Markdown file
- `output_format=latex venue=iclr2026` → ICLR 2026 LaTeX project (source only, not compiled)
- `output_format=latex venue=neurips2026` → NeurIPS 2026 LaTeX project (source only, not compiled)
- `output_format=latex venue=aaai2027` → AAAI-27 LaTeX project (source only, not compiled)
- `output_format=docx` → academic Word document
- `output_format=pdf venue=<venue>` → LaTeX project compiled to PDF
- `output_format=both venue=<venue>` → emit Markdown AND LaTeX (skip docx and pdf unless explicitly requested)

If `venue=` is missing for a `latex`, `pdf`, or `both` request, default to `iclr2026` and warn in your `submit_result()` summary.

### 9a. Markdown branch (default)

1. `write()` the synthesised content to `stage8_paper_writer.md`, following the **heading rules** in step 2 below.
2. **Markdown heading rules — no hand-written section numbers.**
   The §4.2 "Section N — Title" naming is the *spec* for *which* sections must appear; the markdown heading itself carries only the **name**, never the number. Downstream consumers (pandoc → LaTeX, NeurIPS PDF builders, web renderers) auto-number headings — hand-written numbers stack on top and produce "0.1 1. Introduction" double-numbering. Use this hierarchy:
   - `#` — the paper title from §4.2 Section 1. Exactly one `#` in the file.
   - `##` — each top-level body section from §4.2 (Abstract, Introduction, Related Work, Methodology, …, Conclusion, References). The Abstract heading is the literal word `Abstract`, not `## 1. Abstract` and not `## Section 2 — Abstract`.
   - `###` — sub-sections (Related Work themes, Methodology components, Results-per-RQ, etc.).
   - Use heading **text only**: `## Introduction` ✓, `## 1. Introduction` ✗, `## Section 3 — Introduction` ✗. For sub-sections: `### Curiosity-Driven Exploration` ✓, `### 4.1 Curiosity-Driven Exploration` ✗.
   - Apply the rule consistently to figures and tables in body text — write captions as prose ("Figure 1: …"), but never start a markdown heading line with a number.
3. For each figure recorded in Step 1.5, include a standard markdown image reference inline at the appropriate section, e.g. `![Figure 1: Overview of the proposed framework.](stage4_framework_figure.png)`. Paths are relative to the workspace; do **not** copy the PNG anywhere — `stage8_paper_writer.md` lives in the same workspace directory as the figure file.
4. Proceed to Step 10.

### 9b. LaTeX branch

1. Call `fetch_latex_template(venue=<venue>, dest_dir="<workspace>/stage8_paper")`. This vendored-template tool copies the venue's `.sty`, `.bst`, `main.tex` starter, `references.bib`, and `figures/` directory into `dest_dir`.
2. Read the returned `main_tex_path` to see the skeleton structure.
3. Build the full filled-in `.tex` content in your scratchpad. The eleven mandatory sections from Step 4 map cleanly onto the LaTeX `\section{}` structure already in the starter — replace its placeholder text with your synthesised content.
4. Translate Markdown conventions to LaTeX as you write:
   - `[Author, Year]` inline cites → `\citep{author_year}` (with a corresponding `references.bib` entry)
   - `*italics*` → `\emph{italics}` (sparingly)
   - Section headers → `\section{}`, `\subsection{}`. Pass the **name only** into the braces (`\section{Introduction}`, not `\section{1. Introduction}`) — LaTeX auto-numbers; a hand-written prefix produces "1 1. Introduction" double-numbering.
   - Tables → LaTeX `tabular` environments
   - Display equations → `\begin{equation}…\end{equation}`
   - `[TODO: missing from Stage N]` markers → keep them verbatim
5. **Figures.** For each figure recorded in Step 1.5:
   - Copy the PNG into the template's `figures/` directory, e.g. `cp <workspace>/stage4_framework_figure.png <dest_dir>/figures/`.
   - In the corresponding section, emit a `figure` environment:
     ```latex
     \begin{figure}[t]
       \centering
       \includegraphics[width=\linewidth]{figures/stage4_framework_figure.png}
       \caption{Overview of the proposed framework.}
       \label{fig:methodology}
     \end{figure}
     ```
   - Reference it in body prose with `Figure~\ref{fig:methodology}`.
6. `write()` the complete filled-in `.tex` content to `<dest_dir>/main.tex` (overwriting the starter).
7. `write()` populated `<dest_dir>/references.bib` — one BibTeX entry per citation, sourced exclusively from Stage 2.
8. Note in `submit_result()` that the deliverable is the project at `<dest_dir>` (not a single file).

### 9c. Docx branch

1. Build the section content as a Python dict `{header: body}` in your scratchpad — keys numbered like `"1. Introduction"`, `"2. Related Work"`, etc. (Numbers in the dict keys are correct *only here*: `render_docx` writes each key verbatim as a heading and does not auto-number, so you supply the numbering. This is the opposite of the markdown / LaTeX branches.)
2. For each figure recorded in Step 1.5, build a figure descriptor: `{"path": "<abs path to PNG>", "caption": "<caption from prior stage>", "section": "<exact key from sections>"}`. The `section` value must match a key in `sections` byte-for-byte (typically `"3. Methodology"` for `stage4_framework_figure.png`) — otherwise the figure is appended to the end of the body and a warning is recorded.
3. Call `render_docx(title=…, authors=…, abstract=…, sections={…}, references=…, figures=[…], output_path="<workspace>/stage8_paper_writer.docx", venue=<venue or "generic">)`.
4. The tool produces a two-column academic Word document with images embedded at the end of their target section. If `python-docx` is not installed in the OMC venv, the tool returns a clear error — in that case, fall back to writing Markdown and warn in `submit_result()` that docx output was unavailable.

### 9d. Both branch

1. Run **9a** to produce `stage8_paper_writer.md`.
2. Then run **9b** to produce the LaTeX project at `<workspace>/stage8_paper/`.

### 9e. PDF branch

1. Run **9b** in full to materialise and fill in the LaTeX project at `<dest_dir> = <workspace>/stage8_paper`. The PDF path reuses the LaTeX path; do not author content twice.
2. Call `compile_latex(project_dir="<dest_dir>")`. It compiles `main.tex` with the host TeX distribution (`latexmk` if present, otherwise `pdflatex` with a BibTeX pass) and returns `pdf_path` on success.
3. If `compile_latex` returns `status="error"`, do not discard the work: the filled-in LaTeX project is still a valid deliverable. Report the failure and the returned `log_tail` in `submit_result()`, and note that the PDF could not be produced (for example, no TeX distribution on the host, or a LaTeX error in `log_tail`). The deliverable then degrades to the LaTeX project, exactly as `output_format=latex`.
4. On success, the deliverables are both the compiled `pdf_path` and the LaTeX project alongside it.

### Format-agnostic rules

- All Step 7 craft rules apply to every output format. Translate the *form*, not the *rule*.
- Traceability rules apply identically: every claim still traces to a Stage 1-7 file, regardless of carrier. The claim-ledger discipline from Step 3 and the inline-tag audit from Step 6 are carrier-independent; tags are stripped before any format is emitted, so no carrier may reintroduce an untraced claim.
- The eleven mandatory sections from Step 4 must all be present in every format.

---

## Step 10 — Submit

1. Confirm the deliverable exists at the expected path (single file for markdown/docx, directory for latex/both/pdf) and that no `⟨…⟩` tag survived into it.
2. Call `submit_result()` with a one-paragraph summary containing all of the following:
   - **Output format used and path(s).**
   - **Body word count** across all body sections.
   - **Section list** (the eleven mandatory section names actually present).
   - **Argument design summary**: one-sentence contribution (§2.1), mechanism-level gap (one clause from §2.2), insight (§2.3).
   - **Claim ledger size** (number of entries, broken down by `type`).
   - **Sentence accounting**: how many `⟨L…⟩` sourced, `⟨—⟩` connective, `⟨spec⟩` speculation, before strip.
   - **Confirmation that the deliverable is tag-free.**
   - **Citation coverage**: count of Stage 2 papers cited inline, total Stage 2 corpus size, percentage. Target ≥ 80 %.
   - **References dropped** (if any): each paper in the §2.7 citation plan that did not make it into the final paper, with the reason.
   - **Banned-adjective sweep**: confirm zero occurrences of `novel`, `significant`, `extensive`, etc. in the body (or report any that remain with reason — typically none).
   - **Reviewer quick-path audit result**: confirm the six anchors are mutually consistent, or list inconsistencies.
   - Any inline `[TODO: missing from Stage N]` markers — count and the sections they appear in.
   - **Format-specific**:
     - For LaTeX: number of BibTeX entries written; whether any inline cites lack matching `.bib` entries.
     - For docx: whether `python-docx` was available; warnings returned by `render_docx`; `figure_count`.
     - For PDF: the engine `compile_latex` used and the `pdf_path`; if compilation failed, the `log_tail` and the fact that the deliverable degraded to LaTeX source only.

---

## What Happens Next

Your output flows directly into **Stage 9** (`adversarial-critic` with skill `peer_reviewer`). Drafts with hallucinated claims, missing sections, untraced numbers, unflagged speculation, low citation coverage, surviving tags, or banned adjectives will be **REJECTED** and rerun. Optimise for **traceability, completeness, citation coverage, and quick-path consistency over novelty**.

## Top Failure Modes (avoid these)

| Failure | Why it gets rejected |
|---|---|
| Writing a fluent, plausible sentence with no ledger entry | The A→A+B elaboration; untraceable; automatic reject |
| Leaving a `⟨…⟩` tag in any emitted deliverable | Strip step skipped or incomplete; automatic reject |
| Stating an interpretation without `⟨spec⟩` plus hedging | Speculation presented as result; automatic reject |
| Padding paragraphs with connective filler to reach three sentences | Inflated `⟨—⟩` budget; prefer shorter sourced prose |
| Citing a paper not in Stage 2 | Untraceable; critic flags as hallucination |
| Citing fewer than 80 % of Stage 2's corpus without justification | Citation coverage failure; runbook violation |
| Mentioning a paper by name without an inline `[Author, Year]` marker | Citation hygiene failure; runbook violation |
| Rounding or rewording a number from Stage 7 | Quantitative drift; critic flags as misreporting |
| Skipping the Limitations section | Mandatory section is missing; automatic reject |
| Writing the abstract first | Often inconsistent with body; quick-path audit fails |
| Using marketing adjectives (*novel*, *significant*, *robust*, …) | Style violation; auto-reject |
| Inventing a baseline, dataset, or result not in Stages 5-7 | Untraceable; automatic reject |
| Using `**bold**`, bullet points, or em-dashes in body | Style violation; auto-reject |
| One- or two-sentence paragraph in any body section | Stub paragraph; auto-reject (unless traceability requires brevity, per Step 6 connective-budget rule) |
| American spellings (*color*, *optimize*, *behavior*, *toward*) | Language violation; auto-reject |
| Generic gap statement ("existing methods are not good enough") | Mechanism-level gap missing; quick-path audit fails |
| "We propose a novel framework" as a contribution | Vacuous contribution; quick-path audit fails |
| Title that describes the field rather than the contribution | Quick-path failure on Anchor 1 |
| Abstract claim that the main table does not literally support | Overclaim; auto-reject |
