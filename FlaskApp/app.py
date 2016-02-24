# App.py

from flask import Flask
#from peewee import *
#from flask_chairy.db import Database

app = Flask(__name__)
app.config.from_object('config.Configuration')

#db = Database(app)
#def create_tables():
#    User.create_table()