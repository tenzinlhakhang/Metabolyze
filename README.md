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
S02011 | Control | Sample_1
S02012 | Control | Sample_2
S02013 | Treatment | Sample_3
S02014 | Treatment | Sample_4
S02015 | Blank | Blank_1
S02016 | Blank | Blank_2
S02017 | Blank | Blank_3
S02018 | Blank | Blank_4


Then run the metabolyze.py script in the directory along with the Groups.tsv file and the skeleton_hybrid_output.tsv file.

```
$ python metabolyze.py

```

## Pairwise Analysis
For doing pairwise analyses to adjust for a covariate effect in the model, DESeq2 is utilized.
To perform this test only one additional column is needed in the Groups.csv file, see below.

## Pairwise Groups.csv Example 

File | Group | Patient| id | 
--- | --- | --- | --- |
S02011 | Control | Patient_1 | Sample_1
S02012 | Treatment | Patient_1 | Sample_2
S02013 | Control | Patient_2 | Sample_3
S02014 | Treatment | Patient_2 | Sample_4
S02015 | Blank | NA | Blank_1
S02016 | Blank | NA | Blank_2
S02017 | Blank | NA | Blank_3
S02018 | Blank | NA | Blank_4

Then run the pairwise.metabolyze.R like below, pointing to the Intensity.detected.values.csv file of interest.
Running the script below will create a Paired-DME-results-40-Samples directory with the results inside.

```
$ Rscript pairwise.metabolyze.R DME-results-40-Samples/Tables/Intensity.detected.values.csv

```

## Flux Analysis

In order to perform the flux analysis you can run the following script below, this will generate the flux analysis output as
flux.output.csv in the associated Tables directory where the Intensity.values.detected.csv file was located.

```
python flux.py DME-results-40-Samples/Tables/Intensity.detected.values.csv
```



