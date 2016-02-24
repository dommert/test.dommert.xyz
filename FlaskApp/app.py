# Flask
from flask import Flask
from peewee import *
# Flask-TurboDuck
from flask_chairy.db import Database

app = Flask(__name__)
app.config.from_object('config')

db = Database(app)

def create_tables():
    User.create_table()
