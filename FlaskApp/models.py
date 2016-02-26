# Model py
import datetime
from peewee import *
from app import db
from flask_chairy.utils import make_password, check_password



# -----------------------------------------------------

class BaseUser(object):
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

# User Class
class User(db.Model, BaseUser):
    username = CharField(unique=True, null=True)
    password = CharField()
    email = CharField(unique=True)
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __unicode__(self):
        return self.username