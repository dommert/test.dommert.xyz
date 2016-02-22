from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
from flask import g

import jwt
from jwt import DecodeError, ExpiredSignature
from config import SECRET_KEY



users = Blueprint('users', __name__)

def create_token(user):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.utcnow(),
        #expiry
        'exp': datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


def login_required(f):
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

# JWT AUTh process end


class Auth(Resource):

    def post(self):
        data = request.get_json(force=True)
        print(data)
        email = data['email']
        password = data['password']
        user = Users.query.filter_by(email=email).first()
        if user == None:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response
        if check_password_hash(user.password, password):

            token = create_token(user)
            return {'token': token}
        else:
            response = make_response(
                jsonify({"message": "invalid username/password"}))
            response.status_code = 401
            return response