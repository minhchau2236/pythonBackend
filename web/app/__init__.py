from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

from app.api.user import bp as user_bp
app.register_blueprint(user_bp, url_prefix='/api/users')

from app.api.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')

from app import auth
from app.data import User