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
3. Unzip somewhere convenient.
4. Open the notebooks in Jupyter — either locally (recommended) or by uploading to [Google Colab](https://colab.research.google.com) (backstop for restricted-machine students).

## Local install (recommended)

Before the course starts:

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download). These bundle Python and Jupyter together and install in your user folder — no admin rights needed.
2. After install, open a terminal and run:
   ```
   jupyter notebook
   ```
3. Jupyter should open in your browser. Navigate to the unzipped course folder and open the Day 1 notebook.

A full environment specification (`environment.yml`) and a pip-fallback (`requirements.txt`) ship inside the release zip.

## Backup: Google Colab

If your machine is locked down and a local install isn't possible:

1. Go to https://colab.research.google.com.
2. Choose **File → Upload notebook** and upload the Day 1 notebook from the release zip.
3. Upload the corpus and dictionary files from the zip when prompted by the notebook.

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
