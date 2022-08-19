import json
import xdmod.outlier_detection as od

with open('config.json', 'r') as f:
    json_variables = json.load(f)
    
hosts = json_variables['hosts']
start = json_variables['outlier_range']['start_date']
end = json_variables['outlier_range']['end_date']

od.config_json(hosts, start, end_date = end)
print('Reference date range sucessfully configured.')