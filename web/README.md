Leaderboard web UI

This small static site displays a leaderboard from a JSON export. It is intentionally lightweight so you can preview results locally or integrate it with a simple backend.

Files created
- index.html — the web page
- style.css — styling for the page
- script.js — loads JSON and renders the table
- sample_players.json — sample data you can use immediately

How to run locally (recommended)
1. Open PowerShell and change directory to the `web` folder:

   cd "c:\Users\hjpat\OneDrive\Desktop\CS 3704\3704_Proj\web"

2. Start a simple HTTP server (Python 3 must be installed):

   python -m http.server 8000

3. Open your browser and go to http://localhost:8000

Why serve via HTTP? Browsers block fetch() calls to local file:// URLs in many cases; serving the directory solves that.

How to export your leaderboard from Python

If you want to use the actual `Leaderboard` in this repo, you can export it to JSON and place the file in this folder as `sample_players.json`. Example:

```python
# run from the repo root or ensure imports resolve
from leaderboard import Leaderboard
import json

lb = Leaderboard('Weekly')
# add or load players as your app does
lb.add_player('alice', wins=10, losses=2)
lb.add_player('bob', wins=8, losses=4)

# write JSON compatible with the web UI
with open('web/sample_players.json', 'w') as f:
    json.dump(lb.to_dict(), f, indent=2)
```

Notes and next steps
- The UI accepts either a JSON object with a `players` array (the default `Leaderboard.to_dict()` shape) or a plain array of player objects.
- Optional improvements: add pagination, server-side route that returns leaderboard JSON via Flask/Express, or a form to record matches live.

If you'd like, I can add a tiny Python endpoint (Flask) to serve the leaderboard directly from your Python classes so the page can fetch fresh data. Tell me if you want that and I'll implement it.