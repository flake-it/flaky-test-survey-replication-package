======================================================================
Surveying the Developer Experience of Flaky Tests: Replication Package
======================================================================

Contents
========

- ``thematic/`` Records of our collaborative thematic analysis of the open-ended survey questions and the StackOverflow threads.
- ``info.pdf`` The Participant Information Sheet.
- ``analysis.py`` Our Python script for performing our numerical analysis of the closed-ended survey questions.
- ``responses.tsv`` Our complete survey response data in tab-separated-values format. First row is the questions.

Usage
=====

Our Python script can be executed with ``python analysis.py``, producing the following output:

- ``table-data/`` LaTeX sources for the tables in the paper.

    - ``impacts.tex`` Top third of Table 2.
    - ``causes.tex`` Middle third of Table 2.
    - ``actions.tex`` Bottom third of Table 2.

- ``figures-data/`` LaTeX sources for the figures in the paper.

    - ``how_often.tex`` Top bar of Figure 1.
    - ``experience.tex`` Bottom bar of Figure 1.
    - ``actions.tex`` Unused in the paper.
