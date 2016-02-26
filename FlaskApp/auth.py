# Auth

from flask import Flask, request, redirect, jsonify
from flask import render_template, flash
from app import app, db
from models import *
from config import Configuration
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from jwt import DecodeError, ExpiredSignature



# Create Token
def create_token(user, expires = 20):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.utcnow(),
        #expiry
        'exp': datetime.utcnow() + timedelta(hours=expires)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


# Parse Token
def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

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
            user = active.where(User.email == username).get()
        except User.DoesNotExist:
            return False
        else:
            if not check_password_hash(User.password, password):
                return False
        return user


# ------ ROUTES -------- #

# Sign Up
@app.route('/api/register', methods=['POST'])
def register():
    # JSON Data
    json_data = request.json

    try:
        # Add User
        hashed_pass = generate_password_hash(json_data['password'])
        user = User.create(
            username=NULL,
            password=hashed_pass,
            email=json_data['username'],
            created=datetime.datetime.now()
        )
        status = 'Success'
    except:
        status = 'This user is already registered!'

    return jsonify({'message': status})

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
      # Find Email
    user = User.select().where(User.email==json_data['username']).get()
    if authenticate(json_data['username'], json_data['password']):
        jtoken = create_token(user)
        status = True
    else:
        status = False
    return jsonify({'result': status, 'token': jtoken, 'user': json_data['username']})



