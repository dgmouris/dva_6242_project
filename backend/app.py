from dotenv import load_dotenv
import os

from flask import Flask # type: ignore

from flask_sqlalchemy import SQLAlchemy # type: ignore

# from extension_db import db

# gets the database
load_dotenv()
DATABASE_URL = os.getenv("DB_CONNECTION_STRING")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql+psycopg2://tyler:BXEzTQ3f5MXiFcEj@localhost:5433/POIU_Analytics'

db = SQLAlchemy(app)


