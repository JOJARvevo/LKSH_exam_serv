import sqlite3

from ADVANCED_LEVEL.modules.server_requests import request_all_teams, request_all_players, request_all_matches, login

def rebuild_db():
    login()
    clear_db()
    init_all_teams(request_all_teams())
    init_all_players(request_all_players())
    init_all_matches(request_all_matches())


def init_all_matches(matches):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    matches = [(match['id'], match['team1'], match['team2'], match['team1_score'], match['team2_score']) for match in matches]
    cursor.executemany("INSERT INTO matches (match_id, team1_id, team2_id, team1_score, team2_score) VALUES (?,?,?,?,?)", matches)
    conn.commit()
    conn.close()

def init_all_players(players):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    players = [(player['id'], player['name'], player['surname'], player['number']) for player in players]
    cursor.executemany("INSERT INTO players (player_id, name, surname, number) VALUES(?,?,?,?)", players)
    conn.commit()
    conn.close()

def init_all_teams(teams):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    teams_data = []
    players_data = []
    for team in teams:
        teams_data.append((team['id'], team['name']))
        for player_id in team['players']:
            players_data.append((team['id'], player_id))
    cursor.executemany("INSERT INTO teams (team_id, team_name) VALUES(?,?)", teams_data)
    cursor.executemany("INSERT INTO players_to_teams (team_id, player_id) VALUES(?,?)", players_data)
    conn.commit()
    conn.close()

def take_all_matches():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    matches = cursor.execute("SELECT * FROM matches").fetchall()
    conn.close()
    keys = ['match_id', 'team1', 'team1_score', 'team2', 'team2_score']
    matches = [dict(zip(keys, values)) for values in matches]
    return matches

def take_teams_by_id(player_id):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    all_teams = cursor.execute("SELECT team_id FROM players_to_teams WHERE player_id = ?", (player_id,)).fetchall()
    conn.close()
    return all_teams

def get_team_name_by_id(team_id):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    team_name = cursor.execute("SELECT team_name FROM teams WHERE team_id = ?", (team_id,)).fetchone()[0]
    conn.close()
    return team_name

def take_all_players_ids():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    players_ids = cursor.execute("SELECT DISTINCT player_id FROM players_to_teams").fetchall()
    conn.close()
    return players_ids

def take_team_id_by_name(team_name):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    team_id = cursor.execute("SELECT team_id FROM teams WHERE team_name = ?", (team_name,)).fetchone()
    conn.close()
    return team_id

def get_player_name_by_id(player_id):
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    player_name = cursor.execute("SELECT name, surname FROM players WHERE player_id = ?", (player_id,)).fetchone()
    conn.close()
    return player_name

def clear_db():
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teams")
    cursor.execute("DELETE FROM players")
    cursor.execute("DELETE FROM matches")
    cursor.execute("DELETE FROM players_to_teams")
    cursor.execute("DELETE FROM goals")
    conn.commit()
    conn.close()
