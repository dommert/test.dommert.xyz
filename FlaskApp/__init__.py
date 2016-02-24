# API.Dommert.xyz
from flask import Flask, jsonify, request
from app import app
from views import *
#from models import *



if __name__ == "__main__":
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])



