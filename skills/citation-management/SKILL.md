---
name: citation-management
version: 2.0.0
description: "How to maintain a single source of truth for citations across the paper, sourced exclusively from the literature survey (Stage 2). Encodes the bidirectional coverage rule (Stage 2 → paper and paper → Stage 2) and the mention-equals-cite hygiene rule that paper_writer relies on."
author: AutoResearch
---

# Citation Management

This skill is invoked from the `paper_writer` runbook (Stage 8) to govern every citation in the final paper. The rules below are bidirectional and mandatory.

## Source of Truth (forward direction)

**Every** citation in the paper MUST appear in `stage2_literature_surveyor.md`. You do NOT add new citations during paper writing.

- If the methodology references a technique not surveyed → write `[CITATION NEEDED]` inline. The Stage 9 critic will catch this; that is fine. Inventing a reference is not fine.
- If Stage 2 has zero references → the References section says: `_No external references — all claims derive from primary experimental work performed in this pipeline run._`

## Coverage (reverse direction, ≥ 80 %)

**At least 80 % of the papers surveyed in Stage 2 MUST be cited at least once inline in the final paper body** (Sections 3–10 — Introduction through Conclusion). Stage 2 has already filtered the literature for relevance; do not re-filter at Stage 8. The default disposition of every Stage 2 paper is *include*.

This rule exists because the original runbook's instruction to "note the 5–10 most-cited related works" caused the LLM to cherry-pick a small minority of Stage 2's corpus and silently drop the rest. A four-reference paper after a 28-paper survey is a runbook failure, not a stylistic choice. The coverage requirement closes that loophole.

**Dropping a paper is allowed only with cause.** If a Stage 2 paper genuinely cannot be cited — e.g. retracted, duplicate of another corpus entry, paywalled with no recoverable metadata — list it in `submit_result()` under `references dropped` with a one-sentence reason. Do not silently omit.

A practical workflow:

1. In `paper_writer` Step 2.7, enumerate the Stage 2 corpus and pre-allocate each paper to a section.
2. Most papers go in Related Work (taxonomy + positioning); foundational works also appear in Methodology; ablation comparisons appear in Results.
3. After the body is written, count distinct inline cites and divide by Stage 2's corpus size. Below 80 %? Revise Related Work and Methodology to cite the missing papers, or list them as drops with reason.

The `paper_writer` Step 6 audit (Self-Audit and Strip Tags) enforces this check as audit item 6 and refuses to strip tags until coverage clears the threshold.

## Mention Equals Cite (citation hygiene)

**Every paper, method, framework, system, dataset, or benchmark name that appears in the body MUST be followed immediately, on first mention, by an inline `[Author, Year]` marker.**

This rule closes a separate failure mode: the original runbook allowed the LLM to write "SENSEI framework", "CLIP-based intrinsic rewards", "MERCI", "CDE" — naming the work without attaching the citation marker. The paper would then list the works in References (because the LLM listed them in its scratchpad), but never inline-cite them, defeating the traceability contract.

Concretely:

| Pass | Fail |
|---|---|
| `The SENSEI framework [Sancaktar et al., 2025] distills…` | `The SENSEI framework distills…` |
| `Random Network Distillation [Burda et al., 2019] uses…` | `Random Network Distillation uses…` |
| `On the ARC-AGI-3 benchmark [Chollet, 2024], we…` | `On the ARC-AGI-3 benchmark, we…` |

Subsequent mentions of the same work need not repeat the marker; first mention in each section is sufficient.

## Inline Format

**Square brackets, not parentheses.** Always `[Author, Year]` — the opening token is `[`, never `(`. This is non-negotiable: `(Author, Year)` is a citation-format violation, not a stylistic choice.

| Authors | Correct | Wrong |
|---|---|---|
| Single author | `[Vaswani, 2017]` | `(Vaswani, 2017)` |
| Two authors | `[Brown & Mann, 2020]` | `(Brown & Mann, 2020)` |
| Three or more | `[Bommasani et al., 2021]` | `(Bommasani et al., 2021)` |
| Same author, same year, multiple papers | `[Smith, 2023a]`, `[Smith, 2023b]` | `(Smith, 2023a)`, `(Smith, 2023b)` |

In body prose, the markers appear inline with the sentence: `The SENSEI framework [Sancaktar et al., 2025] distills…`, never `The SENSEI framework (Sancaktar et al., 2025) distills…`.

The square-bracket form is what the LaTeX dispatch (`\citep{author_year}` conversion) and the `references.bib` mapping expect, and it matches the `[CITATION NEEDED]` placeholder shape so the Stage 9 critic can grep for citation presence with a single regex (`\[`).

**Exception — numeric citations.** If `stage2_literature_surveyor.md` itself used numeric form (`[1]`, `[2]`, …), match Stage 2's choice instead. Consistency with Stage 2 outweighs personal preference. **No other exception exists**; do not switch to parentheses because they "look more natural" or because a target venue uses them — the dispatch step in `paper_writer` Step 9 handles per-venue conversion downstream.

## References Section

At the end of the paper, output a `## References` section. One entry per line:

```
[1] Vaswani, A., et al. (2017). Attention Is All You Need. NeurIPS.
[2] Brown, T., & Mann, B. (2020). Language Models are Few-Shot Learners. NeurIPS.
```

Rules:

1. **Sort** alphabetically by first author surname, then by year ascending.
2. **Deduplicate** — same paper appears once even if cited multiple times.
3. **Match Stage 2 verbatim.** Do NOT fill in fields Stage 2 did not provide (DOI, page numbers, publisher). Missing fields stay missing.
4. **Drop unreachable refs.** If you cited a paper inline but cannot find it in Stage 2, REMOVE the inline citation. Do not fabricate a reference entry.
5. **Mirror the body.** Every entry in References must be cited at least once inline; conversely, every inline cite must have a References entry. The two sets are equal.
6. **Coverage check.** Compute `|References| / |Stage 2 corpus|` and report it in `submit_result()`. Target ≥ 80 %.

**Note — inline marker vs reference entry are different namespaces.** The parentheses around `(2017)` inside a References *entry* are part of standard bibliographic format (the year is in parentheses by convention), not an inline marker. The square-bracket rule above applies **only** to inline citations in body prose. Do not "fix" the `(YYYY)` inside a References entry to `[YYYY]`; the two layers serve different consumers (human reader vs `\citep{}` dispatcher) and are not interchangeable.

## Reporting

In your final `submit_result()` summary, list:

- Total number of unique references in the paper
- Stage 2 corpus size
- **Coverage percentage** = inline-cited Stage 2 papers ÷ Stage 2 corpus size
- Any inline `[CITATION NEEDED]` markers (count + which sections)
- **References dropped** — each Stage 2 paper not cited in the final paper, with reason
- Any mention-equals-cite hygiene violations you found and repaired in Step 7

The Stage 9 critic uses this report to triage review priority. Coverage below 80 % without justification is an automatic reject signal.
