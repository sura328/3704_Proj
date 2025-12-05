Sura:
  Integrated the front end UI with a Flask backend. All code changes were assisted by AI (Copilot) and then reviewed and refined manually
  
  Changes:
  
  1. Backend (server.py)
  - Serves HTML from templates/ and static files from web/
  - provides API endpoints for: fetching players (/players), adding a new player with elo rating based on W/L record (/add_player), recording a match result (/record_match), removing a player (/remove_player), getting a players data (/player/<name>)
  - Elo ratings are simulated against a baseline player
  2. Frontend (templates/index.html and web/script.js)
  - HTML updated to use Flask for CSS/JS
  - Script fetches players from backend and renders a dynamic leaderboard
  - Adding players now calculates Elo automatically based on wins and losses
  3. README (web/README.md)
  - Updated to explain how to run project with a single Flask server
  - Instructions for prepopulating leaderboard and viewing the UI
  
  AI usage:
  - This PR was AI-assisted. Copilot helped generate backend and frontend code, which was then manually tested and refactored to the project requirements.

Comments:

Henry:

Comments:

David:

Comments:

Nyssa:

Comments:
