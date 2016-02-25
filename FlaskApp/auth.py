# Auth

from flask import Flask, request, redirect
from flask import render_template, flash,
from app import app
from model import *
from config import Configuration
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from jwt import DecodeError, ExpiredSignature




# Create Users


# Login


# LogOut


# Hash_Pass


# Verify_Hash


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

# @Token

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



# ------ ROUTES -------- #

# Sign Up
@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    # JSON Data
    user = User(
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        # Add User
        db.session.add(user)
        db.session.commit()
        #password = generate_password_hash(user.password)
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    # Find Email
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})



@app.route('/api/dummy-api/', methods=['GET'])
@auth_token_required
def dummyAPI():
    ret_dict = {
        "Key1": "Value1",
        "Key2": "value2"
    }
    return jsonify(items=ret_dict)