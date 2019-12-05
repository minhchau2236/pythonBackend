from app import app, db
from flask import Flask, abort, request, jsonify, g, url_for
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/api/login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
       abort(401) # invalid user
    token = g.user.generate_auth_token()
    return jsonify({ 'user': user, 'token': token.decode('ascii') })

@app.route('/api/user', methods = ['POST'])
def new_user():
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
    return jsonify({ 'username': user.username, 'Location': url_for('new_user', id = user.id, _external = True)}), 200, {'Location': url_for('new_user', id = user.id, _external = True)}

@app.route('/api/user', methods = ['GET'])
def get_user():
    id = request.args.get('id')
    user = User.query.filter_by(id = id).first()
    return jsonify( {'username': user.username }), 200