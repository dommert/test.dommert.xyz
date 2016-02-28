# Auth
# Dommert Inc
'''
import datetime
from config import Configuration
from flask_chairy.utils import make_password, check_password
from flask import Flask, redirect, render_template, flash
'''

from flask import request, jsonify, g
from app import app, db
from models import *

from functools import wraps
import jwt
from jwt import DecodeError, ExpiredSignature


# Create Token
def create_token(user, expires=24):
    """

    :param user:
    :param expires: INT hours till token expires. default is 24
    :return:
    """
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.datetime.utcnow(),
        #expiry
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expires)
    }

    token = jwt.encode(payload, app.config['TOKEN_KEY'], algorithm='HS256')
    return token.decode('unicode_escape')


# Parse Token
def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_KEY'], algorithms='HS256')

# @Token Wrapper
def token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Where art thou Token?')
            response.status_code = 401
            return response
        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid :<')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired! :(')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

# Authenicate User

def authenticate(username, password):

    try:
        user = User.get((User.active == True) & (User.username == username))
        if not user.check_password(password):
             return False
    except User.DoesNotExist:
        return False
    return user



# ------ ROUTES -------- #

# Sign Up
@app.route('/api/register', methods=['POST'])
def register():
    # JSON Data
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
    try:
        user = User(username=username, active=True, join_date=datetime.datetime.now())
        user.set_password(password)
        user.save()
        status = True
        msg = 'Success!'
    except:
        status = False
        msg = 'This user is already registered!'
    return jsonify(status=status, message=msg)

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
      # -- Need to make option to login username/email
    if authenticate(username, password):
        user = User.select().where(User.username == username).get()
        jwtoken = create_token(user)
        status = True
        return jsonify(status=status, token=jwtoken, userId=user.id, user=user.email)
    else:
        status = False
        return jsonify(status=status, message="Authentication Error!!")



