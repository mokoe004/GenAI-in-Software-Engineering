import pandas as pd
import json

with open('params.json', 'r') as file:
    data = json.load(file)

# Milestones in DataFrame umwandeln
roadmap_data = pd.DataFrame(data['milestones'])
roadmap_data["Start"] = pd.to_datetime(roadmap_data["Start"])
roadmap_data["End"] = pd.to_datetime(roadmap_data["End"])

# KPIs laden
kpi_data = data['kpis']

# CSFs in DataFrame umwandeln
csf_data = pd.DataFrame(data['csfs'])

goals = data['goals']

team_members = data['team_members']