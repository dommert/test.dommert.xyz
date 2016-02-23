from flask import Flask, request, jsonify


'''
Flask-Token

Work without a frontend, all API and JSON access
  Make the base library just python

Build just a angular frontend
'''

# @Token
  # If token VerifyToken()
  # Else LoginPage

# Sign Up
   # +Form

 # Hash Password

# Login
   # +Form
 # Verify User

# Logout
 # Destroy token


# User Model
 # id
 # username
 # email
 # password
 # created
 # lastlogin
 # active
 # admin
 # (uid)

#

def create_token(user, expires = 24):
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

def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


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


## Views
@app.route('/signup', methods=['POST'])
def register():
    # Get JSON data
    json_data = request.json
    user = User(email=json_data['email'], password=json_data['password'])

    try:
        # Insert into User table
            # auth.signup(user.email, user.password)
        status = 'success'
    except:
        status = 'User already registered!'

    return jsonify({'result': status})


@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    #find the user in db
    user = User.query.filter_by(email=json_data['email']).first()

    if user and check_password_hash(user.password, json_data['password']):
        # Generate Token
        create_token()
        status = True
    else:
        status = False
    return jsonify({'result': status})



# Create a user to test with
@app.before_first_request
def create_user():
    db.create_all()
    if not User.query.first():
        user_datastore.create_user(email='test@example.com', password='test123')
        db.session.commit()