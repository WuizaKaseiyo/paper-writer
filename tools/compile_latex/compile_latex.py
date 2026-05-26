"""compile_latex — compile a LaTeX project to PDF.

Self-contained LangChain @tool using only stdlib + langchain_core. Shells out
to a TeX distribution that must already be on the host's $PATH (MacTeX, TeX
Live, MiKTeX, or a standalone `latexmk` / `pdflatex`). No Python dependencies.

This is the final step of the LaTeX output path: `fetch_latex_template` lays
down the venue project, the LLM overwrites `main.tex` and `references.bib`,
then this tool turns that project into a `main.pdf`.

Design notes:
- When `engine="auto"`, prefer `latexmk` (it figures out how many passes and
  whether BibTeX/Biber is needed). If `latexmk` is absent, fall back to a manual
  pdflatex -> bibtex -> pdflatex -> pdflatex sequence.
- Shell escape (`\\write18`) is disabled on every direct engine call so a
  hostile `.tex` cannot run arbitrary commands during compilation.
- LaTeX commonly exits non-zero on mere warnings while still emitting a valid
  PDF, so success is judged by "a fresh, non-empty PDF exists", not by the exit
  code. The exit code and a tail of the `.log` are always reported for triage.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from langchain_core.tools import tool

# Engine preference when engine="auto" and latexmk is unavailable.
_PDF_ENGINES = ("pdflatex", "xelatex", "lualatex")
COMPILE_TIMEOUT_S = 180
_LOG_TAIL_LINES = 40


@tool
def compile_latex(
    project_dir: str,
    main_tex: str = "main.tex",
    engine: str = "auto",
    run_bibtex: bool = True,
    timeout_s: int = COMPILE_TIMEOUT_S,
) -> dict[str, Any]:
    """Compile a LaTeX project directory into a PDF.

    Call this after the LaTeX project has been materialised by
    `fetch_latex_template` and `main.tex` / `references.bib` have been filled in
    with the synthesised paper content.

    Args:
        project_dir: Directory containing the LaTeX project (where main.tex
            lives) — typically the `dest_dir` returned by fetch_latex_template.
        main_tex: Entry .tex filename within project_dir. Default "main.tex".
        engine: "auto" (default), "latexmk", "pdflatex", "xelatex", or
            "lualatex". "auto" uses latexmk if present, otherwise the first
            available pdf engine.
        run_bibtex: If True (default) and a references.bib is present, run a
            BibTeX pass (only relevant for the manual fallback; latexmk handles
            bibliography automatically).
        timeout_s: Per-command timeout in seconds. Default 180.

    Returns:
        {
          "status": "ok" | "error",
          "pdf_path": "/abs/path/to/main.pdf",   # present on ok
          "engine": "latexmk" | "pdflatex" | ...,
          "passes": ["pdflatex", "bibtex", "pdflatex", "pdflatex"],
          "size_bytes": N,
          "warnings": [...],
        }
        On error: {"status": "error", "error": "...", "log_tail": "...", ...}.
    """
    proj = Path(project_dir).expanduser().resolve()
    if not proj.is_dir():
        return {"status": "error", "error": f"project_dir not found: {proj}"}

    tex = proj / main_tex
    if not tex.exists():
        return {"status": "error", "error": f"{main_tex} not found in {proj}"}

    chosen = _choose_engine(engine)
    if chosen is None:
        return {
            "status": "error",
            "error": (
                "no TeX distribution found on PATH. Install one on the host "
                "(MacTeX, TeX Live, or MiKTeX), or use output_format=markdown / "
                "docx instead. Looked for: latexmk, "
                + ", ".join(_PDF_ENGINES)
            ),
        }

    stem = Path(main_tex).stem
    pdf_path = proj / f"{stem}.pdf"
    # Remove a stale PDF so its mere existence cannot mask a failed rebuild.
    if pdf_path.exists():
        try:
            pdf_path.unlink()
        except OSError as e:
            return {"status": "error", "error": f"cannot remove stale PDF {pdf_path}: {e}"}

    warnings: list[str] = []
    passes: list[str] = []

    try:
        if chosen == "latexmk":
            cmd = [
                "latexmk",
                "-pdf",
                "-interaction=nonstopmode",
                "-halt-on-error",
                f"-jobname={stem}",
                main_tex,
            ]
            rc, _out = _run_latex(cmd, cwd=proj, timeout_s=timeout_s)
            passes.append("latexmk")
            if rc != 0:
                warnings.append(f"latexmk exited {rc}; see log_tail if PDF is missing")
        else:
            # Manual sequence: engine -> (bibtex) -> engine -> engine
            base = [chosen, "-interaction=nonstopmode", "-no-shell-escape", main_tex]
            rc, _out = _run_latex(base, cwd=proj, timeout_s=timeout_s)
            passes.append(chosen)

            if run_bibtex and (proj / "references.bib").exists():
                brc, _bout = _run_latex(["bibtex", stem], cwd=proj, timeout_s=timeout_s)
                passes.append("bibtex")
                if brc != 0:
                    warnings.append(f"bibtex exited {brc}; bibliography may be incomplete")

            for _ in range(2):
                rc, _out = _run_latex(base, cwd=proj, timeout_s=timeout_s)
                passes.append(chosen)
            if rc != 0:
                warnings.append(f"{chosen} exited {rc} on final pass; see log_tail if PDF is missing")
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "error": f"compilation timed out after {timeout_s}s",
            "engine": chosen,
            "passes": passes,
            "log_tail": _read_log_tail(proj, stem),
        }
    except FileNotFoundError as e:
        return {"status": "error", "error": f"engine binary missing: {e}", "engine": chosen}

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        return {
            "status": "error",
            "error": f"compilation finished but no PDF was produced at {pdf_path}",
            "engine": chosen,
            "passes": passes,
            "log_tail": _read_log_tail(proj, stem),
            "warnings": warnings,
        }

    return {
        "status": "ok",
        "pdf_path": str(pdf_path),
        "engine": chosen,
        "passes": passes,
        "size_bytes": pdf_path.stat().st_size,
        "warnings": warnings,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _choose_engine(engine: str) -> str | None:
    """Resolve the requested engine to an available binary name, or None."""
    engine = (engine or "auto").strip().lower()
    if engine == "auto":
        if shutil.which("latexmk"):
            return "latexmk"
        for e in _PDF_ENGINES:
            if shutil.which(e):
                return e
        return None
    if engine in ("latexmk", *_PDF_ENGINES):
        return engine if shutil.which(engine) else None
    # Unknown engine name → treat as unavailable.
    return None


def _run_latex(cmd: list[str], cwd: Path, timeout_s: int) -> tuple[int, str]:
    """Run a LaTeX-toolchain command. Returns (returncode, combined_output).

    Raises subprocess.TimeoutExpired on timeout. Patched in tests.
    """
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout_s,
        env={**os.environ, "TEXMFOUTPUT": str(cwd)},
    )
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _read_log_tail(proj: Path, stem: str) -> str:
    """Return the last few lines of the .log for failure triage, if present."""
    log = proj / f"{stem}.log"
    if not log.exists():
        return ""
    try:
        lines = log.read_text(errors="replace").splitlines()
    except OSError:
        return ""
    return "\n".join(lines[-_LOG_TAIL_LINES:])
