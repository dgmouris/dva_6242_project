'''
This is going to have all of the database tables
so that we can interact with them in the db.
'''
from app import app, db
# from extension_db import db

from sqlalchemy.orm import DeclarativeBase # type: ignore

# base class for the image.
class Base(DeclarativeBase):
    pass


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Season {self.name}>"


def create_all_database_tables():
    print("Creating Database Tables...")
    with app.app_context():
        db.create_all()
    print("Successfully created all tables!")




