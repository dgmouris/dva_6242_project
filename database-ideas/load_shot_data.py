########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv

import json
from pathlib import Path
import pprint

import requests
#################################################################################

## Change to False to disable Sample
SHOW = True

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

# I want to test this on a single game first
TEST_GAME_ID = 20001.0
TEST_GAME_SEASON = 2023.0

# helpers
def get_full_game_id(partial_id, season):
    return f"{int(season)}0{int(partial_id)}"

# is numeric wasn't perfect.
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def convert_minute_format_to_seconds(string_time_value):
    # fix this handle none values better.
    if string_time_value is None:
        return 0.0
    minutes, seconds = string_time_value.split(':')
    total_time = float(minutes)*60 + float(seconds)
    return float(total_time)

def make_rows_values_correct_type(row):
    # row is a on object because of the dictreader here.
    # essentially just converts numbers to floats
    # and keeps the strings the same.
    for key in row.keys():
        value = row[key]
        if is_number(value):
            row[key] = float(value)

    return row

def get_shots_file_path():
    cwd = Path.cwd()
    shots_file_path = cwd.parent / "data" / "shots" / "shots_2023_2024.csv"
    return shots_file_path


# the meat of the parsing.
def import_shot_game_data(shots_file):
    print("importing shots...")

    all_shot_rows = []
    with open(shots_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)  # Uses the first line as column headers

        for row in reader:
            # converts string numbers and all nubmers to float
            row_clean = make_rows_values_correct_type(row)
            # skip if not in test game id remove when serious
            if row_clean["game_id"] != TEST_GAME_ID:
                continue


            all_shot_rows.append(row_clean)
    # get the shot data from ../data/shots/
    return all_shot_rows


# note we'll have to be carful with this to not ddos them
def import_shift_data(game_id, season):
    print("importing shifts...")
    # URL building
    full_game_id = get_full_game_id(game_id, season)
    full_url = f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={full_game_id}"

    response = requests.get(full_url)

    full_shift_data = response.json()

    # need to get the times of shifts in numbers
    # this is needed for the money puck data.
    for index, shift in enumerate(full_shift_data["data"]):
        start_time_number = convert_minute_format_to_seconds(shift["startTime"])
        end_time_number = convert_minute_format_to_seconds(shift["endTime"])
        duration_number = convert_minute_format_to_seconds(shift["duration"])

        # update the
        full_shift_data["data"][index]["startTimeNumber"] = start_time_number
        full_shift_data["data"][index]["endTimeNumber"] = end_time_number
        full_shift_data["data"][index]["durationNumber"] = duration_number

    return full_shift_data["data"]


def assign_players_on_ice_to_shots(shot_data, shift_data):
    print("assigning player shifts to shots...")
    for index, shot in enumerate(shot_data):
        players_for, players_against = get_players_on_ice_for_shot(shot, shift_data)
        
        shot_data[index]["playersOnIceFor"] = players_for
        shot_data[index]["playersOnIceAgainst"] = players_against

    return shot_data

# there's probably a better way of doing this with sets
# but if we need to process it once and then have the data then we should be good.
def get_players_on_ice_for_shot(shot, shift_data):
    players_for = []
    players_against = []
    period = shot["period"]
    shot_time = shot["time"]
    for shift in shift_data:
        if not (shift["startTimeNumber"] < shot_time
            and shift["endTimeNumber"] > shot_time
            and shift["period"] == period):
            continue

        if shot["teamCode"] == shift["teamAbbrev"]:
            players_for.append(shift)
        else:
            players_against.append(shift)

    return players_for, players_against

