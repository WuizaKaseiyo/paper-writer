---
name: citation-management
version: 1.0.0
description: "How to maintain a single source of truth for citations across the paper, sourced exclusively from the literature survey (Stage 2)."
author: AutoResearch
---

# Citation Management

## Source of Truth

**Every** citation in the paper MUST appear in `stage2_literature_surveyor.md`. You do NOT add new citations during paper writing.

- If the methodology references a technique not surveyed → write `[CITATION NEEDED]` inline. The critic will catch this; that's fine. Inventing a reference is not fine.
- If Stage 2 has zero references → the References section says: `_No external references — all claims derive from primary experimental work performed in this pipeline run._`

## Inline Format

Always `[Author, Year]`. Examples:

| Authors | Inline |
|---|---|
| Single author | `(Vaswani, 2017)` |
| Two authors | `(Brown & Mann, 2020)` |
| Three or more | `(Bommasani et al., 2021)` |
| Same author, same year, multiple papers | `(Smith, 2023a)`, `(Smith, 2023b)` |

If Stage 2 used numeric citations (`[1]`, `[2]`), match Stage 2's choice instead. Consistency with Stage 2 outweighs personal preference.

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

## Reporting

In your final `submit_result()` summary, list:
- Total number of unique references in the paper
- Any inline `[CITATION NEEDED]` markers (count + which sections)
- Any references you had to drop (with the reason)

The Stage 9 critic uses this report to triage review priority.
