from app import app, db
from flask import Flask, abort, request, jsonify, g, url_for
from app.data import User
from flask_restful import Api, Resource
from app.api.auth import bp
from app.auth import auth

api = Api(bp)

class LoginAPI(Resource):
  def post(self):
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    user = User.query.filter_by(username = username).first()
    if not user or not user.check_password(password):
       abort(401) # invalid user
    token = user.generate_auth_token()
    return { 'id': user.id, 'name': user.username, 'token': token.decode('ascii') }, 200

api.add_resource(LoginAPI, '/login', endpoint = 'login')
