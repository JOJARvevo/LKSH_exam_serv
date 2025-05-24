import requests
from env.secret import token
import time
from sys import stdin

BASE_URL = 'https://lksh-enter.ru'
matches = []
players_to_teams = {}
team_name_to_id = {}
teams = []

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

def print_all_players():
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
            players_to_teams[player_id] = team['id']
            fullname = (player['name'] + " " + player['surname']).strip()
            if fullname:
                all_names.append(fullname)
    print("\n".join(sorted(set(all_names))))


def get_versus_stats(player1_id, player2_id):
    if player1_id < 0 or player2_id < 0:
        return 0
    if player1_id not in players_to_teams or player2_id not in players_to_teams:
        return 0
    player1_team = players_to_teams[player1_id]
    player2_team = players_to_teams[player2_id]
    count_of_matches = 0
    if player1_team == player2_team:
        return count_of_matches
    for match in matches:
        if (match['team1'] == player1_team or match['team2'] == player1_team) \
            and (match['team1'] == player2_team or match['team2'] == player2_team):
            count_of_matches += 1
    return count_of_matches



def get_stats_by_team(team_name):
    if team_name not in team_name_to_id:
        return "0 0 0"
    team_id = team_name_to_id[team_name]
    total_wins = 0
    total_loses = 0
    sum_skipped = 0
    sum_get = 0
    for match in matches:
        if match['team1'] == team_id:
            sum_skipped += match['team2_score']
            sum_get += match['team1_score']
            difference = match['team1_score'] - match['team2_score']
            if difference < 0:
                total_loses += 1
            elif difference > 0:
                total_wins += 1
        elif match['team2'] == team_id:
            sum_skipped += match['team1_score']
            sum_get += match['team2_score']
            difference = match['team2_score'] - match['team1_score']
            if difference < 0:
                total_loses += 1
            elif difference > 0:
                total_wins += 1
    if sum_get - sum_skipped > 0:
        return f"{total_wins} {total_loses} +{sum_get - sum_skipped}"
    return f"{total_wins} {total_loses} {sum_get - sum_skipped}"


init_all_matches()
init_all_teams()
print_all_players()

for users_input in stdin:
    users_input = users_input.split()
    command, data = users_input[0], users_input[1:]
    if command == 'stats?':
        team_name = data.strip('"')
        print(get_stats_by_team(team_name))
    elif command == 'versus?':
        try:
            print(get_versus_stats(int(data[0]), int(data[1])))
        except TypeError:
            print("some of ID is not a number")
    else:
        print("Unknown command, try another")
