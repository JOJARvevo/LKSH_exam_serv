from modules.server_requests import players_to_teams, matches, team_name_to_id

def get_versus_stats(player1_id, player2_id):
    statistic = {
        'count_of_matches': 0,
        'status': 0
    }
    if player1_id < 0 or player2_id < 0:
        return statistic
    if player1_id not in players_to_teams or player2_id not in players_to_teams:
        return statistic
    statistic['count_of_matches'] = 0
    player1_teams = players_to_teams[player1_id]
    player2_teams = players_to_teams[player2_id]
    for player1_team in player1_teams:
        for player2_team in player2_teams:
            if player1_team == player2_team:
                continue
            for match in matches:
                if (match['team1'] == player1_team or match['team2'] == player1_team) \
                    and (match['team1'] == player2_team or match['team2'] == player2_team):
                    statistic['count_of_matches'] += 1
    statistic['status'] = 1
    return statistic



def get_stats_by_team(team_name):
    statistic = {
        'total_wins': 0,
        'total_loses': 0,
        'difference': 0,
        'status': 0
    }
    if team_name not in team_name_to_id:
        return statistic
    team_id = team_name_to_id[team_name]
    sum_skipped = 0
    sum_get = 0
    for match in matches:
        if match['team1'] == team_id:
            sum_skipped += match['team2_score']
            sum_get += match['team1_score']
            difference = match['team1_score'] - match['team2_score']
            if difference < 0:
                statistic['total_loses'] += 1
            elif difference > 0:
                statistic['total_wins'] += 1
        elif match['team2'] == team_id:
            sum_skipped += match['team1_score']
            sum_get += match['team2_score']
            difference = match['team2_score'] - match['team1_score']
            if difference < 0:
                statistic['total_loses'] += 1
            elif difference > 0:
                statistic['total_wins'] += 1
    statistic['difference'] = sum_get - sum_skipped
    statistic['status'] = 1
    return statistic

def get_all_goals_of_player(player_id):
   pass