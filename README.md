# GenAI-in-Software-Engineering

The goal is to develop a software-based visual configurator which simulates and visualizes the implementation of CoPilot. This simulator should represent the interplay of critical success factors along a roadmap including milestones of AI implementation in a user friendly way while referring explicitly to CoPilot in software development and engineering.

```bash
pip install dash pandas dash_bootstrap_components
```

Then run the app:

```bash
python app.py
```
# Calculation for goals
For each goal, the calculation of the probability is done as follows:
- Goal is calculated by considering the progress of its associated factors. Each factor has a weight, and the progress is determined either from KPI data or CSF data. The weighted progress of all factors is summed up and divided by the total weight to get the probability of achieving the goal. If no factors are present, the probability is set to 0.
- Overall success for simplicity is calculated: 0.2 Team + 0.4 Milestones achieved + 0.4 Goals
# How to configure the parameters
- The parameters can be configured in the `params.json` file.
- The `factors` key contains the list of factors. Each factor has the following keys:
  - `name`: The name of the factor.
  - `weight`: The weight of the factor in the calculation of the goal probability.
  - `type`: The type of the factor. It can be either `kpi` or `csf`.
  - `kpi`: The name of the KPI associated with the factor. This key is only present if the factor type is `kpi`.
  - `csf`: The name of the CSF associated with the factor. This key is only present if the factor type is `csf`.








#### If you want to change the styling of the app, change the `dbc.themes.BOOTSTRAP` line in `app.py` to any of the following:

- [x] dbc.themes.BOOTSTRAP
- [x] dbc.themes.CERULEAN
- [x] dbc.themes.COSMO
- [x] dbc.themes.CYBORG
- [x] dbc.themes.DARKLY
- [x] dbc.themes.FLATLY
- [x] dbc.themes.JOURNAL
- [x] dbc.themes.LITERA
- [x] dbc.themes.LUMEN
- [x] dbc.themes.LUX
- [x] dbc.themes.MATERIA
- [x] dbc.themes.MINTY
- [x] dbc.themes.MORPH
- [x] dbc.themes.PULSE
- [x] dbc.themes.QUARTZ
- [x] dbc.themes.SANDSTONE
- [x] dbc.themes.SIMPLEX
