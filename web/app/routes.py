from app import app, db
from flask import Flask, abort, request, jsonify, g, url_for
from app.data import User
from flask_restful import Api, Resource
from app.auth import auth

api = Api(app)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

class UserAPI(Resource):
  decorators = [auth.login_required]
  def get(self, id):
    user = User.query.filter_by(id = id).first()
    return {'username': user.username }, 200

class UserPostAPI(Resource):
  decorators = [auth.login_required]
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

# @app.route('/api/login', methods = ['POST'])
# def login():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         abort(400) # missing arguments
#     user = User.query.filter_by(username = username).first()
#     if not user or not user.check_password(password):
#        abort(401) # invalid user
#     token = user.generate_auth_token()
#     return jsonify({ 'id': user.id, 'name': user.username, 'token': token.decode('ascii') }), 200

# @app.route('/api/user', methods = ['POST'])
# def new_user():
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         return abort(400) # missing arguments
#     if User.query.filter_by(username = username).first() is not None:
#         return abort(400) # existing user
#     user = User(username = username)
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({ 'username': user.username, 'Location': url_for('user', id = user.id, _external = True)}), 200

# @app.route('/api/user', methods = ['GET'])
# @auth.login_required
# def get_user():
#     id = request.args.get('id')
#     user = User.query.filter_by(id = id).first()
#     return jsonify( {'username': user.username }), 200

api.add_resource(UserAPI, '/api/user/<int:id>', endpoint = 'user')
api.add_resource(UserPostAPI, '/api/user', endpoint = 'userPost')
api.add_resource(LoginAPI, '/api/login', endpoint = 'login')
