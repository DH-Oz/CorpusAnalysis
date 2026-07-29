# 3. The release bundle is an allowlist, checked after it is written

Date: 2026-07-29
Status: Accepted

## Context

Students receive a release zip, and building it had been a manual step. The repo
holds a good deal that must not travel: the 2025 source materials, the per-session
2025 slide PDFs, the day-N internal notebooks, `CLAUDE.md`, the tooling, and above
all a licensed LIWC dictionary.

That last one is the whole problem. `dictionaries/liwcdict.dic` is gitignored, so a
bundle built from a clean CI checkout cannot contain it. But both instructors keep
it unpacked on their own machines, because notebook 2 needs it to run, so a bundle
built locally is exactly where it would slip through.

## Decision

**`tools/build_release.py` assembles the bundle from an allowlist**, naming each
file and directory that travels. A denylist ships whatever nobody thought to
exclude, and here the thing shipped by accident would be somebody's commercial
product.

**A licensed dictionary found on the build machine is skipped and announced, not
treated as an error.** Refusing would mean the build never runs on either
instructor's machine, which makes the tool useless and pushes people back to
assembling the zip by hand.

**The gate is placed after the writing.** `verify()` reads the finished zip back and
refuses to publish if anything matching `liwc*.dic` is inside. A filter that runs
before the write cannot do this job, because a filter that quietly stops matching
fails open: the bundle still builds, still uploads, and the dictionary is public.
Reading the artefact back cannot fail that way.

The workflow then greps the zip once more, from outside that code, so a bug in the
builder's own gate cannot pass unnoticed.

**Tagging is the trigger.** `.github/workflows/release.yml` fires on a `v*` tag,
runs the tests and the notebook checks, builds the bundle and attaches it, creating
the release first if the tag arrived from a terminal rather than a drafted release.

## Consequences

The bundle is about 6.5 MB and 30 files: the five notebooks with their outputs (ADR
1), `corpus_tools.py`, our three dictionaries, the fifteen Nietzsche texts,
`resources.zip`, `environment.yml`, `requirements.txt`, both launchers, and
`README.md`.

`start-jupyter.command` keeps its executable bit through the zip, which is what a
macOS student double-clicks. Losing it would break the intended path in with no
other symptom, so it has a test of its own.

`pyproject.toml` does not travel. Nothing student-facing references it; the README's
terminal route and both launchers use `environment.yml`, which pip-installs
`-r requirements.txt`, so both of those do travel.

A new student-facing file must be added to the allowlist or it will not ship, and a
missing entry stops the build rather than producing a bundle that is quietly short
of something.

Related: `.notes/feedback_liwc-dictionary-handling.md` for why LIWC is treated this
way, and `.notes/feedback_no-git-for-students.md` for why distribution is a zip.
