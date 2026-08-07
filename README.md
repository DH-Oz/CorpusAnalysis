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

1. Go to the course site: https://dh-oz.github.io/CorpusAnalysis/
2. Click **Download the course folder**. That link always fetches the current zip, so it stays right between years.
3. Unzip it somewhere you can find again, such as your Desktop. Everything the course needs sits inside that one folder.
4. Start it as described below: Windows double-clicks, macOS and Linux use a terminal. If your machine is locked down and none of that is possible, use [Google Colab](https://colab.research.google.com) instead.

Do not download the repository itself from GitHub's green **Code** button. That gives you the working repo rather than the course folder, without the notebook outputs you need as answer keys.

## Starting the course

Do this once before the course starts, so that a slow download does not eat into the first session.

Inside the unzipped folder there is a launcher for your machine. Windows starts it with a double-click. macOS needs two typed lines instead, for the reason below.

### Windows

Double-click `start-jupyter.bat`. A black window opens and tells you what it is doing.

### macOS

Do not double-click the launcher. macOS refuses to run programs that arrived from the internet, and you get a box saying Apple cannot check the file for malicious software, offering only **Delete** and **Close**. If you have already seen it, click **Close**. Never click **Delete**, because that throws the launcher away.

Starting it from the Terminal sidesteps that entirely. There is nothing to unlock and no password to find.

1. Open the **Terminal** app. It lives in Applications, then Utilities. A window opens with a blinking cursor.
2. Type `cd` followed by a space. Do not press Return yet.
3. Find the unzipped course folder in Finder and drag it onto the Terminal window. Terminal fills in where the folder lives, so you never type a path. Now press Return.
4. Type the following and press Return:

   ```
   sh start-jupyter.sh
   ```

You run those two lines every time you start the course, so keep the Terminal window handy.

### Linux

Open a terminal, `cd` to the unzipped folder, and run `sh start-jupyter.sh`.

### Once it starts

The first run takes several minutes, because it builds the course environment. Every run after that takes a few seconds.

When JupyterLab opens in your browser, open `0-setup-check.ipynb` and run every cell. The first cell is slow the first time, sometimes for half a minute, while Python caches the libraries as it loads them. If every cell runs without an error, you are ready.

Leave that window open while you work, whether it is the black window Windows opened or the Terminal you typed into. Closing it stops Jupyter.

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

If your machine will not let you install anything, the course runs in a browser
instead. You need a Google account and the course zip.

Put the folder in Google Drive rather than uploading it to Colab directly. Files
uploaded straight into Colab are thrown away when it disconnects, which over four days
means uploading everything again every morning. In Drive it stays put.

**Once, at the start:**

1. Unzip the course zip on whatever machine you can, even a phone or a library
   computer. You want the folder, not the zip.
2. Go to https://drive.google.com and drag the whole unzipped folder into the window.
   Wait for it to finish uploading.
3. Go to https://colab.research.google.com, choose **File → Open notebook**, then the
   **Google Drive** tab, and open `0-setup-check.ipynb` from the folder you uploaded.

**Then, at the start of every session:**

4. Run this in the first cell to reach your files, and click through the permission
   prompt it shows:

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   %cd /content/drive/MyDrive/corpus-analysis-v2026.1
   ```

   Change the last line if you renamed the folder or put it somewhere else in Drive.

5. Install the course libraries, which Colab does not have:

   ```python
   !pip install -r requirements.txt
   ```

   This takes a couple of minutes. **Colab will then ask you to restart the session,
   and you should say yes.** It is replacing versions of numpy and pandas that were
   already loaded, and the new ones are only picked up after a restart. After
   restarting, run step 4 again, but not step 5.

6. Run the rest of `0-setup-check.ipynb`. If every cell runs without an error, you are
   ready.

Your work saves back into Drive, so it is still there next session.

Two things behave differently from a local install. Anything you save goes to the
Drive folder rather than your own disk, and the LIWC lesson on day 3 needs a
dictionary you supply yourself, which you upload into the same folder. Bring either
problem to us rather than fighting it alone.

## Licences

- **Lesson content** (notebooks, slides, prose, custom dictionaries) — [CC BY-NC 4.0](LICENSE-CONTENT.md).
- **Code** (Python sources, scripts, workflows) — [MIT](LICENSE-CODE.md).

LIWC dictionaries are commercial and are **not** distributed in this repository. If you have a LIWC licence and want to use it with the German content analysis lesson, contact the instructors.

## Contact

Mark Alfano — mark.alfano@gmail.com
Brian Ballsun-Stanton — brian.ballsun-stanton@mq.edu.au

## Historical archive

The 2025 edition of this course was taught in R using R Markdown. Those source materials are archived at https://github.com/DH-Oz/2025-corpus-analysis.
