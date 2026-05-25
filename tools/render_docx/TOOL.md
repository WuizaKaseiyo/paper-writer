---
name: render_docx
description: Render synthesized paper sections into an academic .docx (Word) file. Times New Roman 11pt, two-column body, single-column abstract + references, basic equation + table support. Requires python-docx installed in the OMC venv.
---

# render_docx

When the task specifies `output_format=docx`, call this **after** you have
synthesized the full paper content from Stage 1-7 into a structured form.

## Arguments

| Arg | Type | Default | Purpose |
|-----|------|---------|---------|
| `title` | str | `""` | Paper title — centered 14pt bold |
| `authors` | str | `""` | One author per line; centered 11pt |
| `abstract` | str | `""` | Abstract body — single-column with italic "Abstract." prefix |
| `sections` | dict[str, str] | (required) | Ordered: section header → body markdown. Keys appear as bold section headings in document order. |
| `references` | str | `""` | References block — one entry per line. Single-column, hanging indent, 10pt. |
| `output_path` | str | (required) | Absolute path for the output `.docx` |
| `venue` | str | `"generic"` | Informational — saved into doc properties |

## How to populate `sections`

The keys become the section headers. **You** number them (the tool does not
auto-number) — this lets you control structure without fighting the tool:

```python
sections = {
    "1. Introduction": "Motivation paragraph 1...\n\nMotivation paragraph 2...",
    "2. Related Work": "...",
    "3. Methodology": "...",
    "3.1 Loss Function": "...",
    "4. Experimental Setup": "...",
    "5. Results": "...",
    "6. Discussion": "...",
    "7. Limitations": "...",
    "8. Conclusion": "...",
}
```

Each value is **markdown-style** text:
- Paragraphs separated by blank lines
- Inline `[Author, Year]` citations preserved as plain text
- Display equations as `$$expression$$` on their own paragraph
- Simple tables in markdown pipe syntax

## What it produces

Two-column body wrapping all `sections`, with single-column title/abstract/refs:

```
+----------------------------------------------------+
|                    Title (14pt bold)                |
|                  Authors block (11pt)                |
|                                                      |
|         Abstract. body justified ...                |
+----------------------------------------------------+
| 1. Introduction         | 2. Related Work          |
|                         |                          |
|  body justified         |  body justified          |
|  body justified         |  body justified          |
+----------------------------------------------------+
|                    References                       |
|  Smith J., 2024, ... (hanging indent)               |
+----------------------------------------------------+
```

## Dependencies

`python-docx` must be installed in the OMC venv:

```bash
cd /path/to/Memento-Research
.venv/bin/pip install python-docx
```

Without it, the tool returns a clear error directing the user. The other
two output paths (`markdown` and `latex`) work without `python-docx`.

## What this tool does NOT do

- Doesn't auto-format citations to a venue style (e.g. ACM/IEEE/Springer) — you write them as plain text
- Doesn't auto-number sections — you put "1. ", "2. " etc. in the keys
- Doesn't render LaTeX math (equations are shown as text in italics)
- Doesn't generate per-venue templates (use the LaTeX path for that)

For high-fidelity venue formatting, prefer `output_format=latex` and the
ICLR/NeurIPS templates from paper-templates.
