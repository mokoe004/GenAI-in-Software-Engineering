from data import config

import pandas as pd


# Milestone erreicht
# dann iteration aus config.roadmap_data ignorieren

# Success depends on Milestones reached and CSF met

# Funktion zur Berechnung der Zielwahrscheinlichkeit
def calculate_goal_probability(goal):
    """
    Calculate the probability of a goal being achieved based on the factors and their weights.

    Args:
        goal (dict): Goal to calculate the probability for.

    Returns:
        float: Probability of the goal being achieved.
    """
    total_weight = 0
    weighted_sum = 0

    for factor in goal["Factors"]:
        factor_name = factor["Name"]
        factor_weight = factor["Weight"]

        # Suchen im KPI oder CSF
        if factor_name in config.kpi_data:
            progress = config.kpi_data[factor_name] / 100  # KPI als Anteil
        else:
            csf = next((c for c in config.csf_data if c["Metric"] == factor_name), None)
            if csf:
                progress = csf["Current"] / csf["Target"]  # CSF als Anteil
            else:
                continue

        weighted_sum += progress * factor_weight  # Beispiel KPI zu 50% erreicht und Gewichtung von 50% für dieses goal: KPI: 0.5 * Weight: 0.5 = 0.25
        total_weight += factor_weight  # Total weigth um die Summe der Gewichtungen zu berechnen

    return weighted_sum / total_weight if total_weight > 0 else 0  # weighted_sum/ total_weight : Wahrscheinlichkeit für das Goal

def calculate_goals_probabilities():
    """
    Calculate the probabilities for each goal and store them in the config.goal_probabilities_list.

    Returns:
        pd.DataFrame: DataFrame containing the goal probabilities for display.
    """
    for goal in config.goals:
        probability = calculate_goal_probability(goal)
        for goal_prob in config.goal_probabilities_list:
            if(goal_prob["Goal"] == goal["Description"]):
                goal_prob["Probability"] = round(probability * 100, 2)
    # DataFrame aus der Liste erstellen
    goal_probabilities = pd.DataFrame(config.goal_probabilities_list)
    goal_probabilities["Probability"] = goal_probabilities["Probability"].astype(str) + "%"
    return goal_probabilities

# Für sucess rate
def calculate_team_influence():
    """
    Calculate the team influence on the overall success rate.

    Returns:
        float: Team influence on the overall success rate.
    """
    df = pd.DataFrame([
        {
            "name": item["name"],
            "role": item["role"],
            "experience_years": item["experience_years"],
            "age": item["age"],
            "LoC": item["params"]["Level of Commitment"],
            "IoT": item["params"]["Impact on team"],
            "Resistance": item["params"]["Resistance"]
        }
        for item in config.team_members
    ])

    sum_LoC = df['LoC'].sum()
    sum_IoT = df['IoT'].sum()

    # Berechnung der finalen Punkte
    df['final_score'] = (
            (df['LoC'] / sum_LoC +
             df['IoT'] / sum_IoT * (1 - df['Resistance'] / 10)) / 3
    )
    return round(df['final_score'].sum() + 0.2,2)

def calculate_milestones_achieved(achieved_milestones):
    """
    Calculate the multiplicator for the milestone success rate. Milestones are weighted evenly.

    Args:
        achieved_milestones (list): List of lists of achieved milestones.
    """
    total_milestones = sum(len(item["milestones"]) for item in config.iteration_milestone)
    length_achieved_milestones = sum(len(milestone) for milestone in achieved_milestones)
    prob = length_achieved_milestones/total_milestones
    config.milestone_multiplicator = round(prob * 0.4,2)

def calculate_overall_success():
    """
    Calculate the overall success rate based on the goal probabilities, milestone multiplicator and team influence
    """
    goals_probabilities_mean = 0.00
    for goal in config.goal_probabilities_list:
        goals_probabilities_mean += goal["Probability"]
    goals_probabilities_mean /= len(config.goal_probabilities_list)
    config.goals_multiplicator = round(goals_probabilities_mean/100*0.4, 2)

    # Calculate team influence
    team_influence = calculate_team_influence()
    config.team_multiplicator = round(team_influence * 0.2,2)