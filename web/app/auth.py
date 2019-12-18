from flask import g
from flask_httpauth import HTTPTokenAuth
from app.data import User

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
      return False
    g.user = user
    return True
