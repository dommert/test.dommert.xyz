# Model py
import datetime
from peewee import *
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


# -----------------------------------------------------

class BaseUser(object):
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# User Class
class User(db.Model, BaseUser):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username