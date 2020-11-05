import pandas as pd
import sys
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os
import numpy as np


results_folder = sys.argv[1]
class Analysis:
    
    def __init__(self, data,samplesheet,blank_threshold_value,method):
        
        self.data = 'inputs/'+data
        self.samplesheet = 'inputs/'+samplesheet
        self.blank_threshold_value = blank_threshold_value
        self.method = method

    def input_check(self):
        id_dict = self.get_ids('ID')
        print("Number of Samples:",len(id_dict))
        
        for x,y in id_dict.items():
            print (x,':',y)
        sample_id = self.get_ids('All')
        if len(sample_id) != len(set(sample_id)):
            raise Exception('Error: Check unique Sample IDs in: Groups.csv for error')
        
        skeleton_input = pd.read_table(self.data)
        metabolite_list = skeleton_input['Metabolite']
        # if len(metabolite_list) != len(set(metabolite_list)):
#             raise Exception('Error: Check Metabolite column for duplicates in : Skeleton_input.tsv')
        
        if self.get_matrix(self.get_ids('All')).isnull().values.any():
            raise Exception('Error: Check for Missing Values in Sample intensities: Skeleton_input.csv')
        
        if len(sample_id) != len(self.get_matrix(self.get_ids('All')).columns):
            raise Exception('Error: Check if Number of Samples in Groups.csv matches Skeleton_input.tsv')
    
        skeleton = self.get_ids('All')
        groups = pd.read_csv(self.samplesheet)['File'].tolist()
        
        if set(groups).issubset(skeleton) == False:
            raise Exception('Samplesheet Sample Names Incorrectly Match Skeleton File Names')
    

        
    def dir_create(self):
        groups = pd.read_csv(self.samplesheet)
        if self.method == 'flux':
            results_folder  = 'Flux-DME-results-'+str(len(self.get_ids('True'))) + '-Samples/'
        if self.method == 'sum':
            results_folder  = 'Sum-DME-results-'+str(len(self.get_ids('True'))) + '-Samples/'
        if self.method == 'median':
            results_folder  = 'Median-DME-results-'+str(len(self.get_ids('True'))) + '-Samples/'
        if self.method == 'default':
            results_folder  = 'DME-results-'+str(len(self.get_ids('True'))) + '-Samples/'

        sub_directories = [results_folder+ subdir for subdir in ['Volcano','Heatmap','Tables','PCA','Inputs','Pathway','Impacts']]
        sub_directories.append(results_folder)
        
        for direc in sub_directories:
            if not os.path.exists(direc):
                os.makedirs(direc)

    
    def get_groups(self):
    # Get corresponding IDs for each group in Groups.csv

        project = pd.read_csv('inputs/Groups.tsv',sep='\t')
        grouped_samples = {}

        for condition in (project.Group.unique()):
            if condition != 'Blank':
                test = [x.split('.')[0] for x in project.loc[project['Group'] == condition, 'File'].tolist()]
                grouped_samples[condition] = test
        return (grouped_samples)

    def get_ids(self,full):
        
        # Return sample IDS for all samples including blanks
        if full == 'All':
            # skeleton = pd.read_table(self.data)
            
            # spike_cols = [col for col in skeleton.columns if 'S' in col]
            # spike_cols.pop(0)
            project = pd.read_table('inputs/Groups.tsv',sep='\t')
            samples = project['File'].tolist()
            return (list(samples))
        
        # Get all sequence IDS (xml ids) from Groups.csv
        if full == 'True':
            project = pd.read_table('inputs/Groups.tsv',sep='\t')
            project = project.loc[project['Group'] != 'Blank']
            all_samples = [x.split('.')[0] for x in project['File'].tolist()]
            return(all_samples)
        
        if full == 'Sample':
            project = pd.read_csv('inputs/Groups.tsv',sep='\t')
            project = project.loc[project['Group'] != 'Blank']
            all_samples = [x.split('.')[0] for x in project['id'].tolist()]
            return(all_samples)
        
        # Get all blank IDS from skeleton output matrix
        if full == 'Blank':
            project = pd.read_csv('inputs/Groups.tsv',sep='\t')
            project = project.loc[project['Group'] == 'Blank']
            all_samples = [x.split('.')[0] for x in project['File'].tolist()]
            return (list(all_samples))
        if full == 'ID':
            project = pd.read_csv('inputs/Groups.tsv',sep='\t')
            grouped_samples = {}
            
            for condition in (project.id.unique()):

                test = [x.split('.')[0] for x in project.loc[project['id'] == condition, 'File'].tolist()]
                test = ''.join(test)
                grouped_samples[test] = condition
            return(grouped_samples)
    
    def sequence2id(self,result):
        
        ids = self.get_ids('ID')
    
        for x,y in ids.items():
            #print(x,y)
            result.rename(columns={x: y}, inplace=True)
            # Returns matrix based on inputted IDS
        return(result)
    
    def get_matrix(self,ids):
        
        skeleton_outbut_hybrid = pd.read_table(self.data)
        skeleton_outbut_hybrid = skeleton_outbut_hybrid.set_index('Metabolite')
        
        matrix = (skeleton_outbut_hybrid[skeleton_outbut_hybrid.columns.intersection(ids)])
        return (matrix)





