import csv

from sqlalchemy import  text

from app import app, db

shot_with_poiu_sql_query= F"""
    SELECT
        shot.*,
        shooting_poiu.player_one_id,
        shooting_poiu.player_two_id,
        shooting_poiu.player_three_id,
        shooting_poiu.player_four_id,
        shooting_poiu.player_five_id,
        shooting_poiu.player_six_id,
        shooting_poiu.all_players,
        shooting_poiu.situation,
        defending_poiu.player_one_id,
        defending_poiu.player_two_id,
        defending_poiu.player_three_id,
        defending_poiu.player_four_id,
        defending_poiu.player_five_id,
        defending_poiu.player_six_id,
        defending_poiu.all_players
    FROM public.shot shot
    INNER JOIN public.poiu shooting_poiu ON shot.shooting_poiu_id = shooting_poiu.id
    INNER JOIN public.poiu defending_poiu ON shot.defending_poiu_id = defending_poiu.id
"""

# this is a one off script to allow dylan to do some clustering with our generated data.
def create_csv():
    print("creating the similarity algo csv")
    with app.app_context():
        query = text(shot_with_poiu_sql_query)
        executed_query = db.session.execute(query)
        columns = executed_query.keys()
        results = executed_query.all()
        # write to csv row by row
        with open("shot_data_with_poiu.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            # Write each row
            for row in results:
                writer.writerow(row)

    print("successfully created!")

if __name__  == "__main__":
    create_csv()