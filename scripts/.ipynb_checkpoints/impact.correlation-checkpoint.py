import pandas as pd
import numpy as np
import os
import sys


dme_file =sys.argv[1]

dme = pd.read_csv(dme_file)
scatter_subset = [x for x in dme.columns if x.endswith('impact_score')]

for impact_score in scatter_subset:
    x_random = (dme[impact_score])
    y_random = dme['RT']
    # Create a trace
    trace = go.Scatter(
        x = y_random,
        y = x_random,
        mode = 'markers'
    )
    
    
    data = [trace]
    file_name = dme_file.split('/')[0] + 'Correlation'+ '/'+ impact_score.split('_impact')[0]+'.html'
    plotly.offline.plot(data,filename=file_name)



