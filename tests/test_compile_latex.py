"""Tests for compile_latex — mocks the TeX toolchain to stay offline/hermetic.

A single real-compilation test runs only when a pdflatex binary is actually
present on the host; it is skipped otherwise.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.compile_latex.compile_latex import _run_latex, compile_latex

_MINIMAL_TEX = (
    "\\documentclass{article}\n"
    "\\begin{document}\n"
    "Hello from a hermetic compile test.\n"
    "\\end{document}\n"
)


def _make_project(tmp_path: Path, with_bib: bool = False) -> Path:
    proj = tmp_path / "stage8_paper"
    proj.mkdir(parents=True)
    (proj / "main.tex").write_text(_MINIMAL_TEX)
    if with_bib:
        (proj / "references.bib").write_text("% empty bib\n")
    return proj


def _which_factory(available: set[str]):
    """Return a fake shutil.which that only 'finds' the named binaries."""
    def fake_which(name, *a, **k):
        return f"/usr/bin/{name}" if name in available else None
    return fake_which


def _run_factory(pdf_name: str = "main.pdf", rc: int = 0):
    """Fake _run_latex that drops a non-empty PDF in cwd for engine passes."""
    def fake_run(cmd, cwd, timeout_s):
        if cmd[0] in ("latexmk", "pdflatex", "xelatex", "lualatex"):
            (Path(cwd) / pdf_name).write_bytes(b"%PDF-1.5\n%fake\n")
        return rc, "fake output"
    return fake_run


def test_missing_project_dir():
    r = compile_latex.invoke({"project_dir": "/tmp/_definitely_not_here_xyz"})
    assert r["status"] == "error"
    assert "project_dir not found" in r["error"]


def test_missing_main_tex(tmp_path):
    proj = tmp_path / "empty"
    proj.mkdir()
    r = compile_latex.invoke({"project_dir": str(proj)})
    assert r["status"] == "error"
    assert "main.tex not found" in r["error"]


def test_no_tex_distribution(tmp_path):
    proj = _make_project(tmp_path)
    with patch("tools.compile_latex.compile_latex.shutil.which", _which_factory(set())):
        r = compile_latex.invoke({"project_dir": str(proj)})
    assert r["status"] == "error"
    assert "no TeX distribution" in r["error"]


def test_latexmk_success(tmp_path):
    proj = _make_project(tmp_path)
    with patch("tools.compile_latex.compile_latex.shutil.which", _which_factory({"latexmk", "pdflatex"})), \
         patch("tools.compile_latex.compile_latex._run_latex", side_effect=_run_factory()):
        r = compile_latex.invoke({"project_dir": str(proj)})
    assert r["status"] == "ok"
    assert r["engine"] == "latexmk"
    assert r["passes"] == ["latexmk"]
    assert r["pdf_path"] == str(proj / "main.pdf")
    assert r["size_bytes"] > 0


def test_manual_fallback_runs_bibtex(tmp_path):
    proj = _make_project(tmp_path, with_bib=True)
    calls = []

    def recording_run(cmd, cwd, timeout_s):
        calls.append(cmd[0])
        if cmd[0] in ("pdflatex",):
            (Path(cwd) / "main.pdf").write_bytes(b"%PDF-1.5\n")
        return 0, ""

    # latexmk absent → falls back to pdflatex; references.bib present → bibtex runs
    with patch("tools.compile_latex.compile_latex.shutil.which", _which_factory({"pdflatex"})), \
         patch("tools.compile_latex.compile_latex._run_latex", side_effect=recording_run):
        r = compile_latex.invoke({"project_dir": str(proj)})
    assert r["status"] == "ok"
    assert r["engine"] == "pdflatex"
    assert calls == ["pdflatex", "bibtex", "pdflatex", "pdflatex"]


def test_no_pdf_produced_is_error(tmp_path):
    proj = _make_project(tmp_path)
    (proj / "main.log").write_text("! LaTeX Error: something broke\n" * 3)

    def run_no_pdf(cmd, cwd, timeout_s):
        return 1, "error output"  # never writes a PDF

    with patch("tools.compile_latex.compile_latex.shutil.which", _which_factory({"pdflatex"})), \
         patch("tools.compile_latex.compile_latex._run_latex", side_effect=run_no_pdf):
        r = compile_latex.invoke({"project_dir": str(proj)})
    assert r["status"] == "error"
    assert "no PDF was produced" in r["error"]
    assert "LaTeX Error" in r["log_tail"]


def test_unknown_engine_rejected(tmp_path):
    proj = _make_project(tmp_path)
    with patch("tools.compile_latex.compile_latex.shutil.which", _which_factory({"pdflatex"})):
        r = compile_latex.invoke({"project_dir": str(proj), "engine": "wordperfect"})
    assert r["status"] == "error"
    assert "no TeX distribution" in r["error"]


@pytest.mark.skipif(
    not (shutil.which("pdflatex") or shutil.which("latexmk")),
    reason="no real TeX distribution on host",
)
def test_real_compile_smoke(tmp_path):
    """End-to-end: actually compile a minimal document if TeX is installed."""
    proj = _make_project(tmp_path)
    r = compile_latex.invoke({"project_dir": str(proj), "run_bibtex": False})
    assert r["status"] == "ok", r
    assert Path(r["pdf_path"]).exists()
    assert Path(r["pdf_path"]).read_bytes().startswith(b"%PDF")
