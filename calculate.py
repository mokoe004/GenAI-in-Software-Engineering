from data import config

import pandas as pd


# Milestone erreicht
# dann iteration aus config.roadmap_data ignorieren

# Success depends on Milestones reached and CSF met

# Funktion zur Berechnung der Zielwahrscheinlichkeit
def calculate_goal_probability(goal):
    total_weight = 0
    weighted_sum = 0

    for factor in goal["Factors"]:
        csfs = config.csf_data.to_dict(orient='records')
        factor_name = factor["Name"]
        factor_weight = factor["Weight"]

        # Suchen im KPI oder CSF
        if factor_name in config.kpi_data:
            progress = config.kpi_data[factor_name] / 100  # KPI als Anteil
        else:
            csf = next((c for c in csfs if c["Metric"] == factor_name), None)
            if csf:
                progress = csf["Current"] / csf["Target"]  # CSF als Anteil
            else:
                continue

        weighted_sum += progress * factor_weight  # Beispiel KPI zu 50% erreicht und Gewichtung von 50% für dieses goal: KPI: 0.5 * Weight: 0.5 = 0.25
        total_weight += factor_weight  # Total weigth um die Summe der Gewichtungen zu berechnen

    return weighted_sum / total_weight if total_weight > 0 else 0  # weighted_sum/ total_weight : Wahrscheinlichkeit für das Goal


def calculate_goals_probabilities():
    # Liste zur Speicherung der Wahrscheinlichkeiten für alle Ziele
    for goal in config.goals:
        probability = calculate_goal_probability(goal)
        for goal_prob in config.goal_probabilities_list:
            if(goal_prob["Goal"] == goal["Description"]):
                goal_prob["Probability"] = round(probability * 100, 2)
    # DataFrame aus der Liste erstellen
    goal_probabilities = pd.DataFrame(config.goal_probabilities_list)
    goal_probabilities["Probability"] = goal_probabilities["Probability"].astype(str) + "%"
    print(f"Goal Probabilities: {goal_probabilities}")
    return goal_probabilities


def calculate_success_rate(milestones_achieved, slider_values):
    # Beispiel: Erfolgschance basierend auf der Anzahl der erreichten Meilensteine
    milestone_factor = len(milestones_achieved) * 10
    slider_factor = sum(slider_values) / len(slider_values) if slider_values else 0
    return min(100, milestone_factor + slider_factor)  # Maximal 100%

# Für sucess rate
def calculate_team_influence():
    # Calculate average resistance and commitment levels
    total_resistance = sum([member["params"]["Resistance"] for member in config.team_members])
    total_commitment = sum([member["params"]["Level of Commitment"] for member in config.team_members])
    team_influence = (total_commitment - total_resistance) / (len(config.team_members) * 10)
    return max(0, team_influence)  # Ensure non-negative influence

def calculate_overall_success():
    # Calculate probabilities for each goal
    team_calc = 0.2
    goals_calc = 0.4
    milestones_calc = 0.4

    goals_probabilities_mean = 0.00
    for goal in config.goal_probabilities_list:
        goals_probabilities_mean += goal["Probability"]
    goals_probabilities_mean /= len(config.goal_probabilities_list)

    # Calculate team influence
    team_influence = calculate_team_influence()

    # Adjust probabilities for milestones achieved
    #milestones_achieved = [milestone["Milestones"] for milestone in config["milestones"] if
                           #milestone["End"] <= "2025-01-19"]
    #milestone_factor = len(milestones_achieved) / len(config["milestones"])
    milestone_factor = 0.5
    milestones_achieved = 2

    # Overall probability as weighted sum of goal probabilities and team influence
    overall_probability = (goals_probabilities_mean * 0.7) + (milestone_factor * 0.2) + (team_influence * 0.1)

    return {
        "Overall Success Probability (%)": round(overall_probability * 100, 2),
        "Milestones Achieved": milestones_achieved,
        "Team Influence Factor": round(team_influence, 2)
    }
