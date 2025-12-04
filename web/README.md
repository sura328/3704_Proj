Leaderboard Web UI

This small web UI displays a leaderboard using your Python Leaderboard class and Elo calculations. The UI is served via Flask, so you can run the backend and frontend from a single server.

Files

templates/index.html — the web page

web/style.css — styling for the page

web/script.js — JavaScript that fetches leaderboard data and renders the table

leaderboard.py — Python leaderboard class

elo.py — Python Elo rating class

server.py — Flask backend serving the UI and API

How to run locally

Open a terminal and change directory to the project root (where server.py is located):

cd "c:\Users\hjpat\OneDrive\Desktop\CS 3704\3704_Proj"


Make sure Python 3 and Flask are installed. If not, install Flask:

pip install flask flask-cors


Run the Flask server:

python server.py


Open your browser and go to:

http://127.0.0.1:5000/


You should see the leaderboard UI. The page will fetch data from the backend automatically, and any changes made via the "Add Player" form will be reflected in the Python Leaderboard instance.

How to add initial players

You can prepopulate the leaderboard in server.py by editing the global leaderboard instance:

from leaderboard import Leaderboard

lb = Leaderboard("Main", k_factor=32)
lb.add_player("alice", wins=10, losses=2)
lb.add_player("bob", wins=8, losses=4)


Or, if you prefer JSON:

import json
from leaderboard import Leaderboard

lb = Leaderboard("Weekly")
lb.add_player("alice", wins=10, losses=2)
lb.add_player("bob", wins=8, losses=4)

with open('web/sample_players.json', 'w') as f:
    json.dump(lb.to_dict(), f, indent=2)


Then script.js can optionally load this JSON when the page first loads.

Notes

The Flask server serves the HTML from templates/ and static files from web/. No separate HTTP server is needed.

All API requests (add/remove players, record matches) are handled by server.py.

The leaderboard is sorted by Elo rating first, then win rate, total wins, fewer losses, and name.