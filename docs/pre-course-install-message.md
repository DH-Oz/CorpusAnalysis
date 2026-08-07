# Pre-course install message for Slack

Written 2026-08-03, to go out to participants ahead of the winter school. Everything
below the first rule is the message itself, ready to paste. Slack converts `**bold**`
and `*italic*` when you paste markdown into the composer.

The winter school runs 25–28 August 2026.

Two choices worth knowing about, in case someone asks:

- **Miniforge rather than Anaconda or Miniconda.** Anaconda Inc. requires a paid
  Business licence for organisations over 200 people, and while accredited
  institutions are exempt for curriculum-based teaching, a participant's own later
  research use sits in the grey area. Since 15 July 2025 a fresh Miniconda install
  also gates Anaconda's repositories behind a command-line terms-acceptance prompt,
  which is one more failure mode for the audience least able to debug it. Miniforge
  draws from conda-forge and raises neither question. Several universities have
  removed Anaconda from their standard builds, so the line telling IT that Miniforge
  is not Anaconda pre-empts an automatic rejection.
- **A manual install is optional.** `start-jupyter.sh` and `start-jupyter.bat`
  install Miniforge themselves when they find no conda, and they also find an
  existing Anaconda or Miniconda, since `environment.yml` names `conda-forge` only.
  The message goes out now anyway, because a locked-down machine needs an IT ticket
  raised weeks ahead, and because a few hundred megabytes should not download over
  conference wifi in session one.

Settled since: conda-forge signs and notarises the macOS `.pkg` with NumFOCUS
certificates, so Gatekeeper does not block it. The step telling people to Control-click
past an unidentified-developer warning has gone, because that warning cannot appear for
this file and the instruction only taught the habit of clicking through one.

Still to confirm in testing: where the `.pkg` lands, since the launcher looks in
`~/miniforge3`, `/opt/miniforge3` and the Homebrew Caskroom path, and whether it asks
for an administrator password.

Note that `start-jupyter.sh` is a different matter and *is* blocked, because we
sign nothing. macOS Sequoia removed the Control-click bypass, and what replaced it
wants an administrator password and expires after an hour, which is the wrong shape
for half this cohort. So `README.md` now starts the Mac launcher from the Terminal
with `cd` and `sh start-jupyter.sh`. Running the script through `sh` means the
file is read rather than launched, so Gatekeeper is never consulted and there is
nothing to unlock. This is the route that worked with the test student.

---

**Corpus analysis stream: one thing to sort out before we start**

This year we work in Python, using Jupyter notebooks, on the laptop you bring with
you. The course materials come out later this week, so there is nothing to download
yet.

What is worth doing now is finding out whether you are able to install software on
that laptop, because if you are not, the answer has to come from your IT service
desk, and that takes days rather than minutes.

**Installing Miniforge**

Miniforge is a small free program that sets Python up for you. Please use Miniforge
rather than Anaconda or Miniconda, because it is the version we have tested the
course against.

*If you use Windows*

1. Click this link, which downloads the installer:
   https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe
2. The file arrives in your Downloads folder, named `Miniforge3-Windows-x86_64.exe`.
3. Double-click that file.
4. Work through the installer, accepting the licence and choosing **Just Me** when it
   asks who to install it for. Leave every other setting the way you find it.
5. It takes a few minutes, and when it finishes there is nothing to open and nothing
   further to do.

*If you use a Mac*

Macs come with two different kinds of processor, and each one needs a different file.
Click the Apple menu at the top left of your screen, then **About This Mac**. If the
window names an Apple chip, whose name begins with M, use the first link below. If it
names Intel, use the second.

1. Apple chip:
   https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.pkg

   Intel:
   https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-x86_64.pkg
2. The file arrives in your Downloads folder, named `Miniforge3-MacOSX-arm64.pkg` or
   `Miniforge3-MacOSX-x86_64.pkg`.
3. Double-click that file. A window titled **Install Miniforge3** opens. Your Mac does
   not warn you about this one, because conda-forge signs it.
4. Work through the installer, accepting the licence and leaving every setting the way
   you find it.
5. It takes a few minutes. When it finishes you can close the window. There is nothing
   to open afterwards, and nothing new appears in your Applications folder, which is
   what we expect rather than a sign it failed.

*If you use Linux*, send us a message here and we will work through it with you.

**Please install nothing else.** You do not need to install Python or Jupyter
separately, because the course folder builds all of that for itself the first time you
open it.

**If your laptop is managed by your university**

Institutional laptops often refuse to install anything at all. Please raise a request
with your IT service desk this week rather than in the week of the course, and forward
them everything below the line. Let us know here as well, so that we can see how many
people are affected before day one.

If the install turns out to be impossible, you can still take the course, because
everything runs in a web browser through Google Colab, and we will give you
instructions for that.

Bring any question to this channel. Sorting this out this week is far easier than
sorting it out at nine in the morning on day one.

**― For the IT service desk ―**

I am attending the Digital Humanities Winter School corpus analysis masterclass on
25–28 August 2026, which teaches Python programming for text analysis, and I need to
be able to run Python and Jupyter notebooks on this laptop.

The request is to install Miniforge, or to allow me to install it myself. It is
published by the conda-forge project at https://conda-forge.org/download/, with the
source at https://github.com/conda-forge/miniforge.

Miniforge is the community-maintained conda distribution. The installer is licensed
BSD 3-Clause, and the packages it installs carry their own open-source licences. It is
not Anaconda, and it does not draw packages from Anaconda's repositories, so
Anaconda's commercial terms of service do not apply to it.

Installed for a single user, it behaves as follows:

- It installs into that user's own folder, at `%USERPROFILE%\miniforge3` on Windows or
  `~/miniforge3` on macOS.
- It needs no administrator rights, and the installer offers a single-user option that
  asks for no password.
- It does not register itself as the system Python, so other software on the machine is
  unaffected.
- Removing it means deleting that one folder.

The download is around 75 MB. The course then downloads its Python packages from
`conda.anaconda.org` and `pypi.org`, so those two addresses need to be reachable
through the firewall.

If the standard build already provides Anaconda or Miniconda under an institutional
licence, that will serve the course equally well.
