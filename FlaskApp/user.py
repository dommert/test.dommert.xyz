from flask import request, jsonify
from project.models import User


@app.route('/signup', methods=['POST'])
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
