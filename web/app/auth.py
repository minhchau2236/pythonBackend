from flask import g
from flask_httpauth import HTTPTokenAuth
from app.models import User

auth = HTTPTokenAuth()

@auth.verify_password
def verify_password(token):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
      return False
    g.user = user
    return True
