import requests

# season is the model passed in from the db.
def import_season(db, Season):
    print("Importing season data...")
    URL = "https://api-web.nhle.com/v1/season"
    response = requests.get(URL)
    data = response.json()

    allSeasons = []
    for year in data:
        season_id = int(year)
        # Check if the season already exists in the database
        if not db.session.query(Season).filter_by(id=season_id).first():
            allSeasons.append(
                Season(id=season_id, name=year)
            )

    if allSeasons:  # Only add if there are new seasons to insert
        db.session.add_all(allSeasons)
        db.session.commit()
        print("Added all Seasons.")
    else:
        print("No new Seasons to add.")