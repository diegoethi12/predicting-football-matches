import requests
import pandas as pd
from typing import Dict, List
from config import DATA_PATH


def get_matches_dicts(league: int, season: int) -> List[Dict]:
    # Api config
    endpoint = 'fixtures'
    url = f"https://v3.football.api-sports.io/{endpoint}"
    headers = {
        'x-rapidapi-key': '18c95b59fd4e3252bc6f1cf0ae7794e2',
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    # Make request
    payload = {
        "league": league,
        "season": season
    }
    response = requests.request("GET", url, headers=headers, params=payload)

    return response.json()


def build_matches_records(matches_dicts: List[Dict]) -> List[Dict]:
    return [
    {
        'home_team': match['teams']['home']['name'],
        'away_team': match['teams']['away']['name'],
        'home_goals': match['goals']['home'],
        'away_goals': match['goals']['away'],
        'status': match['fixture']['status']['long']
    }
    for match in matches_dicts['response']
    ]

if __name__ == '__main__':
    # Get matches from API Football
    matches_dicts = get_matches_dicts(34, 2022)
    matches_records = build_matches_records(matches_dicts)
    matches_df = pd.DataFrame.from_records(matches_records)

    # Save matches to disk
    DATA_PATH.mkdir(exist_ok=True)
    matches_df.to_pickle(DATA_PATH / 'conmebol_matches.pkl')
