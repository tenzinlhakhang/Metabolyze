import plotly
import pandas as pd
import numpy as np
import os
import sys
import plotly.plotly as py
import plotly.graph_objs as go


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
    title = impact_score.split('_impact')[0]
    
    layout= go.Layout(
    title= title,
    hovermode= 'closest',
    xaxis= dict(
        title= 'Retention Time',
        ticklen= 5,
        zeroline= False,
        gridwidth= 2,
    ),
    yaxis=dict(
        title= 'Impact Score',
        ticklen= 5,
        gridwidth= 2,
    ),
    showlegend= False)
    

    
    data = [trace]
    fig= go.Figure(data=data, layout=layout)
    file_name = dme_file.split('/')[0]+'/Correlation/'+impact_score.split('_impact')[0]+'.html'
    plotly.offline.plot(fig,filename=file_name)




