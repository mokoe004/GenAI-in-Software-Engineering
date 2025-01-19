import pandas as pd
import json

class Config:
    def __init__(self):
        with open('params.json', 'r') as file:
            data = json.load(file)

        self.roadmap_data = pd.DataFrame(data['milestones'])
        self.roadmap_data["Start"] = pd.to_datetime(self.roadmap_data["Start"])
        self.roadmap_data["End"] = pd.to_datetime(self.roadmap_data["End"])

        self.kpi_data = data['kpis']
        self.csf_data = pd.DataFrame(data['csfs'])
        self.goals = data['goals']
        self.team_members = data['team_members']
        self.success_rate = 20.00
        self.goal_probabilities_list = init_goal_probabilities_list(self.goals)



def init_goal_probabilities_list(goals):
    goal_probabilities_list = []
    for goal in goals:
            goal_probabilities_list.append(
                {
                        "Goal": goal["Description"],
                    "Probability": 0.22  # Platzhalter
                }
            )
    return goal_probabilities_list
config = Config()