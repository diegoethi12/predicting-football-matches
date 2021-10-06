import requests
import pandas as pd

endpoint = 'fixtures'

url = f"https://v3.football.api-sports.io/{endpoint}"

payload = {
  "league": 34,
  "season": 2022
}

headers = {
  'x-rapidapi-key': '18c95b59fd4e3252bc6f1cf0ae7794e2',
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.request("GET", url, headers=headers, params=payload)

response.url
response.content
response.text
response.encoding
r = response.json()
r['response']
r['response'][0]['fixture']
r['response'][0]['fixture']['status']
r['response'][0]['league']
r['response'][0]['teams']
r['response'][0]['goals']
r['response'][0]['score']['fulltime']


matches_records = [
  {
    'home_team': match['teams']['home']['name'],
    'away_team': match['teams']['away']['name'],
    'home_goals': match['goals']['home'],
    'away_goals': match['goals']['away'],
    'status': match['fixture']['status']['long']
  }
 for match in r['response']
]

matches_records[0]

matches = pd.DataFrame.from_records(matches_records)

endpoint = 'standings'

url = f"https://v3.football.api-sports.io/{endpoint}"

response = requests.request("GET", url, headers=headers, params=payload)

response.url
response.content
response.text
response.encoding
r = response.json()
r['response']
r['response'][0]['league']
r['response'][0]['league']['standings']
r['response'][0]['league']['standings'][0][0]

