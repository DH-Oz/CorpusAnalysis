# DH-Oz Corpus Analysis Masterclass

A four-day, eight-session introduction to computational corpus analysis for the humanities, taught in Python with Jupyter notebooks. Co-delivered by Mark Alfano and Brian Ballsun-Stanton as part of the Digital Humanities Winter School.

## What this course covers

Across eight 2-hour sessions you will:

- Install Python, Jupyter, and the working environment.
- Read a corpus, count words, and build your first word cloud.
- Cluster documents and explore similarity with hierarchical clustering.
- Build document-feature matrices and use matrix multiplication to surface relationships.
- Detect collocations and visualise them as networks.
- Apply content-analysis dictionaries — including running an analysis in German.
- Build your own custom dictionary for a research question of your choice.
- Find and assemble new corpora, including with AI assistance.

The course assumes **no prior Python experience**. Python concepts (loops, conditionals, functions) are introduced exactly when a corpus task needs them.

## Getting the materials

Materials are distributed as a **release zip** — no git knowledge required.

1. Visit the course site: https://DH-Oz.github.io/CorpusAnalysis (live after first deploy).
2. Download the latest **release zip** linked from the landing page.
3. Unzip it somewhere convenient. Everything the course needs sits inside that one folder.
4. Start the course by double-clicking one file, as below. If your machine is locked down and that is not possible, use [Google Colab](https://colab.research.google.com) instead.

## Starting the course

Do this once before the course starts, so that a slow download does not eat into the first session.

Inside the unzipped folder there is a file for your machine:

- **Windows**: `start-jupyter.bat`
- **macOS and Linux**: `start-jupyter.command`

Double-click it. A black window opens and tells you what it is doing. The first run takes several minutes, because it builds the course environment. Every run after that takes a few seconds.

When JupyterLab opens in your browser, open `0-setup-check.ipynb` and run every cell. The first cell is slow the first time, sometimes for half a minute, while Python caches the libraries as it loads them. If every cell runs without an error, you are ready.

Leave the black window open while you work. Closing it stops Jupyter.

### The first time on a Mac

macOS blocks files that came from the internet until you confirm you meant to open them. If double-clicking does nothing, or you see a warning about an unidentified developer, **right-click** `start-jupyter.command`, choose **Open**, then click **Open** in the dialog. You only do this once.

### If you have no conda yet

The launcher checks whether you already have conda, which is the tool that builds the course environment. If you do not, it offers to install Miniforge and waits for you to answer.

Saying yes downloads about 60 MB and puts everything in one folder inside your home directory. It needs no administrator password, it does not become your system Python, and it leaves your existing setup alone. To remove it later, delete that one folder. Saying no changes nothing at all.

## If you would rather use the terminal

The launcher exists so nobody has to, but the terminal works and some people prefer it.

```
cd path/to/the/unzipped/folder
conda env create -f environment.yml
conda run --no-capture-output -n corpusanalysis jupyter lab
```

The first line is needed once. Note that there is no `conda activate` step: `conda run` does the same job, and it works even when `conda init` has never been run on your machine, which is the usual reason `conda activate` fails.

If the terminal cannot find `conda` at all, use the launcher instead. On Windows the **Anaconda Prompt** from the Start menu also works, since the installer configures it for you.

## Backup: Google Colab

If your machine is locked down and a local install isn't possible:

1. Go to https://colab.research.google.com.
2. Choose **File → Upload notebook** and upload `0-setup-check.ipynb` from the release zip.
3. Upload the supporting files from the zip, including `corpus_tools.py` and the dictionaries.

Some advanced features (e.g. file system access patterns) may need small adjustments in Colab — the notebooks flag these inline.

## Licences

- **Lesson content** (notebooks, slides, prose, custom dictionaries) — [CC BY-NC 4.0](LICENSE-CONTENT.md).
- **Code** (Python sources, scripts, workflows) — [MIT](LICENSE-CODE.md).

LIWC dictionaries are commercial and are **not** distributed in this repository. If you have a LIWC licence and want to use it with the German content analysis lesson, contact the instructors.

## Contact

Mark Alfano — mark.alfano@gmail.com
Brian Ballsun-Stanton — brian.ballsun-stanton@mq.edu.au

## Historical archive

The 2025 edition of this course was taught in R using R Markdown. Those source materials are archived at https://github.com/DH-Oz/2025-corpus-analysis.
