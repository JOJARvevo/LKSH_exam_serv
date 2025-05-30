import time
import requests
from env.secret import token
from ADVANCED_LEVEL.modules.top_secret_messeage import message

BASE_URL = 'https://lksh-enter.ru'

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
    if req.status_code != 200:
        return 0
    return 1


def request_all_matches():
    request = requests.get(BASE_URL + "/matches", headers={'Authorization': token})
    if request.status_code != 200:
        return []
    try:
        matches = request.json()
        return matches
    except requests.exceptions.JSONDecodeError:
        print("TO MANY REQUESTS, SLEEP FOR 60 SECONDS")
        time.sleep(60)
        return request_all_matches()


def request_all_teams():
    request = requests.get(BASE_URL + "/teams", headers={'Authorization': token})
    if request.status_code != 200:
        return []
    teams = request.json()
    return teams

def request_all_players():
    from ADVANCED_LEVEL.database import take_all_players_ids

    all_players = []
    loading = 0
    players_ids = take_all_players_ids()
    for player_id in players_ids:
        loading += 1
        player_id = player_id[0]
        print(f"LOADING PLAYERS {loading}/433")
        try:
            request_for_player = requests.get(BASE_URL + f"/players/{player_id}", headers={'Authorization': token})
            player = request_for_player.json()
        except Exception:
            print("TO MANY REQUESTS, SLEEP FOR 60 SECONDS")
            time.sleep(60)
            request_for_player = requests.get(BASE_URL + f"/players/{player_id}", headers={'Authorization': token})
            player = request_for_player.json()
        all_players.append(player)
    return all_players

def request_all_goals():
    from ADVANCED_LEVEL.database import take_all_matches

    all_goals = []
    loading = 0
    matches = take_all_matches()
    count_of_matches = len(matches)
    for match in matches:
        loading += 1
        print(f"LOADING GOALS {loading}/{count_of_matches}")
        try:
            request_for_goals = requests.get(BASE_URL + f"/goals", json={"match_id": match['match_id']}, headers={'Authorization': token})
            goals = request_for_goals.json()
        except Exception:
            print("TO MANY REQUESTS, SLEEP FOR 60 SECONDS")
            time.sleep(60)
            request_for_goals = requests.get(BASE_URL + f"/goals", json={"match_id": match['match_id']}, headers={'Authorization': token})
            goals = request_for_goals.json()
        all_goals += goals
    result_goals = [(goal_stats['id'], goal_stats['player'], goal_stats['match'], goal_stats['minute']) for goal_stats in all_goals]
    return result_goals