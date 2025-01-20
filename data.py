import pandas as pd
import json

class Config:
    def __init__(self):
        with open('params.json', 'r') as file:
            data = json.load(file)

        self.roadmap_data = pd.DataFrame(data['iterations'])
        self.roadmap_data["Start"] = pd.to_datetime(self.roadmap_data["Start"])
        self.roadmap_data["End"] = pd.to_datetime(self.roadmap_data["End"])

        self.iteration_milestone = data['iteration_milestone']

        self.kpi_data = data['kpis']
        self.csf_data = pd.DataFrame(data['csfs'])
        self.goals = data['goals']
        self.team_members = data['team_members']
        self.goal_probabilities_list = init_goal_probabilities_list(self.goals)
        self.milestones_achieved = []

        self.success_rate = 0
        self.milestone_multiplicator = 0
        self.goals_multiplicator = 0.4
        self.team_multiplicator = 0.2
    def get_success_rate(self):
        print(self.goal_probabilities_list)
        print(f"Goals multiplicator: {self.goals_multiplicator}, Milestone multiplicator: {self.milestone_multiplicator}, Team multiplicator: {self.team_multiplicator}")
        return round((self.success_rate + self.milestone_multiplicator + self.goals_multiplicator + self.team_multiplicator)*100,2)



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