import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

skeleton = sys.argv[1]
groups = sys.argv[2]

def plot(group_column):
    
    
    sns.set(rc={'figure.figsize':(18,5)})
    
    title = group_column.replace('_',' ')
    plt.figure()
    ax = sns.barplot(x=group_column, y="Metabolite", data=cv,palette='hls')
    ax.set_title(title)
    plt.savefig('plot/plot.'+group_column+'.png')
    
if __name__ == "__main__":
    
    groups = pd.read_csv(groups,sep='\t')
    cv = pd.read_csv(skeleton,sep='\t')
    if not os.path.exists('plot'):
    	os.makedirs('plot')
    for column in cv.columns:
        if column.endswith('CV'):
            plot(column)
