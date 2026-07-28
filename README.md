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
4. Set up the environment, either locally with conda (recommended, see below) or in [Google Colab](https://colab.research.google.com) if your machine is locked down.

## Local install (recommended)

Do all of this before the course starts.

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download). Miniconda is the smaller download and is all the course needs. Both install into your user folder, so you do not need admin rights.
2. Open a terminal. On Windows, use the **Anaconda Prompt** that the installer adds to your Start menu. If the terminal cannot find `conda`, jump to *If the terminal cannot find conda* below, then come back here.
3. Change into the unzipped course folder:
   ```
   cd path/to/the/unzipped/folder
   ```
4. Create the course environment. This reads `environment.yml` and installs Python 3.14 along with every library the course uses. It takes several minutes.
   ```
   conda env create -f environment.yml
   ```
5. Activate the environment. You need this line every time you open a new terminal to work on the course.
   ```
   conda activate corpusanalysis
   ```
6. Start Jupyter:
   ```
   jupyter lab
   ```
7. Jupyter opens in your browser showing the course folder. Open `0-setup-check.ipynb` and run every cell. The first cell is slow the first time you run it, sometimes for half a minute, because Python is caching the libraries as it loads them. Later runs take about a second. If every cell runs without an error, your environment is ready.

Step 4 is needed once. On later days you only need steps 2, 3, 5, and 6.

### If the terminal cannot find conda

If step 2 gives you `conda: command not found`, or step 5 gives you an error saying your shell is not configured to use `conda activate`, then conda was installed without setting up your shell. You can run that setup yourself.

On Windows, use the **Anaconda Prompt** from the Start menu. The installer configures it for you, so there is nothing else to do.

On macOS and Linux, check which shell you are using, then run conda's setup for it:

```
echo $SHELL
~/miniconda3/bin/conda init zsh
```

Use `bash` in place of `zsh` if that is what `echo $SHELL` reported. If you installed Anaconda rather than Miniconda, the folder is `~/anaconda3` instead. The full path matters here, because `conda` is not yet on your PATH.

The setup only takes effect once your shell reads its settings again. Rather than closing the window, reload them in place:

```
source ~/.zshrc
```

Use `~/.bash_profile` in place of `~/.zshrc` if `echo $SHELL` reported bash. You will know it worked when your prompt starts with `(base)`. Then carry on from step 3.

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
