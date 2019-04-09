# Metabolyze

An Analysis Pipeline for downstream analysis of Skeleton Hybrid Output

## Overview

Calculation of:
T-test, LFC, and Group mean, Pathway Analysis

Generation of: Heatmaps, Volcano Plots, 3-D PCA.

## Installation

Python = Python 3.6.5

R = R 3.5.1

It is suggested to create a virtual environment for the installation step

```
$ git clone https://github.com/NYUMetabolomics/metabolyze.git
```

```
$ pip install -r requirements.txt
```
```
install.packages('manhattanly')
install.packages('pheatmap')
```
## Inputs
1) Create an inputs directory
2) Include a Groups.tsv file that resembles the template below
3) Include a skeleton_output.tsv

## Example

File | Group | id |
--- | --- | --- |
S02011 | Group_1 | Sample_1
S02012 | Group_1 | Sample_2
S02013 | Group_2 | Sample_3
S02014 | Group_2 | Sample_4

Then run the metabolyze.py script in the directory along with the Groups.tsv file and the skeleton_hybrid_output.tsv file.

```
$ python metabolyze.py

```
