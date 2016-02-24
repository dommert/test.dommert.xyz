from flask import Flask
from app import *


api_url = "/v1"


@app.route("/")
def hello():
    return "Hello World! Flask-Rambo"

@app.route("/about")
def about():
    return "This is the about page!"

@app.route(api_url+'/user', methods=["GET"])
def get_api_user():
     return jsonify(username="James Bond",
           email="bond007@rocketmail.com",
           id="007",
           data="You suck!!")

@app.route(api_url+'/user', methods=["POST"])
def post_api_user():
     return jsonify(error="Dont have access")

@app.route(api_url+'/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():


    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"



@app.route("/<path:path>")
def catch_all(path):
    return 'You want path: %s' % path