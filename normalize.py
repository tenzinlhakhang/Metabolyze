import os
import pandas as pd
import metabolyze as met
import numpy as np
skeleton_name = [x for x in os.listdir('inputs') if x.endswith('output.tsv')][0]
# 	result = Analysis(data=skeleton_name,samplesheet='Groups.csv',blank_threshold_value=10000)
# 	result.t_test()
#normalized_df=(df-df.mean())/df.std()
#result = Analysis(data='skeleton_output.tsv',samplesheet='Groups.csv',blank_threshold_value=10000)
#matrix = result.get_matrix(result.get_ids('All'))
x = met.Analysis(data=skeleton_name,samplesheet='Groups.csv',blank_threshold_value=10000,method='default')
corrected_matrix = (x.get_imputed_full_matrix(x.get_matrix(ids=x.get_ids('True')),param='corrected'))##
blank_matrix = x.get_matrix(ids=x.get_ids('Blank'))
blank_matrix[blank_matrix>1] = 0


mergedDf = corrected_matrix.merge(blank_matrix, left_index=True, right_index=True)
matrix_sum_normalized = mergedDf.div(mergedDf.sum(axis=0), axis=1)
matrix_sum_normalized = matrix_sum_normalized.fillna(0)

matrix_median_normalized = mergedDf.div(mergedDf.replace(0, np.nan).median(axis=0), axis=1)
matrix_median_normalized = matrix_median_normalized.fillna(0)
#matrix_median_normalized = matrix_median_normalized.reset_index(drop=True)


#sum

original = pd.read_csv('inputs/'+skeleton_name,sep='\t',index_col=0)
matrix_sum_normalized.index.names = ['Metabolite']
detect_column = original.columns.get_loc("detections")
meta_data_df = original[original.columns[0:detect_column+1]]
meta_data_df['Skeleton_Metabolite'] = meta_data_df.index
meta_data_df.index = meta_data_df['Metabolite']
final = pd.merge(meta_data_df, matrix_sum_normalized, left_index=True, right_index=True)
col = final.pop("Skeleton_Metabolite")
final.insert(0, 'Skeleton_Metabolite',col)
print(final.columns)
final.to_csv('inputs/skeleton_sum_normalized.tsv',sep='\t',index=False)


# Median
original.to_csv('inputs/sum.test.forreal.tsv',sep='\t')
matrix_median_normalized.index.names = ['Metabolite']
detect_column = original.columns.get_loc("detections")
meta_data_df = original[original.columns[0:detect_column+1]]
meta_data_df['Skeleton_Metabolite'] = meta_data_df.index
meta_data_df.index = meta_data_df['Metabolite']
final = pd.merge(meta_data_df, matrix_median_normalized, left_index=True, right_index=True)
col = final.pop("Skeleton_Metabolite")
#del final['Metabolite.1']
final.insert(0, 'Skeleton_Metabolite',col)
final.to_csv('inputs/skeleton_median_normalized.tsv',sep='\t',index=False)

# 
# # 
sum_normalize_result = met.Analysis(data='skeleton_sum_normalized.tsv',samplesheet='Groups.csv',blank_threshold_value=0,method='sum')
sum_normalize_result.t_test()
# # # 
median_normalize_result = met.Analysis(data='skeleton_median_normalized.tsv',samplesheet='Groups.csv',blank_threshold_value=0,method='median')
median_normalize_result.t_test()
