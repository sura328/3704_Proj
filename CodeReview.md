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
Found an issue with the web, where when trying to update a player's win/loss. There was an error. Used the LLM Gemini to help fix this issue by adding the follwing.

1. Backend (server.py and leaderboard.py) Changes:
- Update Player class in leaderboard.py to include a method for resetting/updating a player's record
- Added new API Endpoint to server.py to handle the update request. It will first update the win/loss record, then recalculate the ELO rating based on the new record.
2. Frontend (index.html and script.js) Changes:
- Added an update form in index.html by adding a new section in the html.
- Added update logic in script.js to handle sending the data to the new Flask endpoint.

This PR was assisted using the LLM Gemini to help find the error in the project and assist in updating the frontend and backend code. It was then tested for any errors and updated to fit the project requirements.

Comments:
