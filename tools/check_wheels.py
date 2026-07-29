"""Verify every course dependency ships a prebuilt wheel for student machines.

Students install with pip, on machines where they may have no compiler at all. A
dependency without a wheel for their platform does not fail at install time with a
clear message; it tries to build from source and demands Xcode Command Line Tools
on macOS or Build Tools for Visual Studio on Windows. In a room of thirty that is
the difference between a working session and a lost morning.

This checks the platforms the course actually supports, reading the dependency
list from pyproject.toml so it can never drift from what students install.

Run it directly, or let CI run it:

    uv run python tools/check_wheels.py
"""

import json
import re
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

# cp314 because pyproject pins Python 3.14. Apple Silicon and Intel Macs are both
# in the room, and Windows is the institutional default.
PLATFORMS = [
    ("macOS Apple Silicon", re.compile(r"cp314.*macosx.*arm64", re.I)),
    ("macOS Intel", re.compile(r"cp314.*macosx.*x86_64", re.I)),
    ("Windows x64", re.compile(r"cp314.*win_amd64", re.I)),
    ("Linux x64", re.compile(r"cp314.*manylinux.*x86_64", re.I)),
]

PURE_PYTHON = re.compile(r"-(py3|py2\.py3)-none-any\.whl$", re.I)


def course_dependencies(pyproject):
    """Return {name: version} for every pinned runtime dependency."""
    with open(pyproject, "rb") as handle:
        data = tomllib.load(handle)
    pinned = {}
    for spec in data["project"]["dependencies"]:
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)==([^\s;]+)", spec.strip())
        if match:
            pinned[match.group(1)] = match.group(2)
        else:
            print(f"  ? {spec}: not an == pin, so it is not checked here")
    return pinned


def wheel_filenames(name, version):
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    return [entry["filename"] for entry in payload["urls"]]


def main():
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    dependencies = course_dependencies(pyproject)
    print(f"Checking {len(dependencies)} pinned dependencies for prebuilt wheels.\n")

    failures = []
    for name, version in sorted(dependencies.items()):
        try:
            filenames = wheel_filenames(name, version)
        except urllib.error.HTTPError as error:
            failures.append(f"{name}=={version}: PyPI returned {error.code}")
            print(f"  FAIL {name}=={version}: PyPI returned {error.code}")
            continue

        if any(PURE_PYTHON.search(filename) for filename in filenames):
            print(f"  ok   {name}=={version}: pure Python, runs anywhere")
            continue

        missing = []
        for label, pattern in PLATFORMS:
            if not any(pattern.search(filename) for filename in filenames):
                missing.append(label)

        if missing:
            failures.append(f"{name}=={version}: no wheel for {', '.join(missing)}")
            print(f"  FAIL {name}=={version}: no wheel for {', '.join(missing)}")
        else:
            print(f"  ok   {name}=={version}: wheels for every supported platform")

    if failures:
        print(f"\n{len(failures)} dependency problem(s). A student without a compiler "
              f"cannot install this:\n")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"\nAll {len(dependencies)} dependencies install without a compiler.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
