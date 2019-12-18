from flask import Blueprint

bp = Blueprint('auth_api', __name__)

from app.api.auth import controller