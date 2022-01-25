# Adds people to a team in an org on GitHub
# Example:

#python add_team_to_github.py --path="/Users/tiffany/Downloads/GitHub_username Survey Student Analysis Report.csv" --column_name="1381024: What is your GitHub.com username?" --org=UBC-DSCI --team=students

import github3
from github3 import login
import os
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path')
parser.add_argument('--column_name')
parser.add_argument('--org')
parser.add_argument('--team')
args = parser.parse_args()
path = args.path
column_name = args.column_name
org = args.org
team = args.team

# get token 
# this only reads from "GITHUB_COM_PAT" from os.environ in .py script, 
# in notebook you must enter GitHub.com API token in text box (see else thingy)
if "GITHUB_COM_PAT" in os.environ:
    token = os.environ["GITHUB_COM_PAT"]
    print("Successfully read GitHub.com PAT from environment variable.")
else:
    token = input("Please enter your GitHub.com API token: ")

# log in to GHE
self = login(token=token)

# get DSCI org
orgname = org
self.org = self.organization(orgname)

# create team
team_name = team

# load new team members csv
team_members = pd.read_csv(path)
#team_members = team_members.dropna()  
team_members.rename(columns = {column_name:'username'}, inplace = True)
team_members.username = team_members.username.apply(str.strip)

# try to create team (in case it doesn't yet exist)
try:
    self.org.create_team(team, permission = "pull")
except:
    pass

# add team members to team 
# retrieve team as dictionary item, where I can use team name as key
self.teams = {team.name : team for team in self.org.teams()}

# use invite function to invite team from csv file
for username in team_members.username.values:
    try:
        self.teams[team_name].invite(username)
    except:
        print(username, "failed to add to", team, "team")
