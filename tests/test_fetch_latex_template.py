"""Tests for fetch_latex_template — runs against the vendored templates dir.

No network or git is involved; the tool copies from tools/fetch_latex_template/
templates/<venue>/, so these tests exercise the real bundled files.
"""

from __future__ import annotations

import pytest

from tools.fetch_latex_template.fetch_latex_template import (
    VALID_VENUES,
    _TEMPLATES_DIR,
    fetch_latex_template,
)


def test_invalid_venue():
    r = fetch_latex_template.invoke({"venue": "icml2026", "dest_dir": "/tmp/_x"})
    assert r["status"] == "error"
    assert "venue must be one of" in r["error"]


def test_templates_are_vendored():
    """The two supported venues must actually ship in the repo."""
    for v in VALID_VENUES:
        assert (_TEMPLATES_DIR / v / "main.tex").exists(), f"{v} template missing"


@pytest.mark.parametrize("venue", VALID_VENUES)
def test_success_path(tmp_path, venue):
    dest = tmp_path / "project_workspace" / "stage8_paper"
    result = fetch_latex_template.invoke({"venue": venue, "dest_dir": str(dest)})

    assert result["status"] == "ok"
    assert result["venue"] == venue
    assert result["main_tex_path"] == str(dest / "main.tex")
    assert (dest / "main.tex").exists()
    assert (dest / "references.bib").exists()
    assert (dest / "figures").is_dir()

    # Reference-only files must not be copied into the paper project.
    assert not (dest / "README.md").exists()
    assert not (dest / "official_template.tex").exists()


def test_iclr_ships_conference_style(tmp_path):
    dest = tmp_path / "iclr"
    result = fetch_latex_template.invoke({"venue": "iclr2026", "dest_dir": str(dest)})
    assert result["status"] == "ok"
    assert (dest / "iclr2026_conference.sty").exists()


def test_neurips_ships_conference_style(tmp_path):
    dest = tmp_path / "neurips"
    result = fetch_latex_template.invoke({"venue": "neurips2026", "dest_dir": str(dest)})
    assert result["status"] == "ok"
    assert (dest / "neurips_2026.sty").exists()


def test_dest_created_if_missing(tmp_path):
    dest = tmp_path / "a" / "b" / "c" / "stage8_paper"
    result = fetch_latex_template.invoke({"venue": "iclr2026", "dest_dir": str(dest)})
    assert result["status"] == "ok"
    assert dest.is_dir()
