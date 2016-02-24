#
# Flask Configs
DEBUG = True
PORT = 80
HOST = "0.0.0.0"


SECRET_KEY = "s0me random string!!"
PASSWORD_SALT = "some0th3r Rad0m String!11"
TOKEN_SECRET = "S0m3Thing R4nd0m Str!ng1!"

# PeeWee DB Config
class Configuration(object):
    DATABASE = {
        'name': 'flask_netbook.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }