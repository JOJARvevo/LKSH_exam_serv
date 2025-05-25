import time

import requests

from env.secret import token
from modules.top_secret_messeage import message

BASE_URL = 'https://lksh-enter.ru'
matches = []
players_to_teams = {}
team_name_to_id = {}
teams = []

def check_connection_to_server():
    request = requests.get(BASE_URL + "/", headers={'Authorization': token})
    if request.status_code != 200:
        return 0
    return 1

def login():
    json_data = {
        'reason': message
    }
    req = requests.post(BASE_URL + "/login", json=json_data, headers={'Authorization': token})

def init_all_matches():
    global matches
    request = requests.get(BASE_URL + "/matches", headers={'Authorization': token})
    matches = request.json()

def init_all_teams():
    global teams
    request = requests.get(BASE_URL + "/teams", headers={'Authorization': token})
    teams = request.json()
    for team in teams:
        team_name_to_id[team['name']] = team['id']

def get_all_players():
    global players_to_teams
    all_names = []
    cnt = 0
    for team in teams:
        for player_id in team['players']:
            cnt += 1
            request_for_player = requests.get(BASE_URL + f"/players/{player_id}", headers={'Authorization': token})
            try:
                player = request_for_player.json()
            except requests.exceptions.JSONDecodeError:
                time.sleep(60)
                player = request_for_player.json()
            if player_id in players_to_teams:
                players_to_teams[player_id].append(team['id'])
            else:
                players_to_teams[player_id] = [team['id']]
            fullname = (player['name'] + " " + player['surname']).strip()
            if fullname:
                all_names.append(fullname)