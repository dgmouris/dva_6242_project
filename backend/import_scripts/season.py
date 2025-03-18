import requests
import pprint

# season is the model passed in from the db.
def import_season(db, Season):
    print("Importing season data...")
    URL = "https://api-web.nhle.com/v1/season"
    response = requests.get(URL)
    data = response.json()

    allSeasons = []
    for year in data:
        print(year)
        allSeasons.append(Season(name=year))
        print("-------------------")
    db.session.add_all(allSeasons)
    db.session.commit()

    print("Added all Seasons.")
