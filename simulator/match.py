import pandas as pd
from typing import List, Tuple
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np

from config import DATA_PATH


def get_average_goals(home_team: str, away_team: str, model) -> Tuple[int]:
    """Use the poisson model to return the expected average goals fro the
    home and away team of the match.

    Args:
        home_team (str): name of the home team
        away_team (str): name of the away team
        model ([type]): trained poisson model

    Returns:
        Tuple[int]: average expected goals for home team and away team of the match
    """
    home_goals_avg = model.predict(pd.DataFrame.from_dict({
        'team': [home_team],
        'opponent': [away_team],
        'home': [1]
    })).values[0]
    away_goals_avg = model.predict(pd.DataFrame.from_dict({
        'team': [away_team],
        'opponent': [home_team],
        'home': [0]
    })).values[0]

    return home_goals_avg, away_goals_avg


def simulate_match_goals_n_times(home_goals_avg: str, away_goals_avg: str, simulations:int) -> Tuple[List]:
    """Simulate home goals and away goals of the match using poisson
    distribution over the input average goals.
    The number of simulations is controlled by the simulations parameter.

    Args:
        home_goals_avg (str): average (lambda) home goals 
        away_goals_avg (str): average (lambda) away goals
        simulations (int): number of simulations to do

    Returns:
        Tuple[List]: Tuple with a list for home goals and a list for away goals
    """
    away_goals = np.random.poisson(away_goals_avg, simulations)
    home_goals = np.random.poisson(home_goals_avg, simulations)
    return home_goals, away_goals


def get_match_result():
    # Get result based on simulated match goals
    pass

def get_match_result_probabilities():
    # Return probabilities of win, loss and draw
    pass


# Get matches
matches = pd.read_pickle(DATA_PATH / 'conmebol_matches.pkl')

# Keep finished matches
finished_matches = matches.query('status == "Match Finished"')

# Create dataframe with model structure
model_columns = ['team', 'opponent', 'goals']
home_columns = ['home_team', 'away_team','home_goals']
away_columns = ['away_team', 'home_team','away_goals']
home_goals = finished_matches[home_columns].assign(home=1).rename(columns=dict(zip(home_columns, model_columns)))
away_goals = finished_matches[away_columns].assign(home=0).rename(columns=dict(zip(away_columns, model_columns)))
finished_matches_for_model = pd.concat([home_goals, away_goals])

# Fit model
goals_poisson_model = smf.glm(
    formula="goals ~ home + team + opponent",
    data=finished_matches_for_model,
    family=sm.families.Poisson()
    ).fit()

goals_poisson_model.summary()

home_goals_avg, away_goals_avg = get_average_goals('Chile', 'Venezuela', goals_poisson_model)
home_goals, away_goals_avg = simulate_match_goals_n_times(home_goals_avg, away_goals_avg, 100)
