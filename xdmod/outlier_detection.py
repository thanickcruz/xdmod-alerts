import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statistics
from datetime import date
import datetime
import requests
import json
import os

import xdmod.datawarehouse as xdw

def config_json(hosts, start_date, end_date = date.today(), config_all = False):
    
    folder_path = './outlier-config'
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    if config_all:
        for host in hosts:
            with xdw.DataWareHouse(hosts[host]) as warehouse:
                for type in ['gpu','hardware', 'cpu', 'realms']: # ADD SCRIPT LATER ON
                    df = warehouse.get_qualitydata({"start": start_date, "end": end_date, "type": type})
                    json_data = df.to_json()
                    with open(f'outlier-config/{host}-{type}.json', 'w') as json_file:
                        json_file.write(json_data)
                        
def display_config(hostname, type, resource):
    with open(f'outlier-config/{hostname}-{type}.json', 'r') as f:
        data = json.load(f)
        x = [date for date in data]
        y = [data[date][resource] if data[date][resource] is not None 
             else np.nan for date in x]
        mean = np.full(len(y), np.nanmean(y))
        std = statistics.stdev(y)
        threshhold = mean - std
    
        fig, ax = plt.subplots(figsize=(20, 8))
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
        plt.plot(x,y,'-.')
        plt.plot(mean, '--')
        plt.fill_between(np.arange(len(y)),mean, threshhold, facecolor= 'orange', alpha=.2)
        plt.xlabel('Date')
        plt.ylabel(f'% of Jobs with {type} Info')
        plt.title(f'Config for {hostname} {type} Data at {resource} resource')
        
        plt.show()
    
def detect_outlier(df, hostname, resource):
    
    title_to_type = {'% of CCR SUPReMM jobs with GPU information': 'gpu',
                 '% of CCR SUPReMM jobs with hardware perf information':'hardware',
                 '% of CCR SUPReMM jobs with cpu usage information':'cpu',
                 '% of CCR SUPReMM jobs with Job Batch Script information': 'script',
                 '% of CCR jobs in the SUPReMM realm compared to Jobs realm':'realms'}

    
    with open(f'outlier-config/{hostname}-{title_to_type[df.name]}.json', 'r') as f:
        reference = json.load(f)
        quality = [reference[date][resource] if reference[date][resource] is not None
                   else np.nan for date in reference]
        
        mean = np.mean(quality)
        std = statistics.stdev(quality)
        threshhold = mean - std
    
    outlier_info = {'alert': False, 'ref_mean': mean, 'ref_std': std, 'ref_threshhold': mean - std}
    
    for val in df.loc[resource]:
        if val<threshhold:
            outlier_info['alert'] = True
    
    return outlier_info