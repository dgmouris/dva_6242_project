from app import app, db

from models import Season

with app.app_context():
    seasons = Season.query.all()
    print(seasons)