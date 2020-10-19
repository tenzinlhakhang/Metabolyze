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

## Demo Example

|File |	 id |  Group |
|--- | --- | --- |
| S02011 | Sample_1 | Control |
| S02012 | Sample_2 | Control |
| S02013 | Sample_3 | Treatment |
| S02014 | Sample_4 | Treatment |
| S02015 | Blank_1 | Blank |
| S02016 | Blank_2 | Blank |
| S02017 | Blank_3 | Blank |
| S02018 | Blank_4 | Blank |



Then run the metabolyze.py script in the directory along with the Groups.tsv file and the skeleton_hybrid_output.tsv file.

```
$ python metabolyze.py

```

## Pairwise Analysis
For doing pairwise analyses to adjust for a covariate effect in the model, DESeq2 is utilized.
To perform this test only one additional column is needed in the Groups.csv file, see below.

## Pairwise Groups.csv Demo Example 

| File |	 id |  Group |  Covariate| 
| --- | --- | --- | ---| 
|S02011 | Sample_1 | Control | Patient_1 |
|S02012 | Sample_2 | Treatment | Patient_1 |
| S02013 | Sample_3 | Control | Patient_2 |
| S02014 | Sample_4 | Treatment | Patient_2 |
| S02015 | Blank_1 | Blank | NA |
| S02016 | Blank_2 | Blank | NA |
| S02017 | Blank_3 | Blank | NA |
| S02018 | Blank_4 | Blank | NA |


Then run the pairwise.metabolyze.R like below, pointing to the Intensity.corrected.values.csv file of interest.
Running the script below will create a Paired-DME-results-40-Samples directory with the results inside.

```
$ Rscript scripts/pairwise.metabolyze.R DME-results-40-Samples/Tables/Intensity.corrected.values.csv

```

## Flux Analysis

In order to perform the flux analysis you can run the following script below, this will generate the flux analysis output as
flux.output.csv in the associated Tables directory where the Intensity.values.detected.csv file was located .

```
python scripts/flux.py DME-results-40-Samples/Tables/Intensity.corrected.values.csv
```

## Normalized Analysis Pipeline

To run the a median and sum normalized analysis of the input data, run the following command.
```
python normalize.py
```



