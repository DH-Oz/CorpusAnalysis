"""Assemble the student release zip.

What students download. Everything the course needs sits in one folder, which is
what README.md tells them to expect after unzipping.

The notebooks travel **with their outputs**, because they are the answer keys.
Students type along into a notebook they make themselves and use these to catch up,
or to stop typing and still follow the session.

The manifest is an allowlist rather than a list of exclusions. A denylist quietly
ships whatever nobody thought to exclude, and the thing that would be shipped by
accident here is a licensed dictionary.

    uv run python tools/build_release.py --version v2026.1 --out dist
"""

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

# Individual files, each one required. A missing entry stops the build rather than
# producing a bundle that is quietly short of something.
REQUIRED_FILES = [
    "README.md",
    "corpus_tools.py",
    "environment.yml",
    "requirements.txt",
    "resources.zip",
    "start-jupyter.bat",
    "start-jupyter.sh",
]

# Whole directories, taken as they are.
REQUIRED_DIRECTORIES = ["dictionaries", "nietzsche"]

# The five code-along notebooks.
NOTEBOOK_GLOB = "[0-9]*.ipynb"

# Never redistributed, in any language. See .notes/feedback_liwc-dictionary-handling.md.
# LIWC reaches students inside the password-protected resources.zip instead.
LICENSED_PATTERNS = ["liwc*.dic", "LIWC*.dic"]


class LicensedFileFound(Exception):
    """A commercial dictionary reached the finished bundle."""


def is_licensed(name):
    return any(fnmatch.fnmatch(name, pattern) for pattern in LICENSED_PATTERNS)


def verify(target):
    """Read the finished zip back and refuse it if a licensed dictionary is inside.

    This is the gate, deliberately placed after the writing rather than before it.
    Filtering during collection is easy to get wrong, and a filter that silently
    stops matching fails open: the bundle still builds, still uploads, and the
    dictionary is public. Reading the artefact back cannot fail that way.
    """
    with zipfile.ZipFile(target) as archive:
        offenders = [name for name in archive.namelist()
                     if is_licensed(Path(name).name)]
    if offenders:
        raise LicensedFileFound(
            f"{target} contains {offenders}, which are licensed and must never ship "
            "loose. LIWC reaches students inside resources.zip, behind its password.")
    return target


def collect(root):
    """Return [(source path, name inside the bundle)], or raise before shipping.

    Both instructors keep `dictionaries/liwcdict.dic` unpacked, because notebook 2
    needs it to run. It is skipped here rather than treated as an error, so that a
    build works on the machines that actually have it.
    """
    root = Path(root)
    entries = []

    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            raise FileNotFoundError(f"{path} is missing, so the bundle would be incomplete")
        entries.append((path, name))

    notebooks = sorted(root.glob(NOTEBOOK_GLOB))
    if not notebooks:
        raise FileNotFoundError(f"no notebooks matched {NOTEBOOK_GLOB} in {root}")
    for path in notebooks:
        entries.append((path, path.name))

    for name in REQUIRED_DIRECTORIES:
        directory = root / name
        if not directory.is_dir():
            raise FileNotFoundError(f"{directory} is missing, so the bundle would be incomplete")
        for path in sorted(directory.rglob("*")):
            if path.is_file() and not is_licensed(path.name):
                entries.append((path, str(path.relative_to(root)).replace("\\", "/")))

    return entries


def skipped_licensed(root):
    """Licensed files present on this machine that the bundle leaves behind."""
    root = Path(root)
    found = []
    for name in REQUIRED_DIRECTORIES:
        directory = root / name
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            if path.is_file() and is_licensed(path.name):
                found.append(path.relative_to(root))
    return found


def build(root, target, folder_name):
    """Write the bundle to `target`, with everything under one folder."""
    entries = collect(root)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, arcname in entries:
            # ZipFile.write carries the file mode through, so start-jupyter.sh
            # arrives executable. Students are taught `sh start-jupyter.sh`, which
            # does not need the bit, but anyone running ./start-jupyter.sh on Linux
            # does, and a mode lost here would be invisible until they tried.
            archive.write(path, f"{folder_name}/{arcname}")
    return verify(target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="dev",
                        help="Release tag, e.g. v2026.1. Names the zip and its folder.")
    parser.add_argument("--out", default="dist", help="Directory to write the zip into.")
    arguments = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    folder_name = f"corpus-analysis-{arguments.version}"
    target = Path(arguments.out) / f"{folder_name}.zip"

    for path in skipped_licensed(root):
        print(f"  leaving behind {path}, which is licensed and travels in resources.zip")

    try:
        written = build(root, target, folder_name)
    except LicensedFileFound as failure:
        print(f"REFUSED: {failure}")
        return 2
    except FileNotFoundError as failure:
        print(f"Cannot build the bundle: {failure}")
        return 1

    with zipfile.ZipFile(written) as archive:
        count = len(archive.namelist())
    size = written.stat().st_size
    print(f"{written}: {count} files, {size / 1_000_000:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
