# Corpus Analysis Masterclass — code-along notebooks

The four hands-on "type-along" notebooks for the 2026 Python edition.

1. `1-sotu-first-look.ipynb` — State of the Union: word cloud, hierarchical
   clustering, topic models (LDA), comparison clouds.
2. `2-dictionary-content.ipynb` — content-analysis dictionaries (per-document
   category percentages), including a LIWC section.
3. `3a-collocations-dispersion.ipynb` — collocation networks, lexical
   dispersion, keyness.
4. `3b-nietzsche-german-paragraphs.ipynb` — German dictionary analysis, concept
   networks, keyness, moral scatters.

## Setup (once, with internet — then it runs offline)

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
2. Download these files: the green **Code** button above, then **Download ZIP**, then unzip.
3. In a terminal, from the unzipped folder:

       conda create -n corpus python=3.14 -y
       conda activate corpus
       pip install -r requirements.txt

   Conda supplies only Python; every library comes from that one `pip install`,
   so there is no conda/pip cross-talk.
4. Start Jupyter and open a notebook:

       jupyter lab

   Run the cells top to bottom. The first run downloads a few small NLTK data
   files, so do one full run while you still have internet.

## LIWC (notebook 2)

Drop your own `liwcdict.dic` into the `dictionaries/` folder. The licensed file
is not redistributed here, so without it that section skips and the open MAC
dictionary stands in for the same method.
