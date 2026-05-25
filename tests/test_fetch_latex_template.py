"""Tests for fetch_latex_template — mocks `git` invocations to stay offline."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.fetch_latex_template.fetch_latex_template import (
    _clone_cache,
    fetch_latex_template,
)


@pytest.fixture(autouse=True)
def reset_clone_cache():
    """Fresh clone-cache for every test (otherwise tests bleed into each other)."""
    _clone_cache.clear()
    yield
    _clone_cache.clear()


def _build_fake_clone(root: Path, venues: list[str]) -> None:
    """Materialize a fake paper-templates clone with the given venue dirs."""
    root.mkdir(parents=True, exist_ok=True)
    for v in venues:
        vdir = root / v
        vdir.mkdir()
        (vdir / "main.tex").write_text("\\documentclass{article}\\begin{document}placeholder\\end{document}")
        (vdir / "references.bib").write_text("% empty bib starter\n")
        (vdir / f"{v}_conference.sty").write_text("% fake sty\n")
        (vdir / "README.md").write_text("# venue README - should NOT be copied")
        (vdir / "official_template.tex").write_text("% reference doc - should NOT be copied")
        figs = vdir / "figures"
        figs.mkdir()
        (figs / ".gitkeep").touch()
    # Repo-level files
    (root / "README.md").write_text("# paper-templates")
    (root / "LICENSE").write_text("CC0")


def test_invalid_venue():
    r = fetch_latex_template.invoke({"venue": "icml2026", "dest_dir": "/tmp/_x"})
    assert r["status"] == "error"
    assert "venue must be one of" in r["error"]


def test_success_path(tmp_path):
    fake_clone = tmp_path / "fake_clone"
    _build_fake_clone(fake_clone, ["iclr2026", "neurips2026"])
    dest = tmp_path / "project_workspace" / "stage8_paper"

    # Mock the git invocation: just leave the prepared directory alone
    def fake_git(args, cwd=None):
        if args[0] == "clone":
            # `clone` writes into the last positional arg
            target = Path(args[-1])
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(fake_clone, target)
        return ""

    with patch(
        "tools.fetch_latex_template.fetch_latex_template._run_git",
        side_effect=fake_git,
    ):
        result = fetch_latex_template.invoke({
            "venue": "iclr2026",
            "dest_dir": str(dest),
        })

    assert result["status"] == "ok"
    assert result["venue"] == "iclr2026"
    assert result["main_tex_path"] == str(dest / "main.tex")
    assert (dest / "main.tex").exists()
    assert (dest / "references.bib").exists()
    assert (dest / "iclr2026_conference.sty").exists()
    assert (dest / "figures" / ".gitkeep").exists()

    # The two excluded files should not have been copied
    assert not (dest / "README.md").exists()
    assert not (dest / "official_template.tex").exists()


def test_cache_reuse_with_use_latest_false(tmp_path):
    """Second call with use_latest=False should NOT re-run git."""
    fake_clone = tmp_path / "fake_clone"
    _build_fake_clone(fake_clone, ["iclr2026"])

    dest1 = tmp_path / "p1"
    dest2 = tmp_path / "p2"

    git_calls = []

    def fake_git(args, cwd=None):
        git_calls.append(args[0])
        if args[0] == "clone":
            target = Path(args[-1])
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(fake_clone, target)
        return ""

    with patch(
        "tools.fetch_latex_template.fetch_latex_template._run_git",
        side_effect=fake_git,
    ):
        r1 = fetch_latex_template.invoke({"venue": "iclr2026", "dest_dir": str(dest1)})
        assert r1["status"] == "ok"
        first_calls = list(git_calls)
        assert "clone" in first_calls

        # Second call with use_latest=False — should NOT touch git again
        r2 = fetch_latex_template.invoke({
            "venue": "iclr2026",
            "dest_dir": str(dest2),
            "use_latest": False,
        })
        assert r2["status"] == "ok"
        assert git_calls == first_calls  # no new git invocations

        # Both destinations got the same content
        assert (dest1 / "main.tex").read_text() == (dest2 / "main.tex").read_text()


def test_pull_failure_is_warning_not_error(tmp_path):
    """If git pull fails on the cached clone, fall back to cached snapshot."""
    fake_clone = tmp_path / "fake_clone"
    _build_fake_clone(fake_clone, ["iclr2026"])

    dest1 = tmp_path / "p1"
    dest2 = tmp_path / "p2"
    call_count = [0]

    def fake_git(args, cwd=None):
        call_count[0] += 1
        if args[0] == "clone":
            target = Path(args[-1])
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(fake_clone, target)
            return ""
        if args[0] == "pull":
            raise RuntimeError("network down")
        return ""

    with patch(
        "tools.fetch_latex_template.fetch_latex_template._run_git",
        side_effect=fake_git,
    ):
        r1 = fetch_latex_template.invoke({"venue": "iclr2026", "dest_dir": str(dest1)})
        assert r1["status"] == "ok"

        r2 = fetch_latex_template.invoke({
            "venue": "iclr2026",
            "dest_dir": str(dest2),
            "use_latest": True,
        })
        # Second call should still succeed because cached clone is reused
        assert r2["status"] == "ok"
        assert any("git pull failed" in w for w in r2["warnings"])


def test_missing_venue_in_clone_returns_error(tmp_path):
    fake_clone = tmp_path / "fake_clone"
    _build_fake_clone(fake_clone, ["iclr2026"])  # NO neurips2026
    dest = tmp_path / "out"

    def fake_git(args, cwd=None):
        if args[0] == "clone":
            target = Path(args[-1])
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(fake_clone, target)
        return ""

    with patch(
        "tools.fetch_latex_template.fetch_latex_template._run_git",
        side_effect=fake_git,
    ):
        result = fetch_latex_template.invoke({
            "venue": "neurips2026",
            "dest_dir": str(dest),
        })

    assert result["status"] == "error"
    assert "not found in cloned repo" in result["error"]
    assert "iclr2026" in result["error"]  # tells you what IS available
