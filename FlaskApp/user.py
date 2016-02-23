from flask import Flask, request, jsonify, session
from flask import request, jsonify
from project.models import User
app = Flask(__name__)

@app.route('/api/signup', methods=['POST'])
def register():
    # Get JSON data
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password']
    )

    try:
        # Insert into User table
        db.session.add(user)
        db.session.commit()
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.json
    #find the user in db
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=80)
