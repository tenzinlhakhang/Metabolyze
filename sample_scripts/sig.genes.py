###Metabolomics
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import os
import sys
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

directory = sys.argv[1]

sig_genes = {}
for root, dirs, files in os.walk(os.path.abspath(directory)):
    for file in files:
        if file.endswith('corrected.csv'):
            #print(root,file)
            file_name = (root,file)            
            file_name = ('/'.join(file_name))
            print(file_name)
            result = pd.read_csv(file_name)
            
            result_sig_genes = result.loc[result['ttest_pval'] < 0.05]['Metabolite']
            result_num_sig_genes = len(result_sig_genes)
            
            comparison_name = file_name.split('/')[-1]
            sig_genes[comparison_name] = result_num_sig_genes
sig_df = pd.DataFrame(list(sig_genes.items()),columns=['Comparison','Significant Metabolite'])
sig_df.columns = ['Comparison','Significant Metabolite']


sig_df = sig_df.sort_values('Significant Metabolite',ascending=False)

sns.set(rc={'figure.figsize':(14,8.27)})
sns.set_color_codes("pastel")
figure = sns.barplot(x="Significant Metabolite", y="Comparison", data=sig_df,
            label="Total", color="b")
plt.title('Significant Metabolite vs Comparison')
plt.tight_layout()
plt.savefig(directory+"/dme.sig.png")



