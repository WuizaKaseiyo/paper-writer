"""fetch_latex_template — copy a bundled venue template into a destination dir.

Self-contained LangChain @tool using only stdlib + langchain_core. The ICLR,
NeurIPS and AAAI templates are vendored into this tool's `templates/`
directory, so this runs fully offline: no network, no `git`, no clone cache.

When called from inside a Stage 8 task, it copies the requested venue
subdirectory into <dest_dir> so the LLM can overwrite main.tex with the
synthesized paper content.

The vendored conference style files (.sty/.bst) are redistributed under their
original authors' terms; see templates/NOTICE for attribution. To refresh them
against upstream, re-copy from https://github.com/WuizaKaseiyo/paper-templates.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

VALID_VENUES = ("iclr2026", "neurips2026", "aaai2027")

# Vendored templates live next to this module: tools/fetch_latex_template/templates/<venue>/
_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Reference-only files that ship in the template dir but should not be copied
# into the paper project itself.
_SKIPPED_FILES = {
    "README.md",             # template README — not for the paper itself
    "official_template.tex", # reference only, don't ship into paper
    "NOTICE",                 # attribution file — never per-venue, but be safe
}


@tool
def fetch_latex_template(
    venue: str,
    dest_dir: str,
) -> dict[str, Any]:
    """Copy a bundled venue LaTeX template into dest_dir.

    Sets up an editable LaTeX project so the LLM can fill in main.tex with
    the synthesized paper content from Stage 1-7. Runs offline from templates
    vendored inside this tool.

    Args:
        venue: One of "iclr2026", "neurips2026" or "aaai2027".
        dest_dir: Where to place the copied template (typically the project
            workspace, e.g. "/path/to/project/stage8_paper").

    Returns:
        {
          "status": "ok" | "error",
          "venue": "...",
          "dest_dir": "/abs/path/to/dest",
          "main_tex_path": "/abs/path/to/dest/main.tex",
          "files_copied": [list of relative paths],
          "instruction": "Now use write() to overwrite main.tex with your paper content",
          "warnings": [...]
        }

    On error: {"status": "error", "error": "..."}.
    """
    venue = (venue or "").strip().lower()
    if venue not in VALID_VENUES:
        return {
            "status": "error",
            "error": f"venue must be one of {VALID_VENUES!r}, got {venue!r}",
        }

    src_venue_dir = _TEMPLATES_DIR / venue
    if not src_venue_dir.is_dir():
        available = (
            [d.name for d in _TEMPLATES_DIR.iterdir() if d.is_dir()]
            if _TEMPLATES_DIR.is_dir()
            else []
        )
        return {
            "status": "error",
            "error": (
                f"bundled template for venue {venue!r} not found at {src_venue_dir}; "
                f"available: {available}"
            ),
        }

    dest = Path(dest_dir).expanduser().resolve()
    warnings: list[str] = []

    try:
        dest.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {"status": "error", "error": f"cannot create dest_dir {dest}: {e}"}

    files_copied: list[str] = []
    for item in src_venue_dir.iterdir():
        if item.name in _SKIPPED_FILES:
            continue
        rel_dest = dest / item.name
        try:
            if item.is_dir():
                if rel_dest.exists():
                    shutil.rmtree(rel_dest)
                shutil.copytree(item, rel_dest)
                for sub in rel_dest.rglob("*"):
                    if sub.is_file():
                        files_copied.append(str(sub.relative_to(dest)))
            else:
                shutil.copy2(item, rel_dest)
                files_copied.append(item.name)
        except Exception as e:
            warnings.append(f"copy {item.name} failed: {e}")

    main_tex = dest / "main.tex"
    if not main_tex.exists():
        return {
            "status": "error",
            "error": f"main.tex not produced at {main_tex}; copy_log={files_copied}",
        }

    return {
        "status": "ok",
        "venue": venue,
        "dest_dir": str(dest),
        "main_tex_path": str(main_tex),
        "files_copied": sorted(files_copied),
        "instruction": (
            f"Template ready at {dest}. Use write() to overwrite "
            f"{main_tex.name} with the synthesized paper content. "
            f"Update references.bib with cited works from Stage 2. "
            f"Drop any figures into {dest}/figures/."
        ),
        "warnings": warnings,
    }
