"""Tests for tools/build_release.py.

Run via: `uv run pytest tools/test_build_release.py -q`

Two of these matter more than the rest. The bundle must never carry a licensed
dictionary, and `start-jupyter.command` must come out of the zip still executable,
because a macOS student who cannot double-click it has no way into the course.
"""

from __future__ import annotations

import stat
import zipfile
from pathlib import Path

import pytest

from tools.build_release import LicensedFileFound, build, collect, verify


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A stand-in repo carrying one of everything the real one has."""
    for name in ("README.md", "corpus_tools.py", "environment.yml", "requirements.txt",
                 "resources.zip", "start-jupyter.bat"):
        (tmp_path / name).write_text(f"{name} contents\n", encoding="utf-8")
    launcher = tmp_path / "start-jupyter.command"
    launcher.write_text("#!/bin/sh\necho hi\n", encoding="utf-8")
    launcher.chmod(0o755)

    for name in ("0-setup-check.ipynb", "1-sotu-first-look.ipynb"):
        (tmp_path / name).write_text('{"cells": [], "metadata": {}, '
                                     '"nbformat": 4, "nbformat_minor": 5}\n', encoding="utf-8")

    (tmp_path / "dictionaries").mkdir()
    for name in ("macdvirtue.dic", "nietzsche.dic", "nuke.dic"):
        (tmp_path / "dictionaries" / name).write_text("%\n1\tThing\n%\n", encoding="utf-8")
    (tmp_path / "nietzsche").mkdir()
    (tmp_path / "nietzsche" / "1885 Z.txt").write_text("Also sprach\n", encoding="utf-8")

    # Instructor-side material that must not travel.
    (tmp_path / "CLAUDE.md").write_text("instructions\n", encoding="utf-8")
    (tmp_path / "slide-figures.ipynb").write_text("{}\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (tmp_path / "tools").mkdir()
    (tmp_path / "tools" / "build_release.py").write_text("x\n", encoding="utf-8")
    (tmp_path / "2025-slides").mkdir()
    (tmp_path / "2025-slides" / "D1-AM.pdf").write_text("pdf\n", encoding="utf-8")
    return tmp_path


def arcnames(repo: Path) -> set[str]:
    return {arc for _, arc in collect(repo)}


def test_the_student_facing_files_are_all_there(repo: Path):
    names = arcnames(repo)
    for expected in ("README.md", "corpus_tools.py", "environment.yml", "requirements.txt",
                     "resources.zip", "start-jupyter.bat", "start-jupyter.command",
                     "0-setup-check.ipynb", "1-sotu-first-look.ipynb",
                     "dictionaries/nuke.dic", "nietzsche/1885 Z.txt"):
        assert expected in names, expected


def test_instructor_material_does_not_travel(repo: Path):
    names = arcnames(repo)
    for forbidden in ("CLAUDE.md", "slide-figures.ipynb", "pyproject.toml",
                      "tools/build_release.py", "2025-slides/D1-AM.pdf"):
        assert forbidden not in names, forbidden


def test_a_build_works_on_a_machine_that_has_the_licensed_dictionary(repo: Path, tmp_path: Path):
    """Both instructors keep it unpacked, because notebook 2 needs it to run."""
    (repo / "dictionaries" / "liwcdict.dic").write_text("%\n1\tAffect\n%\n", encoding="utf-8")
    target = build(repo, tmp_path / "out.zip", "corpus-analysis-v2026.1")
    with zipfile.ZipFile(target) as archive:
        names = archive.namelist()
    assert not any("liwcdict" in name for name in names)
    assert "corpus-analysis-v2026.1/dictionaries/nuke.dic" in names


def test_a_licensed_dictionary_in_any_language_is_left_behind(repo: Path, tmp_path: Path):
    (repo / "dictionaries" / "liwc_german.dic").write_text("%\n", encoding="utf-8")
    (repo / "dictionaries" / "LIWC2015.dic").write_text("%\n", encoding="utf-8")
    target = build(repo, tmp_path / "out.zip", "bundle")
    with zipfile.ZipFile(target) as archive:
        names = " ".join(archive.namelist())
    assert "liwc_german" not in names
    assert "LIWC2015" not in names


def test_the_gate_refuses_a_bundle_that_somehow_contains_one(tmp_path: Path):
    """The check reads the finished artefact, so a broken filter cannot fail open."""
    target = tmp_path / "bad.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("bundle/dictionaries/liwcdict.dic", "%\n1\tAffect\n%\n")
    with pytest.raises(LicensedFileFound):
        verify(target)


def test_the_gate_passes_a_clean_bundle(tmp_path: Path):
    target = tmp_path / "good.zip"
    with zipfile.ZipFile(target, "w") as archive:
        archive.writestr("bundle/dictionaries/nuke.dic", "%\n1\tnuke\n%\n")
    assert verify(target) == target


def test_the_mac_launcher_is_still_executable_after_unzipping(repo: Path, tmp_path: Path):
    target = build(repo, tmp_path / "out.zip", "corpus-analysis-v2026.1")
    with zipfile.ZipFile(target) as archive:
        info = archive.getinfo("corpus-analysis-v2026.1/start-jupyter.command")
        mode = info.external_attr >> 16
    assert mode & stat.S_IXUSR, f"lost the executable bit, mode was {mode:o}"


def test_everything_sits_inside_one_folder(repo: Path, tmp_path: Path):
    target = build(repo, tmp_path / "out.zip", "corpus-analysis-v2026.1")
    with zipfile.ZipFile(target) as archive:
        tops = {name.split("/")[0] for name in archive.namelist()}
    assert tops == {"corpus-analysis-v2026.1"}


def test_a_missing_required_file_stops_the_build(repo: Path):
    (repo / "corpus_tools.py").unlink()
    with pytest.raises(FileNotFoundError):
        collect(repo)


def test_no_notebooks_at_all_stops_the_build(repo: Path):
    for path in repo.glob("[0-9]*.ipynb"):
        path.unlink()
    with pytest.raises(FileNotFoundError):
        collect(repo)
