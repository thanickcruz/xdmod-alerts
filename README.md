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

### `config.json`
The `config.json` file contains the necessary configurable variables.

#### hosts
This should map **host name to its url**. For instance, 

`"hosts": {"metrics-dev": "https://metrics-dev.ccr.buffalo.edu:9004", "ookami": "https://ookami.ccr.xdmod.org", "xdmod-dev": "https://xdmod-dev.ccr.xdmod.org:9002"}`

#### webhook
Paste the Slack webhook url into the `webhook` variable.

#### outlier_range
Provide start and end dates in **YYYY-MM-DD** format.

### Outlier Detection Setup
Run the `outlier_config.py` script whenever a date range must be configured. It will pull the necessary variables from the `config.json` file and generate a directory called `outlier_config` containing all reference json files for the configured hosts.

### Environment Variables
Additionally, proper environment variables must be assigned for logging in. On the command line, export the following variables:
1. `XDMOD_USER=[your_username]`
2. `XDMOD_PASS=[your_password]`

## Automate using `nbconvert` and `crontab`
Schedule the following command to run from `usr/share/xdmod/html/reports/xdmod-alerts` every Monday at 6:00am.

```0 6 * * MON cd [path to supremm-alert dir] && [path to jupyter command]jupyter nbconvert --execute  --to html --output "`date +"%Y-%m-%d"`_report.html" "supremm-alert.ipynb" --no-input```

Expect a Slack message with alerts and a working link to the full report.

#### Warnings and Notes:
- Queries for the `script` type may have longer runtimes than other types.
