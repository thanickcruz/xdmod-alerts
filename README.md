# README

This alerts system gathers weekly SUPReMM quality data and sends visual reports via Slack.

## Dependencies
### Anaconda
Requires [**Anaconda**](https://www.anaconda.com/products/distribution) for the latest version of Python and various modules.

`wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
chmod +x Anaconda3-2022.05-Linux-x86_64.sh
./Anaconda3-2022.05-Linux-x86_64.sh`
### xdmod-python
Requires the [Python module for xdmod](https://github.com/jpwhite4/xdmod-python) for `datawarehouse` objects and visualizers.

# SETUP

## [Slack API](https://api.slack.com/#read_the_docs)
A Slack app with a webhook must first be generated to facilitate requests to the Slack API.
### Create app
"Create an app" $\rightarrow$ "Create new app" $\rightarrow$ "From scratch" $\rightarrow$ _Make name and select Slack workspace_ $\rightarrow$ "Create app"

### Add webhook to app
"Incoming Webhooks" $\rightarrow$ _Activate incoming webhooks_ $\rightarrow$ "Add new webhook to workspace" $\rightarrow$ _Select channel_ $\rightarrow$ "Allow"

**The url provided contains a secret. Do not expose this to git, or its functionality will automatically deactivate.**

## Git Clone SUPReMM Alerts Repo

- On the the desired system, cd into `usr/share/xdmod/html/`
- `mkdir reports`
- `cd reports`
- `git clone ___ `

## Configuration

### Hosts
The `supremm-alert.ipynb` notebook must be configured to access the desired servers/hosts. The variable `hosts` should map **host name to its url**. For instance, 

`'metrics-dev': 'https://metrics-dev.ccr.buffalo.edu:9004', 'ookami': 'https://ookami.ccr.xdmod.org', 'xdmod-dev': 'https://xdmod-dev.ccr.xdmod.org:9002'`

### Outlier Detection Setup
The outlier detection functionality must be configured to a desired date range. The `outlier_detection.py` file contains the function `config_json` which takes the `hosts` dictionary, `start_date`, and optional `end_date` (defaults to today). Function creates a directory from where it was run called `outlier_config` containing all reference json files for `hosts`. For instance,

`config_json(hosts, '2022-05-01', end_date = '2022-07-01', config_all = True)`

### Webhook Variable 
In the `supremm-alert.ipynb` notebook, paste the Slack webhook url into the `webhook` variable.

### Environment Variables
Additionally, proper environment variables must be assigned for logging in. On the command line, export the following variables:
1. `XDMOD_USER=[your_username]`
2. `XDMOD_PASS=[your_password]`

## Automate using `nbconvert` and `crontab`
Schedule the following command to run from `usr/share/xdmod/html/reports/xdmod-alerts` every Monday at 6:00am.

```0 6 * * MON cd [path to supremm-alert dir] && [path to jupyter command]jupyter nbconvert --execute  --to html --output "`date +"%Y-%m-%d"`_report.html" "supremm-alert.ipynb" --no-input```

Expect a Slack message with alerts and a working link to the full report.


```python
0 6 * * MON cd /data/www/nacruz/share/html/reports/xdmod-alerts && ~/anaconda3/bin/jupyter nbconvert --execute  --to html --output "`date +"%Y-%m-%d"`_report.html" "supremm-alert.ipynb" --no-input




```
