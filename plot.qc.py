import pandas as pd
import sys
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os


if not os.path.exists('QC'):
    os.makedirs('QC')

skeleton_name = [x for x in os.listdir('inputs') if x.endswith('output.tsv')][0]

skeleton_input = pd.read_csv('inputs/'+skeleton_name,sep='\t')
groups = pd.read_csv('inputs/Groups.tsv',sep='\t')

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)

ax = sns.distplot(np.array(skeleton_input['detections']), bins=20, kde=False, rug=True);
ax.set_title('Sample Detection Frequency')
ax.set_ylabel('Detection')
ax.set_xlabel('Frequency')
plt.savefig('QC/plot.detection.png',dpi=400)


a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.countplot(y="winner", data=skeleton_input)
ax.set_title('Sample Winner vs. Frequency')
ax.set_ylabel('Sample')
ax.set_xlabel('Count')
plt.savefig('QC/plot.winner.png',dpi=400)


skeleton_input[['ion','polarity']] = skeleton_input['Ion Type'].str.split(']',expand=True)

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)

ax = sns.countplot(y="polarity", data=skeleton_input)
ax.set_title('Polarity Ratio')
ax.set_ylabel('Polarity')
ax.set_xlabel('Count')
plt.savefig('QC/plot.polarity.png',dpi=400)






