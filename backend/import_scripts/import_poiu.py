# important! you need to run the script to download all the shift data to the games

def import_poiu_to_shot_mapping(db, Shot, Player, POIU, get_or_create):
    print("Creating POIU to shot Mapping...")
    all_shots = db.session.query(Shot).filter_by(shooting_poiu_id=None).all()

    for shot in all_shots:
        # get the shot data as a dict
        shot_data = shot.as_dict()
        # get the shift data imported earlier.
        shift_data = shot.game.shift_data

        players_for, players_against = get_players_on_ice_for_shot(shot_data, shift_data)

        # remove the goalies from the the against team.
        goalie_shot_on = int(shot.goalieIdForShot)
        player_only_ids_against = [player["playerId"]
            for player in players_against
            if player["playerId"] != goalie_shot_on
        ]
        # sort
        player_only_ids_against.sort()

        # remove the goalies from the for team.
        all_player_ids_for = [int(player["playerId"]) for player in players_for]
        results = db.session.query(Player).filter(Player.id.in_(all_player_ids_for)).all()
        player_only_ids_for = [result.id for result in results]
        # sort

        situation = get_situation(player_only_ids_for, player_only_ids_against)

        # get the player ids as a column mapping as a dict
        poiu_data_for = get_mapping_to_database_columns(situation, player_only_ids_for)
        poiu_data_against = get_mapping_to_database_columns(situation, player_only_ids_against)

        try:
            # get the player ids as a column mapping as a dict
            poiu_for, created = get_or_create(db.session, POIU, **poiu_data_for)
            poiu_against, created = get_or_create(db.session, POIU, **poiu_data_against)

            # update shot with poius.
            shot.shooting_poiu_id = poiu_for.id
            shot.defending_poiu_id = poiu_against.id

            db.session.add(shot)
            print(F"updated shot {shot.id} with POIU")
        except Exception as error:
            print(F"error skipped {shot.id}")
    db.session.commit()
    print("Updated all shots with POIUs!")

def get_mapping_to_database_columns(situation, player_ids_only):
    MAPPING_TO_POIU_TABLES = [
        "player_one_id",
        "player_two_id",
        "player_three_id",
        "player_four_id",
        "player_five_id",
        "player_six_id"
    ]
    results = {}
    for index, player_id in enumerate(player_ids_only):
        table_col = MAPPING_TO_POIU_TABLES[index]
        results[table_col] = player_id

    results["situation"] = situation

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
    shot_time = shot["time"]
    for shift in shift_data:
        # get the shot time and period
        # this goes to the next shift if they are not on the ice.
        if not (shift["startTimeNumber"] < shot_time
            and shift["endTimeNumber"] > shot_time
            and shift["period"] == period):
            continue

        if shot["teamCode"] == shift["teamAbbrev"]:
            players_for.append(shift)
        else:
            players_against.append(shift)

    return players_for, players_against

def assign_players_on_ice_to_shots(shot_data, shift_data):
    print("assigning player shifts to shots...")
    for index, shot in enumerate(shot_data):
        # shot_time = shot["time"]
        # team_for = shot["teamCode"]
        players_for, players_against = get_players_on_ice_for_shot(shot, shift_data)

        shot_data[index]["playersOnIceFor"] = players_for
        shot_data[index]["playersOnIceAgainst"] = players_against

    return shot_data


