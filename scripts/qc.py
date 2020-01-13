import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings("ignore")



skeleton = sys.argv[1]
groups = sys.argv[2]
# skeleton='inputs/skeleton_output.tsv'
# groups = 'inputs/Groups.tsv'

def get_matrix(ids):

    skeleton_outbut_hybrid = pd.read_csv(skeleton,sep="\t")
    skeleton_outbut_hybrid = skeleton_outbut_hybrid.set_index('Metabolite')

    matrix = (skeleton_outbut_hybrid[skeleton_outbut_hybrid.columns.intersection(ids)])
    matrix = matrix.fillna(0)
    return (matrix)

def get_id_match():
    grouped_samples = {}

    for condition in (project.id.unique()):

        test = [x.split('.')[0] for x in project.loc[project['id'] == condition, 'File'].tolist()]
        test = ''.join(test)
        grouped_samples[test] = condition
    return(grouped_samples)

def sequence2id(df_to_rename):

    ids = get_id_match()

    for x,y in ids.items():
        #print(x,y)
        df_to_rename.rename(columns={x: y}, inplace=True)
        # Returns matrix based on inputted IDS
    return(df_to_rename)

def get_group_to_CV():
    grouped_samples = {}
    project = pd.read_csv(groups,sep='\t')

    for condition in (project.Group.unique()):
        test = [x.split('.')[0] for x in project.loc[project['Group'] == condition, 'File'].tolist()]
        grouped_samples[condition] = test

    project = project.loc[project['Group'] != 'STD']
    project = project.loc[project['Group'] != 'Blank']
    non_istd_samples = [x.split('.')[0] for x in project['File'].tolist()]
    grouped_samples['Samples'] = non_istd_samples
    return(grouped_samples)


def calculate_cv(groups_to_analyze):
    
    CV_groups = []
    for group,ids in groups_to_analyze.items():
        group_matrix = ((get_matrix(ids)))
        group_matrix = group_matrix.fillna(0)
        #group_matrix = group_matrix.replace(0, None)
        metabolites = group_matrix.index

        A = np.array(group_matrix)
        cv =  lambda x: np.std(x) / np.mean(x)
        var = np.apply_along_axis(cv, axis=1, arr=A)

        variance_df = pd.DataFrame(var)
        variance_df.index = metabolites
        variance_df.columns = [group+'_CV']
        variance_df = variance_df*100
        variance_df.fillna(0)

        CV_groups.append(variance_df)

    cv_single = pd.concat(CV_groups,axis=1)
    return(cv_single)



if __name__ == "__main__":
    standard = pd.read_csv(skeleton,sep='\t',index_col=0)
    project = pd.read_csv(groups,sep='\t')
    group_cv_df = calculate_cv(get_group_to_CV())
    skeleton_cv_merged = standard.join(group_cv_df, how='outer')
    skeleton_cv_merged = skeleton_cv_merged.fillna(0)
    skeleton_cv_merged = sequence2id(skeleton_cv_merged)

    outname = skeleton.split('/')[-1]+'_CV.tsv'
    skeleton_cv_merged.to_csv(outname,sep="\t")



