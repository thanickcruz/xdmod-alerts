import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy 
from datetime import date

def quality_heatmap(df, past_df=None):
        
    dates = list(df.columns)
    jobs = list(df.index)

    fig, ax = plt.subplots(figsize=(8, 8))
    cmap = plt.get_cmap("RdYlGn").copy()
    cmap.set_bad('gray', 1.)
    im = ax.imshow(df, cmap = cmap, vmin=0, vmax=100)

    ax.set_xticks(numpy.arange(len(dates)))
    ax.set_yticks(numpy.arange(len(jobs)))
                  
    ax.set_xticklabels(dates)
    ax.set_yticklabels(jobs)
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    for i in range(len(jobs)):
        for j in range(len(dates)):
            text = ax.text(j, i, df.iloc[i][j], ha="center", va="center", color="w")
            if past_df is not None:
                change = df.iloc[i][j] - past_df.iloc[i][j]
                if not numpy.isnan(change):
                    text2 = ax.text(j, i+.25, f'{change}%\n change', ha="center", va="center", color="b")
                else:
                    text2 = ax.text(j, i+.25, 'change\nN/A', ha="center", va="center", color="w")
    ax.set_title(df.name)
    fig.tight_layout()
    plt.show()
        