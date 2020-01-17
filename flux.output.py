import pandas as pd


import sys


input_matrix =sys.argv[1]


intensity_detected = pd.read_csv(input_matrix)
intensity_detected.index = intensity_detected['Metabolite']
del intensity_detected['Metabolite']

flux_metabolites = intensity_detected.index.tolist()

zero_index = []
for index,metabolite in enumerate(flux_metabolites):
    #print(index,metabolite)
    if metabolite.split('-').pop() == '0':
        #print(index,"This is 0th ################")
        zero_index.append(index)

        
total_index_zip = []
for i,item in enumerate(zero_index):
    if i != 0:
        get_previous=zero_index[i-1]
        paired_index_subset = [get_previous,item]
        total_index_zip.append(paired_index_subset)

last_search = [zero_index[-1],len(flux_metabolites)]
total_index_zip.append(last_search)


myDataFrame = []
for x,y in total_index_zip:
    flux_search = (flux_metabolites[x:y])
    flux_search_0_removed = flux_search[1:]
    test = (intensity_detected[intensity_detected.index.isin(flux_search)])
    test_removed = (intensity_detected[intensity_detected.index.isin(flux_search_0_removed)])
    new_final_test = test_removed.sum(axis=0) / test.sum(axis=0) * 100
    new_final_df = pd.DataFrame(new_final_test).transpose()
    new_final_df.index = [flux_search[0]]
    #print(pd.DataFrame(new_final_df))
    myDataFrame.append(new_final_df)


#output_name = input_matrix.split('/')[0] + '/' + input_matrix.split('/')[1] + '/'+ 'flux.output.csv'
output_name = 'inputs/flux.output.csv'
appended_data = pd.concat(myDataFrame, axis=0)
appended_data = appended_data.round(2)
appended_data = appended_data.fillna(0)
appended_data.to_csv(output_name)  
print("Flux Analysis Complete")