class shot_db_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # Create the table where the shot data lives
    def create_shot_table(self,connection):
        shot_table_sql = """CREATE TABLE shot_event(
                id REAL,
                shotID REAL,
                arenaAdjustedShotDistance REAL,
                arenaAdjustedXCord REAL,
                arenaAdjustedXCordABS REAL,
                arenaAdjustedYCord REAL,
                arenaAdjustedYCordAbs REAL,
                awayEmptyNet REAL,
                awaySkatersOnIce REAL,
                awayTeamCode TEXT,
                distanceFromLastEvent REAL,
                event TEXT,
                game_id REAL,
                goal REAL,
                homeEmptyNet REAL,
                homeSkatersOnIce REAL,
                homeTeamCode TEXT,
                location REAL,
                offWing REAL,
                period REAL,
                playerNumThatDidEvent REAL,
                playerPositionThatDidEvent REAL,
                season REAL,
                shooterLeftRight TEXT,
                shooterPlayerId REAL,
                shotAngle REAL,
                shotAngleAdjusted REAL,
                shotAnglePlusRebound REAL,
                shotAnglePlusReboundSpeed REAL,
                shotDistance REAL,
                shotGeneratedRebound REAL,
                shotGoalieFroze REAL,
                shotOnEmptyNet REAL,
                shotPlayContinuedInZone REAL,
                shotPlayContinuedOutsideZone REAL,
                shotRush REAL,
                shotType TEXT,
                shotWasOnGoal REAL,
                teamCode TEXT,
                time REAL,
                xCord REAL,
                xCordAdjusted REAL,
                xFroze REAL,
                xGoal REAL,
                xPlayContinuedInZone REAL,
                xPlayContinuedOutsideZone REAL,
                xPlayStopped REAL,
                xRebound REAL,
                xShotWasOnGoal REAL,
                yCord REAL,
                yCordAdjusted REAL
                
                );
        """
        
        return self.execute_query(connection, shot_table_sql)
    

    # Create the table where the shot data lives
    def create_shift_table(self,connection):
        shift_table_sql = """CREATE TABLE shot_event_shift(
                id REAL,
                shotID REAL,
                game_id REAL,

                shot_for_player_one REAL,
                shot_for_player_two REAL,
                shot_for_player_three REAL,

                shot_for_player_four REAL,
                shot_for_player_five REAL,


                shot_against_player_one REAL,
                shot_against_player_two REAL,
                shot_against_player_three REAL,

                shot_against_player_four REAL,
                shot_against_player_five REAL
                
                );
        """
        
        return self.execute_query(connection, shift_table_sql)
    

    # Create the table where the shot data lives, isolated to players on team shot was taken for
    def create_shift_table_iso_for(self,connection):
        shift_table_iso_for_sql = """CREATE TABLE shot_event_shift_for(
                id REAL,
                shotID REAL,
                game_id REAL,

                shot_for_player_one REAL,
                shot_for_player_two REAL,
                shot_for_player_three REAL,

                shot_for_player_four REAL,
                shot_for_player_five REAL
                
                );
        """
        
        return self.execute_query(connection, shift_table_iso_for_sql)
    

    # Create the table where the shot data lives, isolated to players on team shot was taken against
    def create_shift_table_iso_against(self,connection):
        shift_table_iso_against_sql = """CREATE TABLE shot_event_shift_against(
                id REAL,
                shotID REAL,
                game_id REAL,

                shot_against_player_one REAL,
                shot_against_player_two REAL,
                shot_against_player_three REAL,

                shot_against_player_four REAL,
                shot_against_player_five REAL
                
                );
        """
        
        return self.execute_query(connection, shift_table_iso_against_sql)

    def load_shot_data_reader(self,connection,shots_file):

        all_shots = import_shot_game_data(shots_file) 
        all_shifts = import_shift_data(TEST_GAME_ID, TEST_GAME_SEASON)

        if all_shots and all_shifts:
            for x in all_shots:
                players_for, players_against = get_players_on_ice_for_shot(x, all_shifts)

                while len(players_for) < 5:
                    players_for.append({'playerId':-1.0})
                while len(players_against) < 5:
                    players_against.append({'playerId':-1.0})

                connection.execute("""
                    INSERT INTO shot_event (
                    id,
                    shotID,
                    arenaAdjustedShotDistance,
                    arenaAdjustedXCord,
                    arenaAdjustedXCordABS,
                    arenaAdjustedYCord,
                    arenaAdjustedYCordAbs,
                    awayEmptyNet,
                    awaySkatersOnIce,
                    awayTeamCode,
                    distanceFromLastEvent,
                    event,
                    game_id,
                    goal,
                    homeEmptyNet,
                    homeSkatersOnIce,
                    homeTeamCode,
                    location,
                    offWing,
                    period,
                    playerNumThatDidEvent,
                    playerPositionThatDidEvent,
                    season,
                    shooterLeftRight,
                    shooterPlayerId,
                    shotAngle,
                    shotAngleAdjusted,
                    shotAnglePlusRebound,
                    shotAnglePlusReboundSpeed,
                    shotDistance,
                    shotGeneratedRebound,
                    shotGoalieFroze,
                    shotOnEmptyNet,
                    shotPlayContinuedInZone,
                    shotPlayContinuedOutsideZone,
                    shotRush,
                    shotType,
                    shotWasOnGoal,
                    teamCode,
                    time,
                    xCord,
                    xCordAdjusted,
                    xFroze,
                    xGoal,
                    xPlayContinuedInZone,
                    xPlayContinuedOutsideZone,
                    xPlayStopped,
                    xRebound,
                    xShotWasOnGoal,
                    yCord,
                    yCordAdjusted) 
                                
                    VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?         
                    )""", (x['id'], x['shotID'], x['arenaAdjustedShotDistance'], x['arenaAdjustedXCord'], x['arenaAdjustedXCordABS'],x['arenaAdjustedYCord'], x['arenaAdjustedYCordAbs'], x['awayEmptyNet'], x['awaySkatersOnIce'], x['awayTeamCode'],
                        x['event'], x['game_id'], x['goal'], x['homeEmptyNet'], x['homeSkatersOnIce'],x['homeTeamCode'], x['homeTeamWon'], x['location'], x['offWing'], x['period'],
                        x['playerNumThatDidEvent'], x['playerPositionThatDidEvent'], x['season'], x['shooterLeftRight'], x['shooterPlayerId'],x['shotAngle'], x['shotAngleAdjusted'], x['shotAnglePlusRebound'], x['shotAnglePlusReboundSpeed'], x['shotDistance'],
                        x['shotGeneratedRebound'], x['shotGoalieFroze'], x['shotOnEmptyNet'], x['shotPlayContinuedInZone'], x['shotPlayContinuedOutsideZone'],x['shotRush'], x['shotType'], x['shotWasOnGoal'], x['teamCode'], x['time'],
                        x['xCord'], x['xCordAdjusted'], x['xFroze'], x['xGoal'], x['xPlayContinuedInZone'],x['xPlayContinuedOutsideZone'], x['xPlayStopped'], x['xRebound'], x['xShotWasOnGoal'], x['yCord'],
                        x['yCordAdjusted']
                        
                        ))
                
                connection.execute("""
                    INSERT INTO shot_event_shift (
                        id,
                        shotID,
                        game_id,

                        shot_for_player_one, 
                        shot_for_player_two,
                        shot_for_player_three,

                        shot_for_player_four,
                        shot_for_player_five,


                        shot_against_player_one,
                        shot_against_player_two,
                        shot_against_player_three,

                        shot_against_player_four,
                        shot_against_player_five
                        ) 
                                
                    VALUES (
                        ?,
                        ?,
                        ?,

                        ?,
                        ?,
                        ?,

                        ?,
                        ?,


                        ?,
                        ?,
                        ?,

                        ?,
                        ?      
                    )""", (x['id'], x['shotID'], x['game_id'], 
                           players_for[0]['playerId'], players_for[1]['playerId'], players_for[2]['playerId'] , players_for[3]['playerId'] , players_for[4]['playerId'],
                           players_against[0]['playerId'], players_against[1]['playerId'], players_against[2]['playerId'], players_against[3]['playerId'], players_against[4]['playerId']
                        
                        ))
                

                connection.execute("""
                    INSERT INTO shot_event_shift_for (
                        id,
                        shotID,
                        game_id,

                        shot_for_player_one, 
                        shot_for_player_two,
                        shot_for_player_three,

                        shot_for_player_four,
                        shot_for_player_five
                        ) 
                                
                    VALUES (
                        ?,
                        ?,
                        ?,

                        ?,
                        ?,
                        ?,

                        ?,
                        ? 
                    )""", (x['id'], x['shotID'], x['game_id'], 
                           players_for[0]['playerId'], players_for[1]['playerId'], players_for[2]['playerId'] , players_for[3]['playerId'] , players_for[4]['playerId']
                        
                        ))
                
                connection.execute("""
                    INSERT INTO shot_event_shift_against (
                        id,
                        shotID,
                        game_id,

                        shot_against_player_one, 
                        shot_against_player_two,
                        shot_against_player_three,

                        shot_against_player_four,
                        shot_against_player_five
                        ) 
                                
                    VALUES (
                        ?,
                        ?,
                        ?,

                        ?,
                        ?,
                        ?,

                        ?,
                        ? 
                    )""", (x['id'], x['shotID'], x['game_id'], 
                           players_against[0]['playerId'], players_against[1]['playerId'], players_against[2]['playerId'] , players_against[3]['playerId'] , players_against[4]['playerId']
                        
                        ))
        connection.commit()
       ######################################################################
        
        sql = "SELECT COUNT(*) FROM shot_event;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
        # Part 4 Find the Most Prolific Actors [4 points]
    def query_shot_data(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        shot_data_sql = """SELECT *
                        FROM shot_event_shift
                        LIMIT 5
                            """
        ######################################################################
        cursor = connection.execute(shot_data_sql)
        return cursor.fetchall()



if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Shot and Shift Data Upload: " + '\033[m')
    db = shot_db_sql()


    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS shot_event;")
        conn.execute("DROP TABLE IF EXISTS shot_event_shift;")
        conn.execute("DROP TABLE IF EXISTS shot_event_shift_for;")
        conn.execute("DROP TABLE IF EXISTS shot_event_shift_against;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)



    shots_file = get_shots_file_path()

    try:
        print('\033[32m' + "Creating shot table: " + '\033[m' + str(db.create_shot_table(conn)))
    except Exception as e:
         print("Error in Creating Shot Table")
         print(e)

    try:
        print('\033[32m' + "Creating shift table: " + '\033[m' + str(db.create_shift_table(conn)))
    except Exception as e:
         print("Error in Creating Shift Table")
         print(e)

    try:
        print('\033[32m' + "Creating shift FOR table: " + '\033[m' + str(db.create_shift_table_iso_for(conn)))
    except Exception as e:
         print("Error in Creating Shift FOR Table")
         print(e)


    try:
        print('\033[32m' + "Creating shift AGAINST table: " + '\033[m' + str(db.create_shift_table_iso_against(conn)))
    except Exception as e:
         print("Error in Creating Shift AGAINST Table")
         print(e)



    try:
        print('\033[32m' + "Total shots loaded: " + '\033[m' + str(db.load_shot_data_reader(conn,shots_file)))
    except Exception as e:
         print("Error in Querying Total Shots")
         print(e)

    try:
        print('\033[32m' + "Shift data: " + '\033[m')
        for line in db.query_shot_data(conn):
            print(line)
    except Exception as e:
        print("Error in Shift Data")
        print(e)



    conn.close()
    #################################################################################
    #################################################################################
  
