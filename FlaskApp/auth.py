# Auth

import datetime
from flask import Flask, request, redirect, jsonify
from flask import render_template, flash
from app import app, db
from models import *
from config import Configuration
from flask_chairy.utils import make_password, check_password
from functools import wraps
import jwt
from jwt import DecodeError, ExpiredSignature



# Create Token
def create_token(user, expires=20):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.datetime.utcnow(),
        #expiry
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expires)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token.decode('unicode_escape')


# Parse Token
def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')

# @Token Wrapper
def token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response
        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

# Authenicate User
def authenticate(username, password):
        active = User.select().where(User.active == True)
        try:
            hashpassword = User.password
            user = active.where((User.email == username) & (User.password == hashpassword)).get()
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
    hashed_pass = make_password(password)
    try:
        user = User(username=False, email=username, admin=False, active=True, join_date=datetime.datetime.now())
        user.set_password(password)
        user.save()
        status = true
        msg = 'Success ' + username
    except:
        status = false
        msg = 'This user is already registered!'
    return jsonify(status=status, message=msg)

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    username = json_data['username']
    password = json_data['password']
      # Find Email
    user = User.select().where(User.email==username).get()
    if authenticate(username, password):
        jtoken = create_token(user)
        status = True
        return jsonify(status= status, access_token= jtoken)
    else:
        status = False
        return jsonify(status= status, message="Login Error!")



