#AI was used to create this file
# Prompt: create a python backend server to run python functions in script.js

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from leaderboard import Leaderboard, Player
from elo import Elo
import os

app = Flask(__name__, static_folder="web", template_folder="templates")
CORS(app)  # optional if frontend is served by Flask itself

# --------------------------------------------
# GLOBAL LEADERBOARD INSTANCE
# --------------------------------------------
lb = Leaderboard("Main", k_factor=32)

# --------------------------------------------
# FRONTEND ROUTE
# --------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------
# API ROUTES
# --------------------------------------------
@app.route("/players", methods=["GET"])
def get_players():
    return jsonify([p.to_dict() for p in lb.standings()])


@app.route("/add_player", methods=["POST"])
def add_player():
    data = request.json
    name = data["name"]
    wins = int(data.get("wins", 0))
    losses = int(data.get("losses", 0))

    # Add player
    p = lb.add_player(name, wins, losses)

    # Recalculate Elo based on W/L record
    elo_calc = Elo(lb.elo.k_factor)
    opponent = Player("baseline", rating=1500)

    for _ in range(wins):
        elo_calc.update_ratings(p, opponent)
    for _ in range(losses):
        elo_calc.update_ratings(opponent, p)

    return jsonify(p.to_dict())


@app.route("/record_match", methods=["POST"])
def record_match():
    data = request.json
    winner = data["winner"]
    loser = data["loser"]
    lb.record_match(winner, loser)
    return jsonify({"message": f"{winner} defeated {loser}"})


@app.route("/remove_player", methods=["POST"])
def remove_player():
    data = request.json
    name = data["name"]
    lb.remove_player(name)
    return jsonify({"message": f"removed {name}"})


@app.route("/player/<name>", methods=["GET"])
def get_player(name):
    p = lb.get_player(name)
    if not p:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(p.to_dict())


# --------------------------------------------
# RUN SERVER
# --------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)