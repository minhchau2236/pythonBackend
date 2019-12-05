from flask import g
from flask_httpauth import HTTPTokenAuth
from app.models import User

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    # first try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
      return False
    g.user = user
    return True
