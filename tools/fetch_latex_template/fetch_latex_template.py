"""fetch_latex_template — clone the paper-templates repo and copy a venue subdir.

Self-contained LangChain @tool using only stdlib + langchain_core (and the
host system's `git` binary). No Python dependencies beyond what OMC already
ships.

When called from inside a Stage 8 task, this clones (or refreshes) the
paper-templates repo into a sandbox cache, then copies the requested venue
subdirectory into <dest_dir> so the LLM can overwrite main.tex with the
synthesized paper content.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

DEFAULT_REPO_URL = "https://github.com/WuizaKaseiyo/paper-templates.git"
VALID_VENUES = ("iclr2026", "neurips2026")
CLONE_TIMEOUT_S = 60

# Process-local cache so back-to-back calls in the same OMC run don't re-clone.
_clone_cache: dict[str, Path] = {}


@tool
def fetch_latex_template(
    venue: str,
    dest_dir: str,
    use_latest: bool = True,
    repo_url: str = DEFAULT_REPO_URL,
) -> dict[str, Any]:
    """Clone the paper-templates repo and copy a venue template into dest_dir.

    Sets up an editable LaTeX project so the LLM can fill in main.tex with
    the synthesized paper content from Stage 1-7.

    Args:
        venue: One of "iclr2026" or "neurips2026".
        dest_dir: Where to place the copied template (typically the project
            workspace, e.g. "/path/to/project/stage8_paper").
        use_latest: If True (default), git pulls latest each call. If False
            and a cached clone exists, reuses it (faster, offline-friendly).
        repo_url: Override the template repo. Default is the public
            WuizaKaseiyo/paper-templates repo.

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

    dest = Path(dest_dir).expanduser().resolve()

    warnings: list[str] = []

    # ── Clone or refresh the cache ───────────────────────────────────────
    cache_key = repo_url
    clone_root = _clone_cache.get(cache_key)

    if clone_root and clone_root.exists() and use_latest:
        # Try git pull on the cached clone
        try:
            _run_git(["pull", "--quiet"], cwd=clone_root)
        except Exception as e:
            warnings.append(f"git pull failed: {e}; using cached snapshot")
    elif not clone_root or not clone_root.exists():
        # Fresh clone
        clone_root = Path(tempfile.mkdtemp(prefix="paper_templates_clone_"))
        try:
            _run_git(["clone", "--depth=1", "--quiet", repo_url, str(clone_root)])
        except Exception as e:
            return {"status": "error", "error": f"git clone failed: {e}"}
        _clone_cache[cache_key] = clone_root

    src_venue_dir = clone_root / venue
    if not src_venue_dir.is_dir():
        available = [d.name for d in clone_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
        return {
            "status": "error",
            "error": f"venue {venue!r} not found in cloned repo; available: {available}",
        }

    # ── Copy venue files to dest ─────────────────────────────────────────
    try:
        dest.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {"status": "error", "error": f"cannot create dest_dir {dest}: {e}"}

    files_copied: list[str] = []
    skipped_files = {
        "README.md",                # template README — not for the paper itself
        "official_template.tex",    # reference only, don't ship into paper
    }
    for item in src_venue_dir.iterdir():
        if item.name in skipped_files:
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


def _run_git(args: list[str], cwd: Path | None = None) -> str:
    """Synchronously run git with the given args. Raise on non-zero exit."""
    proc = subprocess.run(
        ["git"] + args,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=CLONE_TIMEOUT_S,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},  # no interactive auth prompts
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} → exit {proc.returncode}: {proc.stderr.strip()[:300]}"
        )
    return proc.stdout
