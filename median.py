import pandas as pd
import metabolyze as met
import numpy as np
#skeleton_name = [x for x in os.listdir('inputs') if x.endswith('output.tsv')][0]
# 	result = Analysis(data=skeleton_name,samplesheet='Groups.csv',blank_threshold_value=10000)
# 	result.t_test()
#normalized_df=(df-df.mean())/df.std()
#result = Analysis(data='skeleton_output.tsv',samplesheet='Groups.csv',blank_threshold_value=10000)
#matrix = result.get_matrix(result.get_ids('All'))
x = met.Analysis(data='skeleton_output.tsv',samplesheet='Groups.csv',blank_threshold_value=10000)
corrected_matrix = (x.get_imputed_full_matrix(x.get_matrix(ids=x.get_ids('True')),param='corrected'))##
blank_matrix = x.get_matrix(ids=x.get_ids('Blank'))
blank_matrix[blank_matrix>1] = 0
mergedDf = corrected_matrix.merge(blank_matrix, left_index=True, right_index=True)
matrix_sum_normalized = mergedDf.div(mergedDf.sum(axis=0), axis=1)
matrix_sum_normalized = matrix_sum_normalized.fillna(0)
#matrix_median_normalized = mergedDf.div(mergedDf.replace(0, np.nan).median(axis=0), axis=1)
# matrix_median_normalized['Metabolite'] = matrix_median_normalized.index
# matrix_median_normalized = matrix_median_normalized.reset_index(drop=True)
original = pd.read_csv('inputs/skeleton_output.tsv',sep='\t')
original.update(matrix_sum_normalized)
original.to_csv('inputs/skeleton_sum_normalized.tsv',sep='\t')

normalize_result = met.Analysis(data='skeleton_sum_normalized.tsv',samplesheet='Groups.csv',blank_threshold_value=0)
normalize_result.t_test()
