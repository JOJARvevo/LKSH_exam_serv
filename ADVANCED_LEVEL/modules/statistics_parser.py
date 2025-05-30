from ADVANCED_LEVEL.database import (take_all_matches, take_teams_by_id,
                                     get_team_name_by_id, get_player_name_by_id, take_team_id_by_name)


def get_versus_stats(player1_id, player2_id):
    statistic = {
        'player1_name': '',
        'player2_name': '',
        'count_of_matches': 0,
        'status': 0,
        'matches': []
    }
    if player1_id < 0 or player2_id < 0:
        return statistic
    player1_name = get_player_name_by_id(player1_id)
    player2_name = get_player_name_by_id(player2_id)
    if not player1_name or not player2_name:
        return statistic
    statistic['player1_name'] = " ".join(player1_name).strip()
    statistic['player2_name'] = " ".join(player2_name).strip()
    player1_teams = take_teams_by_id(player1_id)
    player2_teams = take_teams_by_id(player2_id)
    matches = take_all_matches()
    for player1_team in player1_teams:
        player1_team = player1_team[0]
        for player2_team in player2_teams:
            player2_team = player2_team[0]
            if player1_team == player2_team:
                continue
            for match in matches:
                if match['match_id'] in [1, 49, 375]:
                    print(match)
                if match['team1'] == player1_team and match['team2'] == player2_team:
                    print(match['match_id'])
                    statistic['count_of_matches'] += 1
                    player1_team_name = get_team_name_by_id(player1_team)
                    player2_team_name = get_team_name_by_id(player2_team)
                    statistic['matches'].append(
                        (player1_team_name, player2_team_name, match['team1_score'], match['team2_score']))
                elif match['team1'] == player2_team and match['team2'] == player1_team:
                    print(match['match_id'])
                    statistic['count_of_matches'] += 1
                    player1_team_name = get_team_name_by_id(player1_team)
                    player2_team_name = get_team_name_by_id(player2_team)
                    statistic['matches'].append(
                        (player1_team_name, player2_team_name, match['team2_score'], match['team1_score']))
    statistic['status'] = 1
    return statistic



def get_stats_by_team(team_name):
    statistic = {
        'team_name': team_name,
        'total_wins': 0,
        'total_loses': 0,
        'difference': 0,
        'status': 0
    }
    team_id = take_team_id_by_name(team_name)
    if not team_id:
        return statistic
    team_id = team_id[0]
    sum_skipped = 0
    sum_get = 0
    matches = take_all_matches()
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
    statistic = {
        'status': 0,
        'goals': []
    }
    goals = get_all_players_goals(player_id)
    if not len(goals):
        return statistic
    formated_goals = [{'match': goal[0], 'minute': goal[1]} for goal in goals]
    statistic['status'] = 1
    statistic['goals'] = formated_goals
    return statistic