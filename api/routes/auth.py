"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, Blueprint,current_app,make_response
from flask_jwt_extended import create_access_token,set_access_cookies,unset_jwt_cookies
import bcrypt

api = Blueprint('auth', __name__)


@api.route('/user/create',methods=["POST"])
def create_user():
    username = request.json["username"]
    password = bytes(request.json["password"],'utf-8')
    # hash password
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14)).decode("utf-8")
    dynamo = current_app.extensions["dynamo"]
    dynamo.table.load(f"{username}:USER",username=username,password=hashed)
    return jsonify({}),200

@api.route('/user/delete',methods=["DELETE"])
def delete_user():
    # username = request.json["username"]
    # password = bytes(request.json["password"],'utf-8')
    # # hash password
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt(14)).decode("utf-8")
    # dynamo = current_app.extensions["dynamo"]
    # dynamo.table.load(f"{username}:USER",username=username,password=hashed)
    return jsonify({}),200

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/user/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = bytes(request.json.get("password", None),'utf-8')
    dynamo = current_app.extensions["dynamo"]
    try:
        user = dynamo.table.query(f"{username}:USER")[0]
        user_password = bytes(user['password'],'utf-8')
        if bcrypt.checkpw(password, user_password):
            access_token = create_access_token(identity=user)
            response = jsonify({"status": True})
            set_access_cookies(response, access_token)
            return response
        else:
            return jsonify({"msg": "Bad username or password"}), 401
    except Exception as e:
        print(e)
        return jsonify({"msg": "Bad username or password"}), 401

@api.route("/user/logout", methods=["POST"])
def logout():
    response = make_response()
    unset_jwt_cookies(response)
    return response, 200

