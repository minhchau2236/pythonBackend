from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/api/users')

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    @app.route('/')
    @app.route('/index')
    def index():
        return "Hello, World!"

    return app

from app import auth