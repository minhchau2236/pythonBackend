from app import app, db
from flask import Flask, abort, request, jsonify, g, url_for
from app.data import User
from flask_restful import Api, Resource
from app.api.user import bp
from app.auth import auth

api = Api(bp)

class UserAPI(Resource):
  decorators = [auth.login_required]
  def get(self, id):
    user = User.query.filter_by(id = id).first()
    return {'username': user.username }, 200

class UsersAPI(Resource):
  decorators = [auth.login_required]
  def get(self):
    users = User.query.all()
    return { 'data': [i.json for i in users ] }, 200

  def post(self):
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        return abort(400) # existing user
    user = User(username = username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return { 'username': user.username, 'Location': url_for('user', id = user.id, _external = True)}, 200

api.add_resource(UserAPI, '/<int:id>', endpoint = 'user')
api.add_resource(UsersAPI, '', endpoint = 'userPost')