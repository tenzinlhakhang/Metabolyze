import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')  
import itertools
import string
#import RNAseq
import numpy as np
import pandas as pd
from scipy import stats
import numpy as np
import sys, json
from time import sleep
from scipy import *
from scipy import stats
from sklearn.decomposition import PCA
import plotly.plotly as py
#%matplotlib inline
import plotly
#plotly.offline.init_notebook_mode() # To embed plots in the output cell of the notebook
import plotly.graph_objs as go
import os
import operator
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from math import sqrt
from itertools import combinations
from matplotlib import rcParams
rcParams['pdf.fonttype'] = 42 ## Output Type 3 (Type3) or Type 42 (TrueType)
rcParams['font.sans-serif'] = 'Arial'
import sys
matrix_path = sys.argv[1]
groups_path = sys.argv[2]
pca_name = sys.argv[3]


COLORS8 = [
'#1F77B4',
'#26A9E0',
'#75DBA7',
'#2CA02C',
'#9467BD',
'#FF0000',
'#FF7F0E',
'#E377C2',
]

COLORS = ['#1F78B4','#E31A1C','#FF7F00','#6A3D9A','#B15928','#666666', 'k']
COLORS10 = [
'#1f77b4',
'#ff7f0e',
'#2ca02c',
'#d62728',
'#9467bd',
'#8c564b',
'#e377c2',
'#7f7f7f',
'#bcbd22',
'#17becf',
]

samplesheet = pd.read_csv(groups_path)
samplesheet = samplesheet.loc[samplesheet['Color'] != 'Blank']
COLORS20 = samplesheet['Color'].tolist()

COLORS20 = sorted(set(COLORS20), key=COLORS20.index)




COLORS20b = [
'#393b79',
'#5254a3',
'#6b6ecf',
'#9c9ede',
'#637939',
'#8ca252',
'#b5cf6b',
'#cedb9c',
'#8c6d31',
'#bd9e39',
'#e7ba52',
'#e7cb94',
'#843c39',
'#ad494a',
'#d6616b',
'#e7969c',
'#7b4173',
'#a55194',
'#ce6dbd',
'#de9ed6',
]



def perform_PCA(fpkmMatrix, standardize=3, log=True):
	## preprocessing of the fpkmMatrix
	if log:
		fpkmMatrix = np.log10(fpkmMatrix + 1.)
	if standardize == 2: # standardize along rows/genes
		fpkmMatrix = stats.zscore(fpkmMatrix, axis=1)
	elif standardize == 1: # standardize along cols/samples
		fpkmMatrix = stats.zscore(fpkmMatrix, axis=0)

	## remove genes with NaNs
	fpkmMatrix = fpkmMatrix[~np.isnan(np.sum(fpkmMatrix, axis=1))]

	pca = PCA(n_components=None)
	## get variance captured
	pca.fit(fpkmMatrix.T)
	variance_explained = pca.explained_variance_ratio_[0:3]
	variance_explained *= 100
	## compute PCA and plot
	pca_transformed = pca.transform(fpkmMatrix.T)
	return variance_explained, pca_transformed



def main_plot():


	# directory = matrix_path.split('/')[0]
	# print(directory)
	expr_df = pd.read_csv(matrix_path)


	expr_df.index = expr_df['Metabolite']
	del expr_df['Metabolite']
	expr_df = expr_df.astype(float)
	


	meta_df = pd.read_csv(groups_path)
	meta_df = meta_df.loc[meta_df['Group'] != 'Blank']
	
	meta_df['File'].str.replace('.mzXML','')
	
	meta_df.index = meta_df['id']
	expr_df = expr_df.reindex(columns=meta_df['id'].tolist())

	variance_explained, pca_transformed = perform_PCA(expr_df.values, standardize=2, log=True)

	print(meta_df)
	meta_df['x'] = pca_transformed[:,0]
	meta_df['y'] = pca_transformed[:,1]
	meta_df['z'] = pca_transformed[:,2]

	conditions = meta_df['Group'].unique().tolist()
	#platforms = meta_df['platform'].unique().tolist()
	SYMBOLS = ['circle']
	COLORS = COLORS20

	data = [] 
	#print(meta_df)

	for (condition), meta_df_sub in meta_df.groupby(['Group']):
	    #print(condition)
	    # Iteratate through samples grouped by condition and platform
	    display_name = '%s' % (condition)
	    # Initiate a Scatter3d instance for each group of samples specifying their coordinates
	    # and displaying attributes including color, shape, size and etc.
	    trace = go.Scatter3d(
	        x=meta_df_sub['x'],
	        y=meta_df_sub['y'],
	        z=meta_df_sub['z'],
	        text=meta_df_sub.index,
	        mode='markers',
	        marker=dict(
	            size=10,
	            color=COLORS[conditions.index(condition)], # Color by infection status
	            opacity=.8,
	        ),
	        name=display_name,
	    )
	    
	    data.append(trace)
	    

	# Configs for layout and axes
	layout=dict(height=1000, width=1200, 
	            title='3D PCA plot',
	            scene=dict(
	                xaxis=dict(title='PC1 (%.2f%% variance)' % variance_explained[0]),
	                yaxis=dict(title='PC2 (%.2f%% variance)' % variance_explained[1]),
	                zaxis=dict(title='PC3 (%.2f%% variance)' % variance_explained[2])
	               )
	)
	fig=dict(data=data, layout=layout)


	plotly.offline.plot(fig, filename=str(pca_name))
	#fig.write_image("images/fig1.pdf")
main_plot()
#plotly.offline.iplot(fig)
