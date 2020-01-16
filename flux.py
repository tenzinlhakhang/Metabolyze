import subprocess as sp
import metabolyze as met
import pandas as pd
import sys
import time
results_folder = sys.argv[1]

proc = sp.Popen(['python','flux.output.py',results_folder])

time.sleep(5)

flux_output = pd.read_csv('inputs/flux.output.csv')
flux_output=flux_output.rename(columns = {'Unnamed: 0':'Metabolite'})
standard = pd.read_table('inputs/skeleton_output.tsv')

blanks = standard.filter(regex="_B_")
blanks.index = standard['Metabolite']
blanks[blanks>1] = 0
blanks['Metabolite'] = blanks.index
blanks = blanks.reset_index(drop=True)


project = pd.read_csv('inputs/Groups.tsv',sep='\t')
grouped_samples = {}

for condition in (project.id.unique()):
	test = [x.split('.')[0] for x in project.loc[project['id'] == condition, 'File'].tolist()]
	test = ''.join(test)
	grouped_samples[test] = condition

detection_column_index = standard.columns.get_loc("detections")
standard = pd.read_table('inputs/skeleton_output.tsv')
standard = standard.iloc[:,0:detection_column_index+1]

merged = pd.merge(standard,flux_output,on='Metabolite')

merged_2 = pd.merge(merged,blanks,on='Metabolite')

for x,y in grouped_samples.items():
	merged_2.rename(columns={y: x}, inplace=True)

merged_2['Metabolite'] = merged_2['Metabolite'].str.replace('-13C-0', '')

merged_2.to_csv('inputs/flux_skeleton_output.tsv',sep='\t')


flux_result = met.Analysis(data='flux_skeleton_output.tsv',samplesheet='Groups.csv',blank_threshold_value=0)
flux_result.t_test()