if not os.path.exists(results_folder+'QC'):
    os.makedirs(results_folder+'QC')

skeleton_name = [x for x in os.listdir('inputs') if x.endswith('output.tsv')][0]

skeleton_input = pd.read_csv('inputs/'+skeleton_name,sep='\t')
groups = pd.read_csv('inputs/Groups.tsv',sep='\t')

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)

ax = sns.distplot(np.array(skeleton_input['detections']), bins=20, kde=False, rug=True);
ax.set_title('Sample Detection Frequency')
ax.set_ylabel('Detection')
ax.set_xlabel('Frequency')
plt.savefig(results_folder+'QC/plot.detection.png',dpi=400)


a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.countplot(y="winner", data=skeleton_input)
ax.set_title('Sample Winner vs. Frequency')
ax.set_ylabel('Sample')
ax.set_xlabel('Count')
plt.savefig(results_folder+'QC/plot.winner.png',dpi=400)
# 
# 
# skeleton_input[['ion','polarity']] = skeleton_input['Ion Type'].str.split(']',expand=True)
# 
# a4_dims = (11.7, 8.27)
# fig, ax = plt.subplots(figsize=a4_dims)
# 
# ax = sns.countplot(y="polarity", data=skeleton_input)
# ax.set_title('Polarity Ratio')
# ax.set_ylabel('Polarity')
# ax.set_xlabel('Count')
# plt.savefig('QC/plot.polarity.png',dpi=400)
# 


try:
	skeleton_name = [x for x in os.listdir('inputs') if x.endswith('quantified.tsv')][0]
except IndexError:
	skeleton_name = [x for x in os.listdir('inputs') if x.endswith('output.tsv')][0]

result = Analysis(data=skeleton_name,samplesheet='Groups.csv',blank_threshold_value=10000,method='default')
full_matrix = result.get_matrix(result.get_ids(full='All'))
#full_matrix = full_matrix[(full_matrix.T != 0).any()]
print(full_matrix.head())
df_list = []
for col in full_matrix.columns:
    new_df = (pd.DataFrame(full_matrix[col]))
    new_df[col+'_sample'] = col
    new_df.columns = ['Signal','Sample']
    new_df = new_df[new_df.Signal != 0]
    new_df['lognorm'] = np.log(new_df['Signal'])
    df_list.append(new_df)
    
df = pd.concat(df_list)
a4_dims = (15.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)

groups = pd.read_csv('inputs/Groups.csv')

groups.loc[groups['Group'] == 'Blank', 'Color'] = '#FF35E7'




ax = sns.violinplot(x="lognorm", y="Sample", data=df,scale="count",inner='box',palette=groups['Color'].tolist())
ax.set_title('Violin Plot - lognorm')
ax.set_ylabel('Sample')
ax.set_xlabel('Normalized Intensity')
plt.savefig(results_folder+'QC/plot.distribution.png',dpi=400)


sum_intensity = pd.DataFrame(full_matrix.sum())
sum_intensity['sample'] = sum_intensity.index
sum_intensity.columns = ['Sum Signal','Sample']

a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.barplot(x="Sum Signal", y="Sample", data=sum_intensity,palette=groups['Color'].tolist())
ax.set_title('Sample Sum Intensities')
ax.set_ylabel('Sample')
ax.set_xlabel('Sum Signal')
plt.savefig(results_folder+'QC/plot.sum.signal.png',dpi=400)





full_corr = full_matrix.corr(method='pearson')
a4_dims = (15.7, 12.27)

fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.heatmap(full_corr,annot=True,linewidths=.5,cmap="vlag")
ax.set_title('Sample Correlation Analysis')

plt.savefig(results_folder+'QC/plot.correlation.png',dpi=400)





a4_dims = (15.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
ax = sns.pairplot(full_matrix)
plt.savefig(results_folder+'QC/plot.correlation.pairwise.png',dpi=400)






