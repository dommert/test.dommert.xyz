# Dommert Flask Configs
# Configs v0.1.0-alpha



class Configuration(object):
# Flask Configs
    DEBUG = True
    PORT = 80 # default: 5000
    HOST = "0.0.0.0"
    STATIC = 'static'
    TEMPLATE = 'templates'

# Secrets, Keys, and Salts
    # Flask
    SECRET_KEY = "s0me random string!!"
    # Auth
    PASSWORD_SALT = "some0th3r Rad0m String!11"
    # JWT
    TOKEN_SECRET = "S0m3Thing R4nd0m Str!ng1!"

# PeeWee Database
    DATABASE = {
        'name': 'auth.db',
        'engine': 'peewee.SqliteDatabase',
        'check_same_thread': False,
    }