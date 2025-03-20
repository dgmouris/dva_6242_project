from app import app, db

from models import Season, Game

with app.app_context():
    print("hi")
    # season example
    # seasons = Season.query.all()
    # print(seasons)

    # games examples filter by season
    games = Game.query.filter_by(season_id=20232024).all()
    print(games)

