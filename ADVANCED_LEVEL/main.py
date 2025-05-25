import requests
from env.secret import token
import time
from flask import Flask, render_template, redirect, request, url_for, jsonify, session, flash, abort
from modules.statistics_parser import get_versus_stats, get_stats_by_team, get_all_goals_of_player
from modules.server_requests import *

app = Flask(__name__)

app.secret_key = 'secret_key'

@app.route("/versus", methods=['GET'])
def versus_endpoint():
    player1_id = request.args.get('player1_id')
    player2_id = request.args.get('player2_id')
    print(player1_id, player2_id)
    try:
        versus_statistic = get_versus_stats(int(player1_id), int(player2_id))
        if not versus_statistic['status']:
            abort(400)
        return render_template('versus.html', data=versus_statistic)
    except TypeError:
        abort(400)

@app.route("/stats", methods=['GET'])
def team_stats_endpoint():
    team_name = request.args.get('team_name')
    try:
        team_statistic = get_stats_by_team(team_name.strip('"'))
        if not team_statistic['status']:
            abort(400)
        return render_template('team.html', data=team_statistic)
    except AttributeError:
        abort(400)

@app.route("/goals", methods=['GET'])
def player_goals_statistic():
    player_id = request.args.get('player_id')
    try:
        player_statistic = get_all_goals_of_player(int(player_id))
        if not player_statistic['status']:
            abort(400)
        return render_template('goals.html', data=player_statistic)
    except AttributeError:
        abort(400)



if __name__ == "__main__":
    if check_connection_to_server():
        login()
        init_all_matches()
        init_all_teams()
        get_all_players()
    app.run(port=8080, host="127.0.0.1")