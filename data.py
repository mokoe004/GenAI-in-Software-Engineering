import pandas as pd
import json

# Load parameters from the JSON file
with open('params.json', 'r') as file:
    data = json.load(file)

# Convert milestones to a DataFrame and parse dates
roadmap_data = pd.DataFrame(data['milestones'])
roadmap_data["Start"] = pd.to_datetime(roadmap_data["Start"])
roadmap_data["End"] = pd.to_datetime(roadmap_data["End"])

# Load KPIs
kpi_data = data['kpis']

# Convert CSFs to a DataFrame
csf_data = pd.DataFrame(data['csfs'])

# Load goals
goals = data['goals']

# Load team members
team_members = data['team_members']