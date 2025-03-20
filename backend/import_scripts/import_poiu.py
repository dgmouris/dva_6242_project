import csv
from pathlib import Path
from datetime import datetime
# important! you need to run the script to download all the shift data to the games
from sqlalchemy.orm import joinedload # type: ignore
from sqlalchemy import update # type: ignore

def import_poiu_to_shot_mapping(db, Shot, Player, POIU, get_or_create):
    print("Creating POIU to shot Mapping...")
    before_query = datetime.now().timestamp()
    all_shots = db.session.query(
        Shot
    ).options(
        joinedload(Shot.game)
    ).filter_by(shooting_poiu_id=None).limit(10000).all()
    after_query = datetime.now().timestamp()
    print(F"query took {after_query-before_query}")

    goalie_ids = import_all_goalie_ids()

    # this is an array that will bulk add every 1000 shots.
    all_shots_to_add = []
    for index, shot in enumerate(all_shots):
        # get the shot data as a dict
        shot_data = shot.as_dict()
        # get the shift data imported earlier.
        shift_data = shot.game.shift_data

        players_for, players_against = get_players_on_ice_for_shot(shot_data, shift_data)

        # remove the goalies from the the against team.
        goalie_shot_on = int(shot.goalieIdForShot)
        player_only_ids_against = [player["playerId"]
            for player in players_against
            if player["playerId"] != goalie_shot_on and player["playerId"] not in goalie_ids
        ]
        # # sort
        player_only_ids_against.sort()

        # remove the goalies from the for team.
        all_player_ids_for = [int(player["playerId"])
            for player in players_for
            if  player["playerId"] not in goalie_ids
        ]
        # sort
        all_player_ids_for.sort()
        # results = db.session.query(Player).filter(Player.id.in_(all_player_ids_for)).all()
        # player_only_ids_for = [result.id for result in results]

        # all_player_ids_for = players_for
        # player_only_ids_against = players_against

        # sort
        situation = get_situation(all_player_ids_for, player_only_ids_against)

        # get the player ids as a column mapping as a dict
        poiu_data_for = get_mapping_to_database_columns(situation, all_player_ids_for)
        poiu_data_against = get_mapping_to_database_columns(situation, player_only_ids_against)

        try:

            # get the player ids as a column mapping as a dict
            poiu_for, created = get_or_create(db.session, POIU, **poiu_data_for)
            poiu_against, created = get_or_create(db.session, POIU, **poiu_data_against)

            # update shot with poius.
            shot.shooting_poiu_id = poiu_for.id
            shot.defending_poiu_id = poiu_against.id

            # all_shots_to_add.append(shot)
            shot_data = shot.as_dict()
            all_shots_to_add.append(shot_data)

            # if it's a thouasand
            if index % 1000 == 0:
                db.session.execute(
                    update(Shot),
                    all_shots_to_add,
                )
                # db.session.add_all(all_shots_to_add)
                db.session.commit()
                all_shots_to_add = []
            print(F"updated shot {shot.shotID} with POIU")
        except Exception as error:
            print(F"error skipped {shot.shotID}")
            print(error)

    print("Updated all shots with POIUs!")

def get_mapping_to_database_columns(situation, player_ids_only):
    MAPPING_TO_POIU_TABLES = [
        "player_one_id",
        "player_two_id",
        "player_three_id",
        "player_four_id",
        "player_five_id",
        "player_six_id",

    ]
    results = {}
    for index, player_id in enumerate(player_ids_only):
        if index >= len(MAPPING_TO_POIU_TABLES):
            continue
        table_col = MAPPING_TO_POIU_TABLES[index]
        results[table_col] = player_id

    results["situation"] = situation
    results["all_players"] = player_ids_only

    return results


# gets the situation.
def get_situation(player_only_ids_for, player_only_ids_against):
    return F"{len(player_only_ids_for)}on{len(player_only_ids_against)}"

# there's probably a better way of doing this with sets
# but if we need to process it once and then have the data then we should be good.
def get_players_on_ice_for_shot(shot, shift_data):
    players_for = []
    players_against = []

    period = shot["period"]

    # shot time is time into a game
    shot_time = shot["time"]

    # the shifts start from the period so we're going to add the offset time.
    PERIOD_OFFSET_TO_ADD_IN_SECONDS = 1200 # this is 60secs*20mins

    for shift in shift_data:
        # subtract 1 to the period and multiply by the seconds
        former_period_time_to_add = (shift["period"] - 1) * PERIOD_OFFSET_TO_ADD_IN_SECONDS
        # get the shot time and period
        shift_start_in_game = shift["startTimeNumber"] + former_period_time_to_add
        shift_end_in_game = shift["endTimeNumber"] + former_period_time_to_add
        # this goes to the next shift if they are not on the ice, debugging below.
        # print(F"{shot_time} start {shift_start_in_game} end {shift_end_in_game}")
        # start in game might be after a goal so that's why one is equal one is not.
        if not (shift_start_in_game < shot_time
            and shift_end_in_game >= shot_time
            and shift["period"] == int(period)):
            continue

        if shot["teamCode"] == shift["teamAbbrev"]:
            players_for.append(shift)
        else:
            players_against.append(shift)

    return players_for, players_against

def assign_players_on_ice_to_shots(shot_data, shift_data):
    print("assigning player shifts to shots...")
    for index, shot in enumerate(shot_data):

        players_for, players_against = get_players_on_ice_for_shot(shot, shift_data)

        shot_data[index]["playersOnIceFor"] = players_for
        shot_data[index]["playersOnIceAgainst"] = players_against

    return shot_data



def import_all_goalie_ids():

    file_path = Path(__file__)
    root = file_path.parent.parent.parent

    shots_data_file = Path(root / "data" / "goalies" / F"goalies_2023.csv")

    all_goalies_ids = []

    with open(shots_data_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers
        for row in reader:
            all_goalies_ids.append(int(row["playerId"]))
    return all_goalies_ids