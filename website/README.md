# Website Builder

## Setup and Installation

1. Set up and and Install all the related software into a dev environment by making a conda environment from the environment.yml file:  `conda env create -f environment.yml` .  The new environment is called "ibots-site" by default.

2. Activate the conda environment: `conda activate ibots-site` 

3. To get the non-open data and software needed to run this code, we use dvc.  Just get the credentials you need to access the data from Nick and call `dvc pull`.  You should see the directories `data/` and `theme/` appear.

## Build the Website

1. Build all files needed for a webserver to host the website to the **./_output** directory: `python main.py`

2. Examine the website in a browser: `python main.py -m http.server -d _output`


## Update the Website with the latest group data

The website is always using the last-used version of the database, even if the database has been updated since.  This is a safety feature--it prevents changes to the database from pushing breaking changes onto the website, and it allows developers to try out the latest database temporarily and go back to the last working version if they aren't able to get the site working with the newest data.  We do, however, want to use the latest version of the database whenever possible.  Here's how to do this manually:

1. `dvc update data`.  This checks for any differences between the website's used version of the data and the db's current version and updates the website's version to match.

If you want to roll back, just rollback the `data.dvc` file and run another `dvc pull`.