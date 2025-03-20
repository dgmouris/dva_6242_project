import os
import sys
# this is needed for flask to know about the current modules do not remove.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from app import app
# from flask import request, jsonify,current_app as app
from models import Player
from flask import request, jsonify

# this is needed so that next.js can access our application.
from flask_cors import CORS
CORS(app)

@app.route("/search_players", methods=("GET",))
def search_players():
    # convert the arguments to a dictionary
    player_searched = request.args.to_dict().get("q")

    # this should be sanitized: Todo later.

    # clean this up.
    players = Player.query.filter(Player.full_name.ilike(F"%{player_searched}%")).limit(5).all()
    # format for dict
    players_as_dicts = []
    for player in players:
        players_as_dicts.append(player.as_dict())
    # return json.
    return jsonify({"players": players_as_dicts})

# Note: new paths will be added below.
