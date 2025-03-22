import os
import sys
# this is needed for flask to know about the current modules do not remove.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)


from sqlalchemy import  text, case

from app import app, db
# from flask import request, jsonify,current_app as app
from models import Player, POIU
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

# get units that generate the most shots by a a player id and a situation.
@app.route("/get_units_by_player_id", methods=("GET",))
def get_units_by_player_id():
    player_id = request.args.to_dict().get("player_id")
    situation = request.args.to_dict().get("situation")

    unit_sql_query = F"""
        SELECT
            poiu.id,
            poiu.situation,
            SUM(CASE WHEN shot.shooting_poiu_id = poiu.id THEN 1 ELSE 0 END) AS shot_for_count,
            SUM(CASE WHEN shot.defending_poiu_id = poiu.id THEN 1 ELSE 0 END) AS shot_against_count,
            poiu.player_one_id,
            poiu.player_two_id,
            poiu.player_three_id,
            poiu.player_four_id,
            poiu.player_five_id,
            poiu.player_six_id,
            poiu.all_players
        FROM public.poiu
        INNER JOIN public.shot ON poiu.id = shot.shooting_poiu_id OR poiu.id = shot.defending_poiu_id
        WHERE
            (   poiu.player_one_id = {player_id} OR
                poiu.player_two_id = {player_id} OR
                poiu.player_three_id = {player_id} OR
                poiu.player_four_id = {player_id} OR
                poiu.player_five_id = {player_id} OR
                poiu.player_six_id = {player_id}
            ) AND
            situation = '{situation}'
        GROUP BY
            poiu.id,
            poiu.situation,
            poiu.player_one_id,
            poiu.player_two_id,
            poiu.player_three_id,
            poiu.player_four_id,
            poiu.player_five_id,
            poiu.player_six_id,
            poiu.all_players
        ORDER BY shot_for_count DESC
        LIMIT 5
    """
    query = text(unit_sql_query)
    results = db.session.execute(query).all()
    # get the ids for each result
    unit_ids = []
    UNIT_ID_INDEX = 0
    for result in results:
        unit_ids.append(result[UNIT_ID_INDEX])

    return jsonify(unit_ids)

# gets all of the players in lists of forwards and dmen (for easier frontend parsing)
@app.route("/get_players_by_poiu", methods=("GET",))
def get_players_by_poiu():
    poiu = request.args.to_dict().get("poiu")

    # get the poiu
    poiu = POIU.query.filter(POIU.id==poiu).first()
    # custom order to make it easier to render on the frontend
    custom_order = case(
       {"L": 1, "C": 2, "R": 3, "D": 4},
        value=Player.position,
        else_=5  # Default order for other roles
    )

    # get the players
    players = Player.query.filter(
        Player.id.in_(poiu.all_players)
    ).order_by(
        custom_order
    ).all()

    forwards = []
    defensemen = []
    FORWARD_POSITIONS = ["C", "L", "R"]
    DEFENSE_POSITIONS = ["D"]

    for player in players:
        if player.position in DEFENSE_POSITIONS:
            defensemen.append(player.as_dict())
        elif player.position in FORWARD_POSITIONS:
            forwards.append(player.as_dict())

    return jsonify({
        "forwards": forwards,
        "defensemen": defensemen
    })

# this is just stubbed out
# for once we have the similarity metric working.
# right now it's just getting random POIUs
@app.route("/get_similar_units_by_poiu")
def get_similar_units_by_poiu():
    poiu = request.args.to_dict().get("poiu")
    situation = request.args.to_dict().get("situation")
    # I don't care about this one because it'll be removed
    from sqlalchemy.sql.expression import func

    # get some random poius so we can get it on the
    # frontend
    poius = POIU.query.filter(
        POIU.situation==situation
    ).order_by(
        func.random()
    ).limit(5).all()

    # just return the ids like the "get_units_by_player_id"
    return jsonify([int(poiu.id) for poiu in poius])
